from .models import User
from .database import create_db_and_tables, engine

from sqlmodel import Session, select
import secrets


def create_user(uname: str, passwd: str) -> str:
    """
    Creates user for the provided name and password
    Args:
        uname:str -- name of the user
        passwd:str -- password for the user
    """
    token: str = secrets.token_hex(nbytes=16)
    with Session(engine) as session:
        __user_obj = User(name=uname, passwd=passwd, token=token)

        session.add(__user_obj)
        session.commit()
        session.refresh(__user_obj)

        print(f"Created User By Name: {__user_obj.name}")
    return token


def update_user(uname: str) -> str:
    """
    Updates user token
    Args:
        name:str -- name of the user
    """
    token: str = secrets.token_hex(nbytes=16)
    with Session(engine) as session:
        statement = select(User).where(User.name == uname)
        users = session.exec(statement)
        user = users.one()
        user.token = token
        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Renewed Token for {user.name}")
    return token


def get_user(token: str) -> str:
    """
    Returns User for a given Token
    Args:
        token:str -- Valid Token
    Returns
        User name if found
    """
    if is_token_found(token):
        with Session(engine) as session:
            statement = select(User)
            users = session.exec(statement)
            user = users.first()
            if user is None:
                return f"No User Found"
            else:
                return user.name
    else:
        return f"Invalid Token"


def is_token_found(token: str):
    """
    Checks if token is found in table
    Returns True if token is found in the table else false
    Args:
        token:str: name of the user
    Returns
        True or False
    """
    with Session(engine) as session:
        statement = select(User).where(User.token == token)
        users = session.exec(statement)
        for user in users:
            return True
        return False
