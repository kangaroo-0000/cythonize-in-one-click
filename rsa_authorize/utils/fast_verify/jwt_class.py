from typing import Optional
from pydantic import BaseModel

# 使用者資料，因為預設為回傳值，故不加入密碼
class User(BaseModel):
    username : str
    email : str

# 要回傳的 Token 型態（響應型態）
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None