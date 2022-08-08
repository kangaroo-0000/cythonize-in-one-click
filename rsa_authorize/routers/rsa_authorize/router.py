import copy
from datetime import datetime
import os
import sys
import traceback
import json
from fastapi import APIRouter, Response, Depends, Path
from routers.rsa_authorize.return_scheme import BaseResponse, DecryptResponse, EncryptResponse, AuthorizesResponse
from utils.logger import Logger
from utils.rsa.rsa_class import RSAUtil
from routers.rsa_authorize.input_scheme import CreateAndUpdataAuthorizeMessage, EcryptMessage
from apps.rsa_authorize.sql.sqlite_database import SessionLocal, engine
from apps.rsa_authorize.sql.sqlite_curd import Authorize, Session
import apps.rsa_authorize.sql.sqlite_models as models
from apps.rsa_authorize.rsa_record import add_authorize_time
from routers.rsa_authorize.swagger import *

# model DB init

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------------------------------------------


authorize_app = APIRouter(prefix="/authorize")

authorize_rsa_handler = RSAUtil()
authorize_rsa_handler.load_key('private', os.getenv("AUTHORIZE_PRIVATE_FILE"))
authorize_rsa_handler.load_key('public', os.getenv("CUSTOMER_PUBLIC_FILE"))


logger = Logger(__name__, os.getenv("log_path"))


# 接收密文 API


@authorize_app.post(path="/decrypt", 
                    description=decrypt_message_description, 
                    tags=["authorize"], 
                    responses={
                        400: {
                            "model": BaseResponse,
                            "description": "Fail Response"
                        },
                        200: {
                            "model": EncryptResponse,
                            "description": "Success Response",
                        },
                    })
def decrypt_message(request_data: EcryptMessage, response: Response):
    try:
        res = authorize_rsa_handler.descrypt(request_data.message)
        if(res):
            message = " 請求成功 "
            return DecryptResponse(status=True, detail=message, decrypt_message=json.loads(res))
        else:
            message = " RSA 解密失敗或返回空值，請聯繫相關單位了解詳情"
            response.status_code = 400
            return BaseResponse(status=False, detail=message)
    except:
        message = " RSA 解密過程發生錯誤，請聯繫相關單位了解詳情"
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        response.status_code = 400
        return BaseResponse(status=False, detail=message)

@authorize_app.get(path='/get-authoizes',
                   description = '### get-authoize ',
                   tags=['authorize'],
                   responses={
                        400: {
                            "model": BaseResponse,
                            "description": "Fail Response"
                        },
                        200: {
                            "model": AuthorizesResponse,
                            "description": "Success Response"
                        },
                   })
def get_authorizes(response: Response, db: Session = Depends(get_db)):
    try:
        auth = Authorize(db)
        authorize_data = auth.Get_Authorizes()
        message = "取得授權資料成功"
        return AuthorizesResponse(status=True, detail=message, authorize_list=authorize_data)
    except:
        message = " 取得授權過程發生錯誤，請聯繫相關單位了解詳情 "
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        response.status_code = 400
        return BaseResponse(status=False, detail=message)

# 取得指定 UUID 資訊，並回傳秘密文

@authorize_app.get(path="/get-authoize/{UUID}",
                   description=get_authoize_description,
                   tags=["authorize"],
                   responses={
                        400: {
                            "model": BaseResponse,
                            "description": "Fail Response"
                        },
                        200: {
                            "model": EncryptResponse,
                            "description": "Success Response"
                        },
                   })
def get_authorize(response: Response, UUID: str = Path(..., title="the authoize id"), db: Session = Depends(get_db)):
    try:
        auth = Authorize(db)
        authorize_data = auth.Get_Authorize(UUID)
        if(authorize_data):
            temp = dict()
            temp['uuid'] = authorize_data.uuid
            temp['customer'] = authorize_data.customer
            temp['expired_date'] = authorize_data.expired_date.strftime(
                "%Y/%m/%d-%H:%M:%S")
            data = json.dumps(temp)
            authorize_data = authorize_rsa_handler.encrypt(data)
            message = " 查詢成功，返回加密訊息 "
            return EncryptResponse(status=True, detail=message, encrypt_message=authorize_data)
        else:
            message = " 查詢失敗，尚未有此 UUID 資訊 "
            response.status_code = 400
            return BaseResponse(status=False, detail=message)
    except:
        message = " 取得授權過程發生錯誤，請聯繫相關單位了解詳情 "
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        response.status_code = 400
        return BaseResponse(status=False, detail=message)

