from schemas.scheme import URLCreate, URLGet
from database import add_url, db

# generate code for short url
def generate_code(id: int) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
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
def get_long_url(data: URLGet ):
    # decode
    pass