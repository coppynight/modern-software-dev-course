"""运行方式：从根目录执行 python -m labs.mcp.server。"""
from typing import Annotated, Literal
from mcp.server import MCPServer
from pydantic import Field
from labs.task_tools import list_tasks, task_stats

server = MCPServer('course-tasks', instructions='只读教学数据，无个人任务，无外部 API。')


@server.tool()
def course_list_tasks(status: Literal['all', 'open', 'done'] = 'all',
                      limit: Annotated[int, Field(strict=True, ge=1, le=50)] = 10) -> list[dict]:
    """查询固定课堂任务；不读取本地真实数据库，也不修改数据。"""
    return list_tasks(status, limit)


@server.tool()
def course_task_stats() -> dict:
    """返回固定课堂数据的总数、完成数和未完成数，无副作用。"""
    return task_stats()


if __name__ == '__main__':
    server.run(transport='stdio')
