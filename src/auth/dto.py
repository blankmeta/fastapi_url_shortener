from typing import Union

from pydantic import BaseModel
from pydantic.schema import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserDTO(BaseModel):
    username: str
    password: str


class UserResponseDTO(BaseModel):
    id: int
    username: str

    # create_date: str

    class Config:
        orm_mode = True


class UserInDB(UserDTO):
    hashed_password: str
