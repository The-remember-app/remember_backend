from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from the_remember.src.api.auth.view import auth_app
from the_remember.src.api.folders.view import folder_app
from the_remember.src.api.modules.view import module_app
from the_remember.src.api.sentences.view import sentence_app
from the_remember.src.api.terms.view import term_app
from the_remember.src.api.users.view import user_app
from the_remember.src.config.config import CONFIG


def init_app(app: FastAPI):
    app = init_routers(app)
    app = add_middlewares(app)
    app = add_events(app)
    return app


def init_routers(app: FastAPI):
    app.include_router(auth_app, prefix='/auth', tags=['Auth'])
    app.include_router(user_app, prefix="/user", tags=['Users entities'])
    app.include_router(folder_app, prefix='/folder', tags=['Folders entities'])
    app.include_router(module_app, prefix='/module', tags=['Module entities'])
    app.include_router(term_app, prefix='/term', tags=['Term entities'])
    app.include_router(sentence_app, prefix='/sentence', tags=['Sentence entities'])

    return app


def add_middlewares(app: FastAPI):
    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def add_events(app: FastAPI):
    async def db_dispose():
        await CONFIG.engine.dispose()


    app.add_event_handler('shutdown', db_dispose)

    return app


