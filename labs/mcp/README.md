# 可选实验：真实 MCP，两项只读工具

这里通过官方 Python SDK 执行真实 MCP 握手、发现与调用。数据是固定课堂样例，**没有调用 LLM，也没有连接外部 API或个人数据库**。后两项需要学习者继续扩展。

已选择 SDK `mcp==2.2.0`，与 [当前官方指南](https://modelcontextprotocol.io/docs/develop/build-server) 的 `MCPServer` 接口一致。主线无需安装这些依赖。

## 安装与运行

从课程根目录执行，使用独立虚拟环境。

macOS/Linux：

```bash
python3 -m venv .venv-mcp
.venv-mcp/bin/python -m pip install -r labs/mcp/requirements.txt
.venv-mcp/bin/python -m labs.mcp.smoke
```

Windows PowerShell：

```powershell
py -3.12 -m venv .venv-mcp
.venv-mcp/Scripts/python.exe -m pip install -r labs/mcp/requirements.txt
.venv-mcp/Scripts/python.exe -m labs.mcp.smoke
```

成功输出应包含两个工具、2 次合法调用、2 次非法调用被拒绝。`requirements.txt` 固定顶层 SDK；`requirements-verified.txt` 记录维护时在 Linux/Python 3.12 的已验证依赖组合。其他平台重新验证，不保证所有传递依赖永久兼容。

STDIO 服务器不在终端直接展示网页；它等待客户端的协议消息。启动后安静等待不等于卡死。服务日志写 stderr，不能向 stdout 随意 print。

## 接入你已有的 MCP 客户端

在支持本地 STDIO 的客户端新增服务器，command 填虚拟环境 Python 的**绝对路径**，args 为 `-m`、`labs.mcp.server`，工作目录填课程根目录。不同客户端配置字段不同，以该客户端官方文档为准；不要把一种 JSON 配置直接当作所有产品通用。

如果客户端无法设置工作目录，可使用下面的启动形式，脚本会切换到仓库目录：

```text
command: /绝对路径/.venv-mcp/bin/python
args: ["/绝对路径/modern-software-dev-course/labs/mcp/launch.py"]
```

Windows 用对应的 `.venv-mcp/Scripts/python.exe`。让客户端发现 `course_list_tasks` 和 `course_task_stats`，发起只读查询，记录真实调用证据。烟雾测试通过说明协议可用，不代表某个桌面客户端已配置成功。

## 工具契约

| 工具 | 参数 | 输出 | 副作用 |
| --- | --- | --- | --- |
| course_list_tasks | status=all/open/done；limit 为 1–50 整数 | 有限任务列表 | 无 |
| course_task_stats | 无 | total、done、open | 无 |

下一步按 [选学 S03](../../optional/03-context-mcp.md)接自己的只读数据，再接有权使用的外部 API。明确超时、空结果、错误和速率限制。不要给这个查询工具增加任意 shell 或任意文件路径能力。
