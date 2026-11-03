"""Verify audio routes are absent while core endpoints remain accessible.
Uses the isolated SQLite integration fixture; never connects to PostgreSQL.
"""
from fastapi.testclient import TestClient
from test_integration import app


def test_retired_audio_endpoints_are_not_registered():
    paths = {r.path for r in app.routes}
    assert '/api/pronunciation' not in paths
    assert '/api/pronunciation/status' not in paths
    assert '/api/admin/audio' not in paths
    assert '/api/media' not in paths
    assert all('/api/media' not in path for path in paths)


def test_retired_audio_paths_return_404_and_learning_api_still_works():
    with TestClient(app) as client:
        for method, path in [
            ('get', '/api/pronunciation?lang=en&text=Hello'),
            ('post', '/api/pronunciation'),
            ('get', '/api/pronunciation/status'),
            ('post', '/api/admin/audio'),
            ('get', '/api/media/unused.mp3'),
        ]:
            assert getattr(client, method)(path).status_code == 404, path
        assert client.get('/api/health').status_code == 200
        languages = client.get('/api/languages')
        assert languages.status_code == 200
        assert {item['code'] for item in languages.json()} == {'en','hi','mr','gu','bn','ta','te','kn','ur','es'}