# 產生新授權 API


@authorize_app.post(path="/new-authoize", 
                    description=create_new_authoize_description, 
                    tags=["authorize"], 
                    responses={
                        400: {
                            "model": BaseResponse,
                            "description": "Fail Response"
                        },
                        200: {
                            "model": BaseResponse,
                            "description": "Success Response"
                        },
                    })
def create_new_authorize(request_data: CreateAndUpdataAuthorizeMessage, response: Response, db: Session = Depends(get_db)):
    try:
        origin_date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        new_deadline = add_authorize_time(
            current_data=origin_date, time_range=request_data.time_range)
        request_data.decrypt_data.expired_date = new_deadline
        new_data = copy.deepcopy(request_data.decrypt_data.dict())
        new_data['latest_update_time'] = datetime.now()
        auth = Authorize(db)
        res = auth.Create_New_Authorize(new_data)
        if(res):
            message = " 初始創建成功 "
            return BaseResponse(status=True, detail=message)
        else:
            message = " 創建失敗，或許此 UUID 已創建過，請使用 Updata 更新授權日期 "
            response.status_code = 400
            return BaseResponse(status=False, detail=message)
    except:
        message = " 創建新授權過程發生錯誤，請聯繫相關單位了解詳情"
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        response.status_code = 400
        return BaseResponse(status=False, detail=message)

# 更新授權 API


@authorize_app.patch(path="/updata-authoize", 
                     description=updata_new_authoize_description, 
                     tags=["authorize"], 
                     responses={
                        400: {
                            "model": BaseResponse,
                            "description": "Fail Response"
                        },
                        200: {
                            "model": BaseResponse,
                            "description": "Success Response"
                        },
                     })
def updata_new_authorize(request_data: CreateAndUpdataAuthorizeMessage, response: Response, db: Session = Depends(get_db)):
    try:
        origin_date = request_data.decrypt_data.expired_date
        new_deadline = add_authorize_time(
            current_data=origin_date, time_range=request_data.time_range)
        request_data.decrypt_data.expired_date = new_deadline
        new_data = copy.deepcopy(request_data.decrypt_data.dict())
        new_data['latest_update_time'] = datetime.now()
        new_data['latest_expired_date'] = datetime.strptime(
            origin_date, "%Y/%m/%d-%H:%M:%S")
        auth = Authorize(db)
        res = auth.Updata_Authorize_Single(
            request_data.decrypt_data.uuid, new_data)
        if(res):
            message = " 更新資料成功 "
            return BaseResponse(status=True, detail=message)
        else:
            message = " 更新失敗，請確認 UUID 等資訊正確 "
            response.status_code = 400
            return BaseResponse(status=False, detail=message)
    except:
        message = " 更新授權過程發生錯誤，請聯繫相關單位了解詳情 "
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        response.status_code = 400
        return BaseResponse(status=False, detail=message)

# 刪除授權 API


@authorize_app.delete(path="/delete-authoize/{UUID}", 
                      description=delete_authoize_description, 
                      tags=["authorize"], 
                      responses={
                        400: {
                            "model": BaseResponse,
                            "description": "Fail Response"
                        },
                        200: {
                            "model": BaseResponse,
                            "description": "Success Response"
                        },
                      })
def delete_authorize(response: Response, db: Session = Depends(get_db), UUID: str = Path(..., title="the authoize id")):
    try:
        auth = Authorize(db)
        res = auth.Delete_Authorize_Single(uuid=UUID)
        if(res):
            message = " 刪除資料成功 "
            return BaseResponse(status=True, detail=message)
        else:
            message = " 刪除失敗，請確認 UUID 等資訊正確 "
            response.status_code = 400
            return BaseResponse(status=False, detail=message)

    except:
        message = " 刪除授權過程發生錯誤，請聯繫相關單位了解詳情 "
        logger.debug(message)
        logger.debug(sys.exc_info())
        logger.debug(traceback.format_exc(1))
        response.status_code = 400
        return BaseResponse(status=False, detail=message)
