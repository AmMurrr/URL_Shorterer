from schemas.scheme import URLCreate
from database import add_url, db, get_url

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
    code = 0
    offset = 1
    for i in data[::-1]:
        code = code + characters.index(i) * offset
        offset *= len(characters)

    long_url = get_url(code)
    return long_url

    