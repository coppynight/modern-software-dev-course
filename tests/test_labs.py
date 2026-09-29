import unittest
from labs.agent_trace import run_trace
from labs.prompt_eval import evaluate
from labs.task_tools import list_tasks, task_stats
from tools.log_summary import summarize


class LabTests(unittest.TestCase):
    def test_eval_shape_missing_and_semantics(self):
        cases = [{'id': 'a', 'note': '', 'expected': []}, {'id': 'b', 'note': '- x', 'expected': ['x']}]
        report = evaluate(cases, {'a': [], 'b': 'x'})
        self.assertEqual(report['exact_matches'], 1)
        self.assertEqual(report['valid_shapes'], 1)
        self.assertEqual(evaluate(cases, {})['exact_matches'], 0)

    def test_duplicate_cases_rejected(self):
        case = {'id': 'a', 'note': '', 'expected': []}
        with self.assertRaises(ValueError): evaluate([case, case], {})

    def test_tool_contract(self):
        self.assertEqual(list_tasks('open')[0]['done'], False)
        self.assertEqual(list_tasks('done')[0]['done'], True)
        self.assertEqual(task_stats([]), {'total': 0, 'done': 0, 'open': 0})
        for args in ({'status': 'wrong'}, {'limit': True}, {'limit': 0}, {'limit': 51}):
            with self.subTest(args=args), self.assertRaises(ValueError): list_tasks(**args)

    def test_trace_failure_recovery_budget_and_allowlist(self):
        results = [e for e in run_trace() if e['kind'] == 'tool_result']
        self.assertFalse(results[0]['ok']); self.assertTrue(results[1]['ok'])
        self.assertEqual(run_trace([{'tool': 'delete_all'}] * 4, 2)[-1]['reason'], 'budget')
        self.assertEqual(len([e for e in run_trace([{'tool': 'delete_all'}] * 4, 2) if e['kind'] == 'tool_result']), 2)

    def test_logs_empty_bad_and_p95(self):
        self.assertIsNone(summarize('')['p95_ms_nearest_rank'])
        report = summarize('bad\n{"status":200,"duration_ms":10}\n{"status":500,"duration_ms":100}\n{"status":200,"duration_ms":-1}')
        self.assertEqual(report['requests'], 2)
        self.assertEqual(report['skipped_lines'], 2)
        self.assertEqual(report['server_error_rate'], .5)
        self.assertEqual(report['p95_ms_nearest_rank'], 100)
