from fastapi import APIRouter, HTTPException, Response
from starlette.responses import JSONResponse
from validate_email import validate_email
from app.auth.schemas import SignupSchemaRequest, LoginSchemaRequest, AvailableSignupDataSchemeResponse, Message
from app.auth.security_utils import create_access_token, verify_password
import app.auth.db_api as db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={403: {"model": AvailableSignupDataSchemeResponse}},
)


@router.get("/available_signup_data", response_model=AvailableSignupDataSchemeResponse)
async def available_signup_data(nickname: str | None = None, email: str | None = None):
    if not validate_email(email):
        return JSONResponse(status_code=403, content="Invalid email.")

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
            message=message,
    )


@router.post("/signup")
async def sign_up(data: SignupSchemaRequest, response: Response):
    available = await available_signup_data(nickname=data.nickname, email=data.email)
    if not available.available:
        return JSONResponse(status_code=403, content=dict(available))

    db.add_user(data)
    access_token = create_access_token(data.email)
    response.set_cookie(key="token", value=access_token)
    return


@router.post("/login", responses={403: {"model": Message}})
async def log_in(data: LoginSchemaRequest, response: Response):
    user = db.select_user(nickname=None, email=data.email)
    if not user or not verify_password(data.password, user[0].password):
        raise HTTPException(status_code=403, detail="Wrong email or password.")

    access_token = create_access_token(data.email)
    response.set_cookie(key="token", value=access_token)
    return
