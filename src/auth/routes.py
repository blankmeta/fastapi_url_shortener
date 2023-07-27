from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.dto import UserDTO, Token, UserResponseDTO
from auth.repository import user_crud
from auth.services import authenticate_user, create_access_token, \
    get_current_active_user
from db.db import get_session

user_router = APIRouter()


@user_router.post("/token", response_model=Token)
async def login_for_access_token(
        # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user: UserDTO,
        db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(db, user.username,
                                   user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get('/users/me', response_model=UserResponseDTO)
async def read_users_me(
        current_user: Annotated[
            UserDTO, Depends(get_current_active_user)],
):
    return current_user


@user_router.post('/users/create', status_code=status.HTTP_201_CREATED)
async def create_user(
        user_obj: UserDTO,
        db: AsyncSession = Depends(get_session)
) -> UserResponseDTO:
    try:
        user = await user_crud.create(db=db, obj_in=user_obj)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='User already exist')
    return user
