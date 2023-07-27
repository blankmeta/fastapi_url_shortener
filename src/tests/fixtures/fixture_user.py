import os
from datetime import timedelta
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from auth.models import User
from auth.services import create_access_token
from db.db import async_session
from main import app


@pytest.fixture(scope='session')
async def auth_ac() -> AsyncGenerator[AsyncClient, None]:
    """Authenticated async client."""
    user_username = os.getenv('test_client_username', default='user')
    user_password = os.getenv('test_client_password', default='password')
    async with async_session() as db:
        db_obj = User(username=user_username, password=user_password)
        db.add(db_obj)

        await db.commit()
        await db.refresh(db_obj)

    access_token = create_access_token(
        data={"sub": user_username}, expires_delta=timedelta(seconds=30)
    )

    async with AsyncClient(
            app=app,
            base_url='http://127.0.0.1:8000',
            headers=(('Authorization', f'Bearer {access_token}'),)
    ) as auth_ac:
        yield auth_ac
