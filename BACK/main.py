import uvicorn
from fastapi import FastAPI, HTTPException, Response, Request
from starlette.responses import JSONResponse

from app import auth, task
from app.auth.schemas import UserSchemaResponse
import app.auth.db_api as db


app = FastAPI()
app.include_router(auth.router)
app.include_router(task.router)


@app.get("/")
async def root():
    print(1234)
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/get_users", response_model=list[UserSchemaResponse])
async def get_users():
    return db.select_all_users()


@app.get("/get_cookies")
async def get_cookies(request: Request):
    return request.cookies.get("access_token")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
