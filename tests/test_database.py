import pytest

import database


class FakeCountersCollection:
    def __init__(self, value: int) -> None:
        self.value = value
        self.calls = []

    def find_one_and_update(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return {"value": self.value}


class FakeUrlsCollection:
    def __init__(self, document=None) -> None:
        self.document = document
        self.inserted = None
        self.find_args = None

    def insert_one(self, doc):
        self.inserted = doc

    def find_one(self, query, projection):
        self.find_args = (query, projection)
        return self.document


def test_get_next_url_id_uses_counter_collection(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_counters = FakeCountersCollection(value=5)
    monkeypatch.setattr(database, "counters_collection", fake_counters)

    result = database._get_next_url_id()

    assert result == 4
    assert fake_counters.calls
    args, kwargs = fake_counters.calls[0]
    assert args[0] == {"_id": "url_id"}
    assert args[1] == {"$inc": {"value": 1}}
    assert kwargs["upsert"] is True


def test_add_url_inserts_document(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_urls = FakeUrlsCollection()
    monkeypatch.setattr(database, "urls_collection", fake_urls)
    monkeypatch.setattr(database, "_get_next_url_id", lambda: 7)

    url_id = database.add_url("https://example.com")

    assert url_id == 7
    assert fake_urls.inserted == {"_id": 7, "long_url": "https://example.com"}


def test_get_url_negative_id_raises_key_error() -> None:
    with pytest.raises(KeyError):
        database.get_url(-1)


def test_get_url_missing_document_raises_key_error(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_urls = FakeUrlsCollection(document=None)
    monkeypatch.setattr(database, "urls_collection", fake_urls)

    with pytest.raises(KeyError):
        database.get_url(1)


def test_get_url_missing_long_url_raises_key_error(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_urls = FakeUrlsCollection(document={"_id": 1})
    monkeypatch.setattr(database, "urls_collection", fake_urls)

    with pytest.raises(KeyError):
        database.get_url(1)


def test_get_url_returns_string_value(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_urls = FakeUrlsCollection(document={"_id": 1, "long_url": 12345})
    monkeypatch.setattr(database, "urls_collection", fake_urls)

    result = database.get_url(1)

    assert result == "12345"
