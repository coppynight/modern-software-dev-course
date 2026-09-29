"""本地单用户课堂服务器；不是互联网部署模板。"""
import argparse
import json
import re
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from app.domain import extract_tasks
from app.store import Store

STATIC = Path(__file__).parent / "static"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
          "/style.css": ("style.css", "text/css")}


class APIError(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


def handler_for(store):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def respond(self, status, body, content_type="application/json"):
            data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.status_code = status
            self.send_response(status)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Request-ID", self.request_id)
            self.send_header("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(data)

        def body(self):
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                raise APIError(415, "请求须使用 application/json")
            if self.headers.get("Transfer-Encoding"):
                raise APIError(400, "不支持分块请求")
            try:
                size = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise APIError(400, "请求长度无效") from None
            if not 0 < size <= 20000:
                raise APIError(413, "请求体为空或超过 20000 字节")
            try:
                value = json.loads(self.rfile.read(size))
            except (ValueError, UnicodeDecodeError):
                raise APIError(400, "JSON 格式无效") from None
            if not isinstance(value, dict):
                raise APIError(400, "JSON 顶层须为对象")
            return value

        def handle_request(self):
            start = time.perf_counter()
            self.connection.settimeout(5)
            self.request_id = uuid.uuid4().hex[:12]
            self.status_code = 500
            path = urlsplit(self.path).path
            try:
                port = self.server.server_address[1]
                hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
                if self.headers.get("Host") not in hosts:
                    raise APIError(403, "只允许本机地址访问")
                origin = self.headers.get("Origin")
                if origin and origin not in {f"http://{h}" for h in hosts}:
                    raise APIError(403, "不允许跨站请求")
                if self.command == "GET" and path in ASSETS:
                    filename, mime = ASSETS[path]
                    return self.respond(200, (STATIC / filename).read_bytes(), mime)
                if self.command == "GET" and path == "/health":
                    return self.respond(200, {"ok": True})
                if self.command == "GET" and path == "/api/tasks":
                    return self.respond(200, store.list())
                if self.command == "POST" and path == "/api/tasks":
                    data = self.body()
                    if set(data) != {"title"}:
                        raise ValueError("创建任务只接受 title")
                    return self.respond(201, store.add(data["title"]))
                if self.command == "POST" and path == "/api/extract":
                    data = self.body()
                    if set(data) != {"note"}:
                        raise ValueError("提取只接受 note")
                    return self.respond(200, {"tasks": extract_tasks(data["note"]), "engine": "rules"})
                match = re.fullmatch(r"/api/tasks/([1-9][0-9]*)", path)
                if match and self.command == "PATCH":
                    return self.respond(200, store.update(int(match[1]), self.body()))
                if match and self.command == "DELETE":
                    store.delete(int(match[1]))
                    return self.respond(200, {"deleted": True})
                raise APIError(404, "接口不存在")
            except APIError as exc:
                self.respond(exc.status, {"error": exc.message})
            except ValueError as exc:
                self.respond(400, {"error": str(exc)})
            except KeyError:
                self.respond(404, {"error": "任务不存在"})
            except (BrokenPipeError, ConnectionResetError):
                self.status_code = 499
            except Exception:
                self.respond(500, {"error": "内部错误，请记录请求编号"})
            finally:
                # 不记录标题、笔记、请求体、查询串或密钥。
                route = path if path in ASSETS or path in {"/health", "/api/tasks", "/api/extract"} else "/other"
                if re.fullmatch(r"/api/tasks/[1-9][0-9]*", path):
                    route = "/api/tasks/:id"
                print(json.dumps({"request_id": self.request_id, "method": self.command,
                                  "route": route, "status": self.status_code,
                                  "duration_ms": round((time.perf_counter() - start) * 1000, 2)}),
                      file=sys.stderr, flush=True)

        do_GET = do_POST = do_PATCH = do_DELETE = handle_request

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", type=Path, default=ROOT / "data/tasks.db")
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(Store(args.db)))
    print(f"小事板 http://127.0.0.1:{server.server_address[1]}（Ctrl+C 停止）", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
