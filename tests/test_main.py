import main


def test_app_title() -> None:
    assert main.app.title == "MyTinyURL"


def test_routes_registered() -> None:
    paths = {route.path for route in main.app.routes}

    assert "/short-url" in paths
    assert "/short-url/{data}" in paths
