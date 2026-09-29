"""有限步、脚本决策的教学轨迹，帮助区分提议、执行与观测。"""
import json
from labs.task_tools import list_tasks


def run_trace(calls=None, max_steps=3):
    if type(max_steps) is not int or max_steps < 1:
        raise ValueError('max_steps 必须为正整数')
    if calls is None:
        calls = [{'tool': 'list_tasks', 'arguments': {'status': 'unfinished'}},
                 {'tool': 'list_tasks', 'arguments': {'status': 'open'}}]
    events = [{'kind': 'metadata', 'decision_source': 'scripted fixture; no LLM'}]
    for index, call in enumerate(calls[:max_steps], 1):
        events.append({'step': index, 'kind': 'proposed_call', 'call': call})
        try:
            if call.get('tool') != 'list_tasks':
                raise ValueError('工具不在只读允许列表中')
            value = list_tasks(**call['arguments'])
            events.append({'step': index, 'kind': 'tool_result', 'ok': True, 'value': value})
        except (ValueError, TypeError, KeyError) as exc:
            events.append({'step': index, 'kind': 'tool_result', 'ok': False, 'error': str(exc)})
    events.append({'kind': 'stop', 'reason': 'budget' if len(calls) > max_steps else 'script_complete'})
    return events


if __name__ == '__main__':
    for event in run_trace():
        print(json.dumps(event, ensure_ascii=False))
