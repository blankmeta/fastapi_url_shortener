from datetime import datetime

from sqlalchemy import (Integer, String, func, DateTime, ForeignKey, Boolean,
                        Column)
from sqlalchemy.orm import Mapped, relationship, validates

from db.db import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url_path = Column(String)
    hashed_url_path = Column(String)
    create_date = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_deleted = Column(Boolean, default=False)
    statistics = relationship('Statistics')

    def __repr__(self):
        return f'{self.url_path}'


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    url_id = Column(ForeignKey('urls.id'))
    url = relationship('Url', back_populates='statistics')
    ip = Column(String)
    redirect_datetime = Column(
        DateTime(timezone=True), server_default=func.now()
    )
