import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from app.main import app


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.available = {"models": [{"name": "qwen3:4b"}]}

    def test_empty_text_rejected(self):
        self.assertEqual(self.client.post('/api/extract', json={"text": "  ", "model": "x"}).status_code, 422)

    def test_unknown_owner_and_deadline_preserved(self):
        reply = {"response": '{"tasks":[{"task":"Обновить инструкцию","owner":null,"deadline":null,"evidence":"Нужно обновить инструкцию"}]}'}
        with patch('app.services.ollama.ollama_request', AsyncMock(side_effect=[self.available, reply])):
            response = self.client.post('/api/extract', json={"text":"Нужно обновить инструкцию", "model":"qwen3:4b"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['result']['tasks'][0]['owner'])

    def test_fabricated_quote_rejected_after_retry(self):
        reply = {"response": '{"tasks":[{"task":"Отчёт","owner":null,"deadline":null,"evidence":"выдуманная цитата"}]}'}
        with patch('app.services.ollama.ollama_request', AsyncMock(side_effect=[self.available, reply, reply])) as call:
            response = self.client.post('/api/extract', json={"text":"Обсудили погоду", "model":"qwen3:4b"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(call.await_count, 3)

    def test_invalid_json_recovers(self):
        with patch('app.services.ollama.ollama_request', AsyncMock(side_effect=[self.available, {"response":"broken"}, {"response":'{"tasks":[]}'}])):
            response = self.client.post('/api/extract', json={"text":"Обсудили погоду", "model":"qwen3:4b"})
        self.assertEqual(response.json()['result']['tasks'], [])
        self.assertEqual(response.json()['attempts'], 2)


    def test_web_assets_are_served(self):
        for path in ['/', '/static/css/styles.css', '/static/js/app.js', '/static/js/api.js', '/static/js/ui.js']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        html = self.client.get('/').text
        self.assertIn('type="module"', html)
        self.assertNotIn('<style>', html)

    def test_unavailable_ollama_returns_readable_error(self):
        from app.services.errors import ServiceError
        with patch('app.services.ollama.ollama_request', AsyncMock(side_effect=ServiceError(503, 'Ollama недоступна'))):
            response = self.client.get('/api/models')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['detail'], 'Ollama недоступна')


if __name__ == '__main__':
    unittest.main()
