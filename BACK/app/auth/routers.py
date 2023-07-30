from fastapi import APIRouter, Response, Request
from jose import JWTError
from starlette.responses import JSONResponse
from validate_email import validate_email

from app.auth.db_api import select_user, add_user, select_all_users
from app.auth.schemas import SignupSchemaRequest, LoginSchemaRequest, AvailableSignupDataSchemaResponse, Message, \
    ValidationResult, UserSchemaResponse
from app.auth.security_utils import create_access_token, verify_password, decode_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/available_signup_data", response_model=AvailableSignupDataSchemaResponse)
async def available_signup_data(username: str | None = None, email: str | None = None):
    valid_email = ValidationResult(valid=True)
    valid_username = ValidationResult(valid=True)

    if email and not validate_email(email):
        valid_email.message = "Invalid email."
        valid_email.valid = False

    user = await select_user(username=username, email=email)
    if not user:
        return AvailableSignupDataSchemaResponse(email=valid_email, username=valid_username)

    if len(user) == 2 or (user[0][0].username == username and user[0][0].email == email):
        valid_email.message, valid_username.message = "This email is already taken.", "This username is already taken."
        valid_email.valid, valid_username.valid = False, False

    elif user[0][0].username == username:
        valid_username.message = "This name is already taken."
        valid_username.valid = False
    else:
        valid_email.message = "This email is already taken."
        valid_email.valid = False

    return AvailableSignupDataSchemaResponse(email=valid_email, username=valid_username)


@router.post("/signup", responses={403: {"model": AvailableSignupDataSchemaResponse}}, response_model=str)
async def sign_up(response: Response, data: SignupSchemaRequest):
    available = await available_signup_data(username=data.username, email=data.email)
    if not (available.email.valid and available.username.valid):
        return JSONResponse(status_code=403, content=available.dict())

    user = await add_user(data)

    access_token = create_access_token({"email": data.email, "user_id": user, "username": data.username})
    response.set_cookie(key="access_token", value=access_token)
    return True


@router.post("/login", responses={403: {"model": Message}}, response_model=bool)
async def log_in(response: Response, data: LoginSchemaRequest):
    user = await select_user(email=data.email)
    if not user or not verify_password(data.password, user[0][0].password):
        return JSONResponse(status_code=403, content=Message(message="Wrong email or password."))

    user = user[0][0]
    access_token = create_access_token({"email": data.email, "user_id": user.user_id, "username": user.username})
    response.set_cookie(key="access_token", value=access_token)
    return True


@router.get("/proper_token", response_model=UserSchemaResponse)
async def proper_token(request: Request):
    try:
        access_token = request.cookies.get("access_token")
        payload = decode_token(access_token)
    except JWTError:
        return None
    except AttributeError:
        return None
    return payload


@router.get("/get_signed_users", response_model=list[UserSchemaResponse])
async def get_signed_users():
    return await select_all_users()
