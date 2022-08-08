from pydantic import BaseModel
from typing import Optional

class EcryptMessage(BaseModel):
    message : str

    class Config:
        orm_mode = True
    

class decrypt_data_detail(BaseModel):
    expired_date :Optional[str]
    customer :str
    uuid :str

    class Config:
        orm_mode = True

class CreateAndUpdataAuthorizeMessage(BaseModel):
    decrypt_data: decrypt_data_detail
    time_range: int

    class Config:
        orm_mode = True