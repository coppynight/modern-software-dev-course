# 小事板 API 与项目导览

起始版本，仅本机单用户。JSON 使用 UTF-8，响应包含 `X-Request-ID`。默认绑定 `127.0.0.1:8000`。

| 方法 | 路径 | 输入 | 成功 | 常见失败 |
| --- | --- | --- | --- | --- |
| GET | `/health` | 无 | 200，`{"ok":true}` | 只检查进程响应，不检查数据库 |
| GET | `/api/tasks` | 无 | 200，按 id 顺序的任务数组 | 500，存储故障 |
| POST | `/api/tasks` | `{"title":"读书"}` | 201，包含 id/title/done | 400，标题不合法或多余字段 |
| PATCH | `/api/tasks/1` | title、done 至少一个 | 200，更新后任务 | 400，字段/类型错误；404，不存在 |
| DELETE | `/api/tasks/1` | 无 | 200，`{"deleted":true}` | 404，不存在 |
| POST | `/api/extract` | `{"note":"- 读书"}` | 200，tasks 数组和 `engine:"rules"` | 400，类型或长度不合法 |

标题去首尾空白后 1–120 字符；done 只能为 JSON 布尔值，字符串 `"false"` 不接受。笔记最多 4000 字符；提取预览不写数据库，候选需用户逐条确认。当前规则识别 `- `、`* `、`TODO:`、`待办：`，按原顺序去重，不理解任意自然语言。

POST/PATCH 须为 `application/json` 对象，请求体最多 20000 字节。415=内容类型错误；413=体积超限或空体；403=Host/Origin 不符合本机访问约束；404=未知路径/记录。未知方法可能由标准库返回 501。GET 查询参数目前未定义且不会自动实现筛选。

## 从哪里修改

`app/domain.py` 负责数据规则；`app/store.py` 负责参数化 SQL 与事务；`app/server.py` 负责路由、请求/响应、日志；`app/static/` 是浏览器页面；`tests/test_app.py` 使用临时数据库，独立于你的实际任务。

完整数据流：表单值 → fetch/JSON → HTTP 路由 → 校验 → SQLite → JSON 响应 → 文本节点呈现。新增功能尽量沿这条链路逐层修改，不把模型调用、数据库和 DOM 操作堆到同一处。
