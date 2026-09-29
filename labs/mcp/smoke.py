"""真实 STDIO 握手、工具发现、合法/非法调用；不需要 AI 账号。"""
import asyncio
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command=sys.executable, args=['-m', 'labs.mcp.server'],
                                   cwd=str(Path(__file__).resolve().parents[2]))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=10) as session:
            await session.initialize()
            names = {t.name for t in (await session.list_tools()).tools}
            assert names == {'course_list_tasks', 'course_task_stats'}, names
            items = await session.call_tool('course_list_tasks', {'status': 'open', 'limit': 10})
            assert not items.is_error, items
            stats = await session.call_tool('course_task_stats', {})
            assert not stats.is_error, stats
            invalid = await session.call_tool('course_list_tasks', {'status': 'unknown'})
            assert invalid.is_error, invalid
            invalid_limit = await session.call_tool('course_list_tasks', {'limit': 0})
            assert invalid_limit.is_error, invalid_limit
            print(json.dumps({'protocol': 'real MCP over STDIO', 'data': 'fixed classroom fixtures',
                              'tools': sorted(names), 'valid_calls': 2, 'invalid_calls_rejected': 2},
                             ensure_ascii=False, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
