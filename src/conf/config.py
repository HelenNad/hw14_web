from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'postgresql+psycopg2://postgres:11111@localhost:5432/aaaa'
    SECRET_KEY_JWT: str = "1234567890"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "postgres@mail.com"
    MAIL_PASSWORD: str = "postgres"
    MAIL_FROM: EmailStr = "postgres@mail.com"
    MAIL_PORT: int = 567234
    MAIL_SERVER: str = "postgres"
    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "abc"
    CLD_API_KEY: int = 326488457974591
    CLD_API_SECRET: str = "secret"

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        """
        The validate_algorithm function is a validator that ensures the algorithm
        attribute of the JWTConfig class is either HS256 or HS512. If it isn't, then
        a ValueError exception will be raised.

        :param cls: Pass the class that is being validated
        :param v: Any: Specify the type of the value that is passed in
        :return: The value of v
        :doc-author: Trelent
        """
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8") # noqa


config = Settings()
