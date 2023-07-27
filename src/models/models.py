from sqlalchemy import (Integer, String, func, DateTime, ForeignKey, Boolean,
                        Column)
from sqlalchemy.orm import relationship

from db.db import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    hashed_url = Column(String)
    create_date = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_deleted = Column(Boolean, default=False)
    statistics = relationship('Statistics')

    def __repr__(self):
        return f'{self.url}'


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    url_id = Column(ForeignKey('urls.id'))
    url = relationship('Url', back_populates='statistics')
    ip = Column(String)
    redirect_datetime = Column(
        DateTime(timezone=True), server_default=func.now()
    )
