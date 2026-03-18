
from typing import Optional


# Make proper MongoDB
db = []

# add url to db
def add_url(long_url:str) -> int:
    db.append(long_url)
    id = len(db) - 1
    return id

def get_url(id:int) -> str:
    long_url = db[id]
    return long_url