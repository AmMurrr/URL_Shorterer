import pytest
from pydantic import ValidationError

from schemas.scheme import URLCreate, URLResponse


def test_url_create_accepts_string_url() -> None:
    payload = URLCreate(long_url="https://example.com")

    assert payload.long_url == "https://example.com"


def test_url_response_requires_short_url() -> None:
    with pytest.raises(ValidationError):
        URLResponse(long_url="https://example.com")
