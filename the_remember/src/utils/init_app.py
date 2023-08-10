from fastapi import FastAPI

from the_remember.src.api.auth.view import auth_app
from the_remember.src.api.folders.view import folder_app
from the_remember.src.api.users.view import user_app


def init_app(app: FastAPI):
    app = init_routers(app)

    return app

def init_routers(app: FastAPI):
    app.include_router(user_app, prefix="/user")
    app.include_router(folder_app, prefix='/folder')
    app.include_router(auth_app, prefix='/auth')

    return app