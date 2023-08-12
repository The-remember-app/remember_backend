from datetime import datetime, timedelta
from typing import Annotated

import orjson
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

# load_dotenv()
# MY_ENV_VAR = os.getenv('')

class ConfigBuilder(object):
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']

    asyncpg_introspection_issue = dict(connect_args={'server_settings': {'jit': 'off'}})
    POSTGRES_CONNECTION_URL = URL.create(
        drivername="postgresql+asyncpg",
        **dict(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            username=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
    )

    # POSTGRES_CONNECTION_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # orjson_dumps = orjson_dumps  # FROM py objects TO str
    orjson_dumps = orjson.dumps  # FROM py objects TO bytes
    orjson_loads = orjson.loads  # FROM str/bytes  TO py objects

    engine = create_async_engine(
        POSTGRES_CONNECTION_URL,
        **asyncpg_introspection_issue,
        json_deserializer=orjson_loads,
        json_serializer=orjson_dumps,
        echo=True

    )


CONFIG = ConfigBuilder()
