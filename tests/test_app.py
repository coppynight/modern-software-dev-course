import http.client
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

from app.domain import clean_title, extract_tasks
from app.server import handler_for
from app.store import Store


class DomainTests(unittest.TestCase):
    def test_markers_dedup_and_order(self):
        self.assertEqual(extract_tasks('- 读书\nTODO:跑步\n待办：读书\n闲聊\n* 写字'), ['读书', '跑步', '写字'])

    def test_empty(self):
        self.assertEqual(extract_tasks('  \n- \n闲聊'), [])

    def test_note_limits(self):
        for value in (None, 3, 'x' * 4001, '- ' + 'x' * 121):
            with self.subTest(value=str(value)[:20]), self.assertRaises(ValueError):
                extract_tasks(value)

    def test_title_boundary(self):
        self.assertEqual(clean_title(' 中 文 '), '中 文')
        self.assertEqual(len(clean_title('字' * 120)), 120)
        for value in ('', '   ', 1, '字' * 121):
            with self.subTest(value=str(value)[:20]), self.assertRaises(ValueError):
                clean_title(value)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'tasks.db'
        self.store = Store(self.path)

    def test_persistence_crud(self):
        task = self.store.add('读书')
        self.assertEqual(Store(self.path).list(), [task])
        edited = self.store.update(task['id'], {'done': True, 'title': '读完书'})
        self.assertTrue(edited['done'])
        self.assertEqual(edited['title'], '读完书')
        self.store.delete(task['id'])
        self.assertEqual(self.store.list(), [])

    def test_sql_looking_title_is_data(self):
        title = "x'); DROP TABLE tasks; --"
        self.store.add(title)
        self.assertEqual(self.store.list()[0]['title'], title)
        self.assertEqual(len(self.store.list()), 1)

    def test_bad_update_leaves_data_unchanged(self):
        task = self.store.add('原文')
        for changes in ({}, {'done': 'false'}, {'done': 1}, {'id': 4}, {'title': ''}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.store.update(task['id'], changes)
        self.assertEqual(self.store.list(), [task])

    def test_missing(self):
        with self.assertRaises(KeyError): self.store.delete(999)
        with self.assertRaises(KeyError): self.store.update(999, {'done': True})


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(Store(Path(cls.temp.name) / 'tasks.db')))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(); cls.temp.cleanup()

    def request(self, method, path, data=None, headers=None, raw=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_address[1], timeout=5)
        try:
            body = raw if raw is not None else (json.dumps(data).encode() if data is not None else None)
            conn.request(method, path, body, headers or {'Content-Type': 'application/json'})
            r = conn.getresponse(); value = r.read()
            return r.status, r.getheaders(), value
        finally:
            conn.close()

    def test_health_and_assets(self):
        for path in ('/health', '/', '/app.js', '/style.css'):
            status, headers, _ = self.request('GET', path)
            self.assertEqual(status, 200)
            self.assertIn('X-Request-ID', dict(headers))

    def test_crud_over_http(self):
        status, _, body = self.request('POST', '/api/tasks', {'title': '测试 HTTP'})
        self.assertEqual(status, 201); task_id = json.loads(body)['id']
        status, _, body = self.request('PATCH', f'/api/tasks/{task_id}', {'done': True})
        self.assertEqual(status, 200); self.assertTrue(json.loads(body)['done'])
        self.assertEqual(self.request('DELETE', f'/api/tasks/{task_id}')[0], 200)
        self.assertEqual(self.request('DELETE', f'/api/tasks/{task_id}')[0], 404)

    def test_extract_does_not_persist(self):
        before = self.request('GET', '/api/tasks')[2]
        status, _, body = self.request('POST', '/api/extract', {'note': '- 学测试'})
        self.assertEqual(status, 200); self.assertEqual(json.loads(body)['tasks'], ['学测试'])
        self.assertEqual(self.request('GET', '/api/tasks')[2], before)

    def test_input_contracts(self):
        for data in ([], {'title': ' '}, {'title': 4}, {'title': '好', 'admin': True}):
            self.assertEqual(self.request('POST', '/api/tasks', data)[0], 400)
        self.assertEqual(self.request('POST', '/api/tasks', raw=b'{')[0], 400)
        self.assertEqual(self.request('POST', '/api/tasks', raw=b'x' * 20001)[0], 413)
        self.assertEqual(self.request('POST', '/api/tasks', raw=b'{}', headers={'Content-Type': 'text/plain'})[0], 415)

    def test_cross_origin_rejected(self):
        self.assertEqual(self.request('POST', '/api/tasks', {'title': 'x'},
                         {'Content-Type': 'application/json', 'Origin': 'https://example.org'})[0], 403)

    def test_host_and_path_allowlist(self):
        self.assertEqual(self.request('GET', '/', headers={'Host': 'example.org'})[0], 403)
        for path in ('/../app/store.py', '/data/tasks.db', '/api/tasks/0', '/missing'):
            self.assertEqual(self.request('GET', path)[0], 404)


if __name__ == '__main__':
    unittest.main()
