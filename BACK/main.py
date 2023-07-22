import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from app.auth.jwt_bearer import JwtBearer
from app.schemas import SignupSchemaRequest, LoginSchemaRequest, UserSchemaResponse
from app.utils import create_access_token, verify_password
import app.db_api as db

app = FastAPI()


@app.get("/")
async def root():
    print(1234)
    return {"message": "Hello World"}


@app.get("/hello/{name}", dependencies=[Depends(JwtBearer())])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/available_signup_data")
async def available_signup_data(data: SignupSchemaRequest):
    user = db.select_user(nickname=data.nickname, email=data.email)
    if not user:
        return
    user = user[0]
    if user.nickname == data.nickname and user.email == data.email:
        raise HTTPException(status_code=406, detail="This name and email are already taken.")
    if user.nickname == data.nickname:
        raise HTTPException(status_code=406, detail="This name is already taken.")
    if user.email == data.email:
        raise HTTPException(status_code=406, detail="This email is already taken.")


@app.post("/signup")
async def sign_up(data: SignupSchemaRequest):
    await available_signup_data(data)
    db.add_user(data)
    return create_access_token(data.email)


@app.post("/login")
async def log_in(data: LoginSchemaRequest):
    user = db.select_user(nickname=None, email=data.email)
    if not user or not verify_password(data.password, user[0].password):
        raise HTTPException(status_code=406, detail="Wrong email or password.")
    return create_access_token(user[0].email)


@app.get("/get_users", response_model=list[UserSchemaResponse])
async def get_users():
    return db.select_all_users()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
