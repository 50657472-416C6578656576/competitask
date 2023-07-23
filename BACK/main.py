import asyncio

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException, Response, Request
from starlette.responses import JSONResponse

from app.auth.jwt_bearer import JwtBearer
from app.schemas import SignupSchemaRequest, LoginSchemaRequest, UserSchemaResponse, Message, \
    AvailableSignupDataSchemeResponse
from app.utils import create_access_token, verify_password
import app.db_api as db

app = FastAPI()


@app.get("/")
async def root():
    print(1234)
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/available_signup_data", response_model=AvailableSignupDataSchemeResponse)
async def available_signup_data(nickname: str | None = None, email: str | None = None):
    user = db.select_user(nickname=nickname, email=email)
    if not user:
        return AvailableSignupDataSchemeResponse(available=True)
    user = user[0]
    if user.nickname == nickname and user.email == email:
        message = "These name and email are already taken."
    elif user.nickname == nickname:
        message = "This name is already taken."
    else:
        message = "This email is already taken."

    return AvailableSignupDataSchemeResponse(
            available=False,
            taken_email=user.email == email,
            taken_nickname=user.nickname == nickname,
            message=message
    )


@app.post("/signup", responses={403: {"model": AvailableSignupDataSchemeResponse}})
async def sign_up(data: SignupSchemaRequest, response: Response):
    available = await available_signup_data(nickname=data.nickname, email=data.email)
    if not available.available:
        return JSONResponse(status_code=403, content=dict(available))
    db.add_user(data)
    access_token = create_access_token(data.email)
    response.set_cookie(key="session_token", value=access_token)
    return


@app.post("/login", responses={403: {"model": AvailableSignupDataSchemeResponse}})
async def log_in(data: LoginSchemaRequest, response: Response):
    user = db.select_user(nickname=None, email=data.email)
    if not user or not verify_password(data.password, user[0].password):
        raise HTTPException(status_code=403, detail="Wrong email or password.")
    access_token = create_access_token(data.email)
    response.set_cookie(key="session_token", value=access_token)
    return


@app.get("/get_users", response_model=list[UserSchemaResponse])
async def get_users():
    return db.select_all_users()


@app.get("/get_cookies")
async def get_cookies(request: Request):
    return request.cookies.get("session_token")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
