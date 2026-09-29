"""汇总本地教学日志。p95 使用 nearest-rank 定义。"""
import argparse
import json
import math
from pathlib import Path


def summarize(text):
    events, skipped = [], 0
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            status, duration = event['status'], event['duration_ms']
            if type(status) is not int or not 100 <= status <= 599:
                raise ValueError('invalid status')
            if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
                raise ValueError('invalid duration')
            events.append(event)
        except (ValueError, TypeError, KeyError):
            skipped += 1
    durations = sorted(e['duration_ms'] for e in events)
    n = len(events)
    errors = sum(500 <= e['status'] <= 599 for e in events)
    return {'requests': n, 'client_4xx': sum(400 <= e['status'] <= 499 for e in events),
            'server_5xx': errors, 'server_error_rate': errors / n if n else None,
            'p95_ms_nearest_rank': durations[math.ceil(.95 * n) - 1] if n else None,
            'skipped_lines': skipped}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('log', type=Path)
    args = p.parse_args()
    try:
        raw = args.log.read_bytes()
        text = raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')
    except (OSError, UnicodeError) as exc:
        p.exit(2, f'无法读取日志：{exc}\n')
    print(json.dumps(summarize(text), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
