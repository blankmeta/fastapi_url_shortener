import os

from fastapi.testclient import TestClient
from httpx import AsyncClient
from starlette import status

from main import app

client = TestClient(app)


class TestUser:
    USER_USERNAME = 'username'
    USER_PASSWORD = 'password'

    async def test_user_create(self, ac: AsyncClient):
        """Test user creation."""
        url = app.url_path_for('create_user')
        payload = {
            'username': self.USER_USERNAME,
            'password': self.USER_PASSWORD
        }
        response = await ac.post(url, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_user_create_same_username(self, ac: AsyncClient):
        """Test create a user with existing username."""
        url = app.url_path_for('create_user')
        payload = {
            'username': self.USER_USERNAME,
            'password': self.USER_PASSWORD
        }
        response = await ac.post(url, json=payload)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {'detail': 'User already exist'}

    async def test_get_token(self, ac: AsyncClient):
        """Test receiving an access token."""
        url = app.url_path_for('login_for_access_token')
        payload = {
            'username': self.USER_USERNAME,
            'password': self.USER_PASSWORD
        }
        response = await ac.post(url, json=payload)
        assert response.status_code == status.HTTP_200_OK

    async def test_get_user(self, auth_ac: AsyncClient):
        """Test getting current user."""
        url = app.url_path_for('read_users_me')
        response = await auth_ac.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('username') == os.getenv(
            'test_client_username')
