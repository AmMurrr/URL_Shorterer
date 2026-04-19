import pytest
from fastapi import HTTPException

from schemas.scheme import URLCreate
import services.shorterer as shorterer


def test_generate_code_zero_returns_zero() -> None:
    assert shorterer.generate_code(0) == "0"


def test_generate_code_rollover_base62() -> None:
    assert shorterer.generate_code(61) == "Z"
    assert shorterer.generate_code(62) == "10"


def test_shorten_url_uses_generated_code(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shorterer, "add_url", lambda _url: 62)
    payload = URLCreate(long_url="https://example.com")

    assert shorterer.shorten_url(payload) == "https://mytiny.url/10"


def test_get_long_url_decodes_and_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}

    def fake_get_url(code: int) -> str:
        captured["code"] = code
        return "https://example.com"

    monkeypatch.setattr(shorterer, "get_url", fake_get_url)

    assert shorterer.get_long_url("10") == "https://example.com"
    assert captured["code"] == 62


def test_get_long_url_empty_code_returns_400() -> None:
    with pytest.raises(HTTPException) as exc:
        shorterer.get_long_url("")

    assert exc.value.status_code == 400
    assert exc.value.detail == "Short code is empty"


def test_get_long_url_invalid_symbol_returns_400() -> None:
    with pytest.raises(HTTPException) as exc:
        shorterer.get_long_url("ab*")

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid short code"


def test_get_long_url_not_found_returns_404(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get_url(_code: int) -> str:
        raise KeyError("URL not found")

    monkeypatch.setattr(shorterer, "get_url", fake_get_url)

    with pytest.raises(HTTPException) as exc:
        shorterer.get_long_url("abc")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Short URL not found"
