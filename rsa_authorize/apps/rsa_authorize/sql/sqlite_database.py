# 1、匯入 sqlalchemy 部分的包
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import getenv

# 2、宣告 database url
SQLALCHEMY_DATABASE_URL = 'sqlite:///{}'.format(getenv("rsa_authorize_db_path"))

# 3、建立 sqlalchemy 引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 4、建立一個 database 會話
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5、返回一個 ORM Model
Base = declarative_base()