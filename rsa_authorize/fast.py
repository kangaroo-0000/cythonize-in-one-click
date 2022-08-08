# load_dotenv一定要在最前
from dotenv import load_dotenv
load_dotenv(".env")
import uvicorn
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
# jwt 驗證
from fastapi.security import OAuth2PasswordRequestForm
from utils.fast_verify.jwt_method import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, oauth2_scheme 
from utils.fast_verify.jwt_class import Token, User
from routers.rsa_authorize.router import authorize_app, get_db
from apps.rsa_authorize.sql.sqlite_curd import Session, TokenRecordHandler
# swagger
from fast_swagger import *

app = FastAPI(openapi_tags=tags_metadata)

# jwt verify
# ------------------------------------------ #
@app.post('/token', response_model=Token, tags=["OAuth2 - JWT"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    user = authenticate_user(db, username, password)
    if(not user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type":"bearer"}

@app.get('/token', tags=["OAuth2 - JWT"])
async def logout_user(user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        token  = TokenRecordHandler(db)
        data = {
            "jwt_token":""
        }
        token.Updata_Token_Single(user.username,data=data)
        return True
    except:
        return False

@app.get('/user', tags=["OAuth2 - JWT"])
async def read_user(user: User = Depends(get_current_active_user)):
    return user

@app.get('/user/token', tags=["OAuth2 - JWT"])
async def read_token(token: str= Depends(oauth2_scheme)):
    return {"token":token}
# ------------------------------------------ #

app.include_router(authorize_app, dependencies=[Depends(get_current_active_user)])


if "__main__" == __name__:
    uvicorn.run(app, host="0.0.0.0", port=8081)
