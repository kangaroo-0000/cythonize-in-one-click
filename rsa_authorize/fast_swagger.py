# jwt swagger 說明
JWT_description="""
### 說明
- 藉由帳號密碼登入，取得 jwt token
- 在 Header `Authorization` 欄位中，設定 "Bearer \<token\>"
"""

# authorize swagger 說明
authorize_description="""
### 功能概述
- 透過 RSA-AES 加密，認證與紀錄授權過程，並最終決定是否更新授權日期

### 說明
- 一輪授權主要用到兩組共四個密鑰
1. 專案端
    - 專案端私鑰
    - 授權端公鑰
2. 授權端（ <- 此系統角色）
    - 授權端私鑰
    - 專案端公鑰
"""

tags_metadata=[
    {
        "name":"OAuth2 - JWT",
        "description":JWT_description
    },
    {
        "name":"authorize",
        "description":authorize_description
    }
]