from apps.rsa_authorize.sql.sqlite_models import Authorize, SuperUser, TokenRecord
from utils.logger import Logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
import sys
import traceback

logger = Logger(__name__,os.getenv("log_path"))

class SQLlite_Handler():
    def __init__(self,db:Session):
        self.db = db

    # def set_log(self,logname):
    #     self.log = Logger(logname,os.getenv("log_path"))

class Authorize(SQLlite_Handler):
    table_class = Authorize

    def __init__(self, db: Session):
        super().__init__(db)

    # 取得所有
    def Get_Authorizes(self, skip: int=0, limit: int =1000):
        try:
            result = self.db.query(self.table_class).offset(skip).limit(limit).all()
            return result
        except:
            message = " 取得全部 Authorizes 失敗"
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
            

    # 取得單一
    def Get_Authorize(self, uuid: str) -> Authorize: 
        try:
            result =  self.db.query(self.table_class).filter(self.table_class.uuid == uuid).first()
            return result
        except:
            message = " 取得單獨 Authorizes 失敗"
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False


    # 新增
    def Create_New_Authorize(self, data:dict):
        try:
            db_target = self.table_class(**data)
            self.db.add(db_target)
            self.db.commit()
            self.db.refresh(db_target)
            return db_target
        except IntegrityError:
            message = (" This uuid is already in DB ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
        except:
            message = (" Create_New_Authorize is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
    
    # 刪除
    def Delete_Authorize_Single(self, uuid: str):
        try:
            db_target = self.db.query(self.table_class).filter(self.table_class.uuid == uuid).first()
            self.db.delete(db_target)
            self.db.commit()
            return True
        except:
            message = (" Delete_Authorize_Single is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

    # 修改
    def Updata_Authorize_Single(self, uuid: str, data:dict):
        try:
            db_target = self.db.query(self.table_class).filter(self.table_class.uuid == uuid).first()
            db_target.latest_update_time = data.get("latest_update_time")
            db_target.latest_expired_date = data.get("latest_expired_date")
            db_target.expired_date = data.get("expired_date")
            self.db.commit()
            self.db.refresh(db_target)
            return db_target
        except:
            message = (" Patch_Authorize_Single is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

class SuperUserHandler(SQLlite_Handler):
    table_class = SuperUser

    def __init__(self, db: Session):
        super().__init__(db)
    
    # 取得所有
    def Get_Users(self, skip: int = 0, limit: int = 0):
        try:
            return self.db.query(self.table_class).offset(skip).limit(limit).all()
        except:
            message = " 取得全部 Users 失敗"
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
            

    # 取得單一
    def Get_User(self, username: str) -> Authorize: 
        try:
            result =  self.db.query(self.table_class).filter(self.table_class.username == username).first()
            return result
        except:
            message = " 取得單獨 User 失敗"
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False


    # 新增
    def Create_New_User(self, data:dict):
        try:
            db_target = self.table_class(**data)
            self.db.add(db_target)
            self.db.commit()
            self.db.refresh(db_target)
            return db_target
        except IntegrityError:
            message = (" This uuid is already in DB ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
        except:
            message = (" Create_New_User is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
    
    # 刪除
    def Delete_User_Single(self, username: str):
        try:
            db_target = self.db.query(self.table_class).filter(self.table_class.username == username).first()
            self.db.delete(db_target)
            self.db.commit()
            return True
        except:
            message = (" Delete_User_Single is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

    # 修改
    def Updata_User_Single(self, username: str, data:dict):
        try:
            db_target = self.db.query(self.table_class).filter(self.table_class.username == username).first()
            db_target.hashed_password = data.get("hashed_password")
            db_target.email = data.get("email")
            self.db.commit()
            self.db.refresh(db_target)
            return db_target
        except:
            message = (" Patch_User_Single is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

class TokenRecordHandler(SQLlite_Handler):
    table_class = TokenRecord

    def __init__(self, db: Session):
        super().__init__(db)
    
    # 取得所有
    def Get_Tokens(self, skip: int = 0, limit: int = 0):
        try:
            return self.db.query(self.table_class).offset(skip).limit(limit).all()
        except:
            message = " 取得全部 Users 失敗"
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
            

    # 取得單一
    def Get_Token(self, username: str) -> Authorize: 
        try:
            result =  self.db.query(self.table_class).filter(self.table_class.username == username).first()
            return result
        except:
            message = " 取得單獨 User 失敗"
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False


    # 新增
    def Create_New_Token(self, data:dict):
        try:
            db_target = self.table_class(**data)
            self.db.add(db_target)
            self.db.commit()
            self.db.refresh(db_target)
            return db_target
        except IntegrityError:
            message = (" This uuid is already in DB ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
        except:
            message = (" Create_New_User is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
    
    # 刪除
    def Delete_Token_Single(self, username: str):
        try:
            db_target = self.db.query(self.table_class).filter(self.table_class.username == username).first()
            self.db.delete(db_target)
            self.db.commit()
            return True
        except:
            message = (" Delete_User_Single is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

    # 修改
    def Updata_Token_Single(self, username: str, data:dict):
        try:
            db_target = self.db.query(self.table_class).filter(self.table_class.username == username).first()
            db_target.jwt_token = data.get("jwt_token")
            self.db.commit()
            self.db.refresh(db_target)
            return db_target
        except:
            message = (" Patch_User_Single is Fail ")
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False