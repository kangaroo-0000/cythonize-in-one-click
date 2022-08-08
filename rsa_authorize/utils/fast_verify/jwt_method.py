import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from .jwt_class import User, TokenData
from apps.rsa_authorize.sql.sqlite_curd import SuperUserHandler, TokenRecordHandler
# jwt 過期時間相關設定
from datetime import datetime, timedelta
# 密碼的 Hash 驗證
from passlib.context import CryptContext
# jwt 加解密
from jose import ExpiredSignatureError, jwt, JWTError
from routers.rsa_authorize.router import get_db

# 加密密鑰
SECRET_KEY = os.getenv("SECRET_KEY")
# jwt加密演算法
ALGORITHM = os.getenv("ALGORITHM")
# 過期時間
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# 指定 API 使用的 OAuth 認證方式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 指定加密方式
pwd_handler = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_handler.hash(password)


def verify_password(oringin_password, hashed_password):
    return pwd_handler.verify(oringin_password, hashed_password)


def get_user(db, username: str):
    # 檢查使用者存在與否
    user = SuperUserHandler(db)
    res = user.Get_User(username)
    return res


def authenticate_user(db, username: str, password: str):
    # 1.在資料庫尋找用戶
    user = get_user(db, username)
    if(not user):
        # 2.用戶不存在
        return False
    if(not verify_password(password, user.hashed_password)):
        # 3.密碼錯誤
        return False
    return user




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 只要沒有過期就會解密成功
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        db = next(get_db())
        token_handler = TokenRecordHandler(db)
        token_record = token_handler.Get_Token(username)
        if(token_record.jwt_token != token):
            raise
    except:
        raise credentials_exception
    try:
        if(not username):
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError as e:
        raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = next(get_db())
    user = get_user(db, username=token_data.username)
    if(not user):
        raise credentials_exception
    return user

# 可以在 User 新增值（user.disabled）來判斷是否屬於活躍用戶

def get_current_active_user(user: User = Depends(get_current_user)):
    return user

def create_or_update_jwt_record(to_encode, encode_jwt):
    db = next(get_db())
    token = TokenRecordHandler(db)
    data = {
        "username":to_encode.get("sub"),
        "jwt_token":encode_jwt
    }
    if(token.Get_Token(data.get("username"))):
        token.Updata_Token_Single(username=data.get("username"), data=data)
    else:
        token.Create_New_Token(data)

# 用戶通過驗證，生成 token
def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = None):
    # 另產生一個 dict data
    to_encode = data.copy()
    if expires_delta:
        # 有指定則使用指定時間
        expire = datetime.utcnow() + expires_delta
    else:
        # 無指定則延長 15 分鐘
        expire = datetime.utcnow() + timedelta(minutes=15)
    # 新增過期相關資訊
    to_encode.update({"exp": expire})
    # 加密 jwt 資訊
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    create_or_update_jwt_record(to_encode, encode_jwt)
    return encode_jwt
