from schemas.scheme import URLCreate
from database import add_url, db

def generate_code(id: int) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    base = len(characters)
    code = ""
    
    while id > 0:
        code = characters[id % base] + code
        id //= base
    
    return code or "0"

def shorten_url(data: URLCreate) -> str:
    id = add_url(data.long_url)
    code = generate_code(id)
    short_url = f"https://mytiny.url/{code}"
    return short_url