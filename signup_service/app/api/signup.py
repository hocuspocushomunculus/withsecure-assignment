from xml.dom import NotFoundErr
from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from .be_db.db_api import (
    create_db_and_tables,
    create_user,
    update_user,
    get_user,
    is_token_found,
)

create_db_and_tables()
signup = APIRouter()


@signup.post("/signup", summary="Signup a new User")
async def signmeup(name: str, passwd: str):
    """
    Create a user with all the information:

    - **name**: name of the user
    - **passwd**: unique password for user to login
    """
    token = create_user(uname=name, passwd=passwd)
    return f"token: {token}\n Please save it. This is visible only once. If you forget please regenerate token"


@signup.patch(
    "/renew",
    responses={
        200: {"description": "OK"},
        409: {"description": "Duplicate Records"},
        404: {"description": "Not Found"},
    },
    summary="Renew Token for the user",
)
async def renew_token(name: str):
    """
    Renew Token for the user

    - **name**: name of the user whose token needs to be renewed
    """
    try:
        token = update_user(uname=name)
        return f"token: {token}\n Please save it. This is visible only once."
    except exc.MultipleResultsFound:
        raise HTTPException(409, "Duplicate Records found")
    except exc.NoResultFound:
        raise HTTPException(404, "User Not Found")
    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
        )
        raise HTTPException(400, "Bad Request")


@signup.get("/validate", summary="Validate provided Token is valid or not")
async def validate_token(token: str):
    """
    Validates if Token provided is valid or not. Returns True if valid or False if it is invalid

    - **name**: name of the user whose token needs to be renewed
    """
    return is_token_found(token)


@signup.get(
    "/user",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
    },
    summary="Get user information",
)
async def get_username(token: str):
    """
    Gets user information for the given token

    - **token**: Valid token for which user needs to be fetched
    """
    user = get_user(token)
    if user == "No User Found":
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=user)
    elif user == "Invalid Token":
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=user)
    return user
