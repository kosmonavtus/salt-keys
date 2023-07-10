from fastapi import FastAPI
from app_salt_keys.routes.kyes import router


def app_salt_keys():
    app = FastAPI()
    app.include_router(router)
    return app


app = app_salt_keys()
