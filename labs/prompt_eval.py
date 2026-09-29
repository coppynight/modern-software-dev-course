"""严格匹配是教学指标；不代表唯一合理的自然语言评价方法。"""
import argparse
import json
from pathlib import Path

from app.domain import extract_tasks


def evaluate(cases, predictions):
    if not isinstance(cases, list) or not cases:
        raise ValueError('cases 必须是非空数组')
    if not isinstance(predictions, dict):
        raise ValueError('predictions 必须是以案例 id 为键的 JSON 对象')
    seen, rows = set(), []
    for case in cases:
        if not isinstance(case, dict) or set(case) != {'id', 'note', 'expected'}:
            raise ValueError('每个案例须含 id、note、expected')
        key = case['id']
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError('案例 id 须为非空且不重复的字符串')
        seen.add(key)
        if not isinstance(case['note'], str) or not isinstance(case['expected'], list) or not all(isinstance(x, str) for x in case['expected']):
            raise ValueError('note 须为字符串，expected 须为字符串数组')
        actual = predictions.get(key)
        valid = isinstance(actual, list) and all(isinstance(x, str) for x in actual)
        rows.append({'id': key, 'valid_shape': valid, 'exact_match': valid and actual == case['expected'],
                     'expected': case['expected'], 'actual': actual})
    return {'total': len(rows), 'exact_matches': sum(r['exact_match'] for r in rows),
            'valid_shapes': sum(r['valid_shape'] for r in rows),
            'extra_prediction_ids': sorted(set(predictions) - seen), 'cases': rows}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cases', type=Path, default=Path(__file__).with_name('prompt-cases.json'))
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--baseline', action='store_true')
    mode.add_argument('--predictions', type=Path)
    args = p.parse_args()
    try:
        cases = json.loads(args.cases.read_text(encoding='utf-8'))
        predictions = ({c['id']: extract_tasks(c['note']) for c in cases} if args.baseline
                       else json.loads(args.predictions.read_text(encoding='utf-8')))
        report = evaluate(cases, predictions)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        p.exit(2, f'评测输入错误：{exc}\n')
    report['mode'] = 'deterministic-rules-not-LLM' if args.baseline else 'supplied-predictions'
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
