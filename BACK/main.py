import uvicorn
from fastapi import FastAPI, Request

from app import auth, task


app = FastAPI()
app.include_router(auth.router)
app.include_router(task.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_cookies")
async def get_cookies(request: Request):
    return request.cookies.get("access_token")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
