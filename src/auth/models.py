from sqlalchemy import Column, Integer, String, DateTime, func

from db.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    create_date = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f'{self.username}'
