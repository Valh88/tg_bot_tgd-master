# from base import Base
from sqlalchemy import Integer, Column, String, DateTime, func, Boolean

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telega_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String(10))
    language_code = Column(String(7))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_bot = Column(Boolean, default=False)
    have_premium = Column(Boolean, default=False)




