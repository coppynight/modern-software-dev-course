"""筛选作业独立 HTTP 验收；起始版本应失败，不属于基线 CI。

运行：python verify-filter.py --project YOUR_PRACTICE_COPY
仅使用临时数据库与随机本地端口，不读取或改写 data/tasks.db。
"""
import argparse
import http.client
import json
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser(description='独立练习HTTP验收；仅临时数据')
parser.add_argument('--project', required=True, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.project.resolve()))
from app.server import handler_for
from app.store import Store


def main():
    failures = []
    checks = 0

    def check(label, actual, expected):
        nonlocal checks
        checks += 1
        if actual != expected:
            failures.append(label)
            print(f'FAIL {label}: expected={expected!r}, actual={actual!r}')
        else:
            print(f'PASS {label}')

    with tempfile.TemporaryDirectory(prefix='course-filter-') as directory:
        store = Store(Path(directory) / 'tasks.db')
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(store))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        def request(method, path, data=None):
            connection = http.client.HTTPConnection('127.0.0.1', server.server_address[1], timeout=5)
            try:
                body = None if data is None else json.dumps(data).encode('utf-8')
                connection.request(method, path, body, {'Content-Type': 'application/json'})
                response = connection.getresponse()
                return response.status, json.loads(response.read())
            finally:
                connection.close()

        def expect_list(label, path, expected):
            status, body = request('GET', path)
            check(label + ' HTTP', status, 200)
            # 比较完整对象及顺序，不能只比较条数。
            check(label + ' 内容与顺序', body, expected)

        try:
            for path in ('/api/tasks', '/api/tasks?status=all',
                         '/api/tasks?status=open', '/api/tasks?status=done'):
                expect_list('无数据 ' + path, path, [])
            tasks = []
            for title in ('第一项未完成', '第二项已完成', '第三项未完成', '第四项已完成'):
                status, task = request('POST', '/api/tasks', {'title': title})
                if status != 201:
                    raise RuntimeError(f'无法准备数据：POST 返回 {status}: {task}')
                tasks.append(task)
            for index in (1, 3):
                status, task = request('PATCH', f"/api/tasks/{tasks[index]['id']}", {'done': True})
                if status != 200:
                    raise RuntimeError(f'无法准备数据：PATCH 返回 {status}: {task}')
                tasks[index] = task
            snapshot = store.list()
            expect_list('省略 status 默认全部', '/api/tasks', tasks)
            expect_list('all 全部', '/api/tasks?status=all', tasks)
            expect_list('open 未完成', '/api/tasks?status=open', [tasks[0], tasks[2]])
            expect_list('done 已完成', '/api/tasks?status=done', [tasks[1], tasks[3]])
            status, body = request('GET', '/api/tasks?status=invalid')
            check('非法值 HTTP', status, 400)
            check('非法值明确错误', isinstance(body, dict) and isinstance(body.get('error'), str)
                  and bool(body['error'].strip()), True)
            check('全部查询与非法输入不修改数据库', store.list(), snapshot)
            # 有数据但无匹配项，不只测试空数据库。
            for task in tasks:
                status, body = request('PATCH', f"/api/tasks/{task['id']}", {'done': True})
                if status != 200:
                    raise RuntimeError(f'无法准备空结果：PATCH 返回 {status}: {body}')
            snapshot = store.list()
            expect_list('有数据但 open 无匹配', '/api/tasks?status=open', [])
            check('空结果查询不修改数据库', store.list(), snapshot)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    print(f'{checks - len(failures)}/{checks} checks passed')
    if failures:
        print('筛选作业尚未完成；起始版本出现此结果是预期。基线绿灯不代表作业通过。')
        return 1
    print('HTTP 筛选契约通过；页面、失败恢复与学员解释仍需单独验收。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
