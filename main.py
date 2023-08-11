from datetime import datetime, timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from the_remember.src.utils.init_app import init_app

app = FastAPI()
app = init_app(app)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=10010, reload=True)
