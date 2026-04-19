from fastapi import HTTPException

from schemas.scheme import URLCreate
from database import add_url, get_url

characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# generate code for short url
def generate_code(id: int) -> str:
    base = len(characters)
    code = ""
    
    while id > 0:
        code = characters[id % base] + code 
        id //= base
    
    return code or "0"

# add to db and return short url
def shorten_url(data: URLCreate) -> str:
    id = add_url(data.long_url)
    code = generate_code(id)
    short_url = f"https://mytiny.url/{code}"
    return short_url


# get long url from db and return it
def get_long_url(data: str) -> str:
    if not data:
        raise HTTPException(status_code=400, detail="Short code is empty")

    code = 0
    offset = 1
    for i in data[::-1]:
        try:
            digit = characters.index(i)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid short code") from exc

        code = code + digit * offset
        offset *= len(characters)

    try:
        long_url = get_url(code)
    except (KeyError, IndexError) as exc:
        raise HTTPException(status_code=404, detail="Short URL not found") from exc

    return long_url

    