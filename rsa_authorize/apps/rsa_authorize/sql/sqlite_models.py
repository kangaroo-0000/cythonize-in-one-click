import datetime
from apps.rsa_authorize.sql.sqlite_database import Base
from sqlalchemy import Column, VARCHAR, DATETIME


class Authorize(Base):
    __tablename__ = "authorize"

    uuid = Column(VARCHAR(512), primary_key=True, index=True)
    customer = Column(VARCHAR(512))
    create_time = Column(DATETIME, default=datetime.datetime.now())
    latest_update_time = Column(DATETIME)
    latest_expired_date = Column(DATETIME)
    expired_date = Column(DATETIME)


class SuperUser(Base):
    __tablename__ = "superuser"

    username = Column(VARCHAR(128), primary_key=True, index=True)
    hashed_password = Column(VARCHAR(128))
    email = Column(VARCHAR(128))


class TokenRecord(Base):
    __tablename__ = "tokenrecord"

    username = Column(VARCHAR(128), primary_key=True, index=True)
    jwt_token = Column(VARCHAR(256))
