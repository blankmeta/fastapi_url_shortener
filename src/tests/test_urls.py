from fastapi.testclient import TestClient
from starlette import status

from main import app

client = TestClient(app)

BASE_URL = '/api/v1'


class TestUrl:
    def test_db_connection(self, event_loop):
        response = client.get(BASE_URL + '/ping')

        assert response.status_code == status.HTTP_200_OK

    def test_create_short_url(self, event_loop):
        response = client.post(BASE_URL + '/', json={
            "url_path": "https://some-url.com"
        })

        assert response.status_code == status.HTTP_201_CREATED
