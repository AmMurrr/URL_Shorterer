
from typing import Optional


# Make proper MongoDB
db = []

# add url to db
def add_url(long_url:str):
    db.append(long_url)
    id = len(db) - 1
    return id
