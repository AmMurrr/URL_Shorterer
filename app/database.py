
import os

from pymongo import MongoClient, ReturnDocument


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mytinyurl")
MONGO_URL_COLLECTION = os.getenv("MONGO_URL_COLLECTION", "urls")
MONGO_COUNTER_COLLECTION = os.getenv("MONGO_COUNTER_COLLECTION", "counters")


mongo_client = MongoClient(MONGO_URI)
database = mongo_client[MONGO_DB_NAME]
urls_collection = database[MONGO_URL_COLLECTION]
counters_collection = database[MONGO_COUNTER_COLLECTION]


def _get_next_url_id() -> int:
    counter = counters_collection.find_one_and_update(
        {"_id": "url_id"},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(counter["value"]) - 1


def add_url(long_url: str) -> int:
    url_id = _get_next_url_id()
    urls_collection.insert_one({"_id": url_id, "long_url": long_url})
    return url_id


def get_url(url_id: int) -> str:
    document = urls_collection.find_one({"_id": url_id}, {"long_url": 1})
    if document is None:
        raise KeyError("URL not found")
    return str(document["long_url"])