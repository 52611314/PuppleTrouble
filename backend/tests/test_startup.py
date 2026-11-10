from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app
from app.core.config import ROOT_DIR, Settings


def test_health_and_unknown_route_have_request_id():
    with TestClient(app) as client:
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        assert response.json()['data']['stage'] == 'bootstrap'
        assert response.json()['request_id'] == response.headers['X-Request-ID']
        missing = client.get('/api/v1/missing')
        assert missing.status_code == 404
        assert missing.json()['error']['code'] == 'HTTP_404'


def test_cors_allows_local_web_and_denies_other_origins():
    with TestClient(app) as client:
        for origin, status in [('http://localhost:5173', 200), ('https://unknown.invalid', 400)]:
            response = client.options('/api/v1/health', headers={'Origin': origin, 'Access-Control-Request-Method': 'GET'})
            assert response.status_code == status


def test_database_failure_is_reported_without_connection_secret():
    engine = MagicMock()
    engine.connect.side_effect = OperationalError('secret_database_url', {}, Exception('secret_password'))
    with patch('app.api.v1.endpoints.health.get_engine', return_value=engine):
        with TestClient(app) as client:
            response = client.get('/api/v1/health/ready')
    assert response.status_code == 503
    assert response.json()['error']['code'] == 'DATABASE_NOT_READY'
    assert 'secret_' not in response.text


def test_configuration_is_independent_of_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings = Settings(_env_file=None, storage_dir='storage')
    assert settings.storage_path == ROOT_DIR / 'storage'
