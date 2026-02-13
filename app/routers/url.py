from fastapi import APIRouter
from schemas.scheme import URLCreate, URLResponse
from services.shorterer import shorten_url

router = APIRouter()

@router.post("/shorten", response_model=URLResponse, status_code=201)
def short(data: URLCreate):
    shortened =  shorten_url(data)
    return {"short_url": shortened, "long_url": data.long_url}

