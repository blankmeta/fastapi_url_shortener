from fastapi.testclient import TestClient
from httpx import AsyncClient
from starlette import status

from main import app

client = TestClient(app)


class TestUrl:
    URL_EXAMPLE = 'https://some-url.com'
    HASHED_URL_EXAMPLE = '00a583dd1bed7bc6f3bbaf12e03f5fa4'
    HASHED_UNEXISTING_URL = 'aaa583dd1bed7bc6f3bbaf12e03f5f12'

    async def test_db_connection(self, ac: AsyncClient):
        url = app.url_path_for('ping_db')
        response = await ac.get(url)
        assert response.status_code == status.HTTP_200_OK

    async def test_create_short_url(self, ac: AsyncClient):
        url = app.url_path_for('shorten_url')
        response = await ac.post(url, json={
            'url': self.URL_EXAMPLE
        })

        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_existing_short_url(self, ac: AsyncClient):
        url = app.url_path_for('shorten_url')
        response = await ac.post(url, json={
            'url': self.URL_EXAMPLE
        })

        assert response.status_code == status.HTTP_409_CONFLICT

    async def test_redirect(self, ac: AsyncClient):
        url = app.url_path_for('get_original_url',
                               short_url=self.HASHED_URL_EXAMPLE)
        response = await ac.get(url)

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    async def test_not_found_url(self, ac: AsyncClient):
        url = app.url_path_for('get_original_url',
                               short_url=self.HASHED_UNEXISTING_URL)
        response = await ac.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_url(self, ac: AsyncClient):
        url = app.url_path_for('set_deleted',
                               short_url=self.HASHED_URL_EXAMPLE)
        response = await ac.post(url)

        assert response.status_code == status.HTTP_200_OK

    async def test_get_deleted_url(self, ac: AsyncClient):
        url = app.url_path_for('get_original_url',
                               short_url=self.HASHED_URL_EXAMPLE)
        response = await ac.get(url)

        assert response.status_code == status.HTTP_410_GONE
