# from base import Base
from datetime import datetime, timedelta

from sqlalchemy import Integer, Column, String, DateTime, func, Boolean, ForeignKey

from sqlalchemy.orm import declarative_base, relationship

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
    invoice = relationship('InvoiceUser', back_populates='user', cascade='delete, all')


class InvoiceUser(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, index=True)
    rocket_id = Column(Integer, unique=True)
    expired_in = Column(Integer)
    url = Column(String)
    currency = Column(String(30))
    paid = Column(Boolean, default=False)
    valid_until = Column(DateTime, default=datetime.utcnow)
    delete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User", back_populates="invoice"
    )

    @property
    def valid_time_url(self):
        if self.valid_until > datetime.now():
            return True
        return False
