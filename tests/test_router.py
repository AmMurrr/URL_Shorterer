from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest

import main
from routers import url as url_router


@pytest.fixture
def client() -> TestClient:
    return TestClient(main.app)


def test_create_short_url_returns_201(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(url_router, "shorten_url", lambda _data: "https://mytiny.url/abc")

    response = client.post("/short-url", json={"long_url": "https://example.com"})

    assert response.status_code == 201
    assert response.json() == {
        "short_url": "https://mytiny.url/abc",
        "long_url": "https://example.com",
    }


def test_get_long_url_returns_payload(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(url_router, "get_long_url", lambda _code: "https://example.com")

    response = client.get("/short-url/abc")

    assert response.status_code == 201
    assert response.json() == {"long_url": "https://example.com"}


def test_get_long_url_propagates_http_exception(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_get_long_url(_code: str) -> str:
        raise HTTPException(status_code=404, detail="Short URL not found")

    monkeypatch.setattr(url_router, "get_long_url", fake_get_long_url)

    response = client.get("/short-url/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "Short URL not found"}
