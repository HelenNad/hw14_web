from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserSchema


async def get_user_by_email(email: str, db: Session):
    """
    The get_user_by_email function takes an email address and returns the user associated with that email.
    If no such user exists, it returns None.

    :param email: str: Specify the email of the user we want to retrieve
    :param db: Session: Pass in the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserSchema, db: Session = Depends(get_db)):
    """
    The create_user function creates a new user in the database.

    :param body: UserSchema: Validate the request body
    :param db: Session: Pass in the database session
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(username=body.username,
                    email=body.email,
                    password=body.password,
                    avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session):
    """
    The update_token function updates the refresh token for a user.
        Args:
            user (User): The User object to update.
            token (str | None): The new refresh token to set for the user. If None, then no change is made and an error is logged instead.
            db (Session): A database session that will be used to commit changes if necessary.

    :param user: User: Get the user's id and email
    :param token: str | None: Specify the type of the token parameter
    :param db: Session: Access the database
    :return: The user object
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Get the email of the user
    :param db: Session: Pass in the database session
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar_url(email: str, url: str | None, db: Session) -> User:
    """
    The update_avatar_url function updates the avatar url of a user.

    :param email: str: Get the user by email
    :param url: str | None: Allow for the url to be nullable
    :param db: Session: Pass in the database session to the function
    :return: A user object, which is the same as what we get from our get_user_by_email function
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    db.refresh(user)
    return user
