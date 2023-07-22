from fastapi import FastAPI, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils import decode_token


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials and credentials.scheme == "Bearer":
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid Token!")

    @staticmethod
    def verify_jwt(jwt_token: str):
        return bool(decode_token(jwt_token))
