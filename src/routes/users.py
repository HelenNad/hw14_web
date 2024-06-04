import pickle

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, status, Path, Query, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repository_users

router = APIRouter(prefix='/users', tags=['users'])
cloudinary.config(cloud_name=config.CLD_NAME, api_key=config.CLD_API_KEY, api_secret=config.CLD_API_SECRET, secure=True)


@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    The get_current_user function is a dependency that will be injected into the
        get_current_user endpoint. It uses the auth_service to retrieve the current user,
        and returns it if found.

    :param user: User: Pass the user object to the function
    :return: The user object that is stored in the database
    :doc-author: Trelent
    """
    return user


@router.patch("/avatar", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(file: UploadFile = File(), user: User = Depends(auth_service.get_current_user),
                           db: Session = Depends(get_db)):
    """
    The get_current_user function is a dependency that will be used by the
        get_current_user endpoint. It returns the current user, if any, based on
        their authentication token. If no user is found for the given token, an HTTPException
        with status code 401 (Unauthorized) will be raised.

    :param file: UploadFile: Get the file from the request body
    :param user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: A user object
    :doc-author: Trelent
    """
    public_id = f"Web21/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop="fill",
                                                              version=res.get("version"))
    user = await repository_users.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user
