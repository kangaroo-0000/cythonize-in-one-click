from pydantic import BaseModel
from typing import List, Optional

from routers.rsa_authorize.input_scheme import decrypt_data_detail

class BaseResponse(BaseModel):
    status: bool
    detail: Optional[str]

class DecryptResponse(BaseResponse):
    decrypt_message : decrypt_data_detail

class EncryptResponse(BaseResponse):
    encrypt_message : str
    
class AuthorizesResponse(BaseResponse):
    authorize_list : List