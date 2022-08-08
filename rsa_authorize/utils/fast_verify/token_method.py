# import os
# from fastapi import Header, HTTPException

# token_list = os.getenv("token_list")

# ACCESS_TOKEN_LIST = os.getenv("token_list").split(',')

# def verify_token(x_token: str = Header(...)):
#     if x_token not in ACCESS_TOKEN_LIST:
#         raise HTTPException(status_code=400, detail=" verify header invalid")

# def verify_key(x_key: str = Header(...)):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

