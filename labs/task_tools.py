"""教学工具契约，固定假数据，不执行 MCP 协议或真实模型调用。"""
import json

SAMPLE_TASKS = (
    {'id': 1, 'title': '阅读课程', 'done': False},
    {'id': 2, 'title': '运行测试', 'done': True},
)


def list_tasks(status='all', limit=10, tasks=SAMPLE_TASKS):
    if status not in ('all', 'open', 'done'):
        raise ValueError('status 必须为 all、open 或 done')
    if type(limit) is not int or not 1 <= limit <= 50:
        raise ValueError('limit 必须为 1–50 的整数')
    return [dict(t) for t in tasks if status == 'all' or t['done'] == (status == 'done')][:limit]


def task_stats(tasks=SAMPLE_TASKS):
    done = sum(bool(t['done']) for t in tasks)
    return {'total': len(tasks), 'done': done, 'open': len(tasks) - done}


if __name__ == '__main__':
    print(json.dumps({'mode': 'fixture-functions-not-MCP', 'tasks': list_tasks('open'), 'stats': task_stats()}, ensure_ascii=False, indent=2))
