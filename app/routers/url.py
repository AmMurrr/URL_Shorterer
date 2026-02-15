from fastapi import APIRouter
from schemas.scheme import URLCreate, URLResponse,URLGet
from services.shorterer import shorten_url, get_long_url

router = APIRouter()

# transform long url to short
@router.post("/create-url", response_model=URLResponse, status_code=201)
def short(data: URLCreate):
    shortened =  shorten_url(data)
    return {"short_url": shortened, "long_url": data.long_url}

# from short url get long
# fix bug when try
@router.get("/short-url",status_code=201)
def give_url(data: URLGet ):
   long_url = get_long_url(URLGet)
   return {"long_url": long_url}