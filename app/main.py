from fastapi import FastAPI

from routers import url

app = FastAPI(title="MyTinyURL")

app.include_router(url.router)