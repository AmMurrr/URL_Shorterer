from fastapi import FastAPI

from routers import url

app = FastAPI()

app.include_router(url.router)