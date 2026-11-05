"""테스트 공통 픽스처."""

import pytest

from inventory import create_app

ADMIN_ORIGIN = "https://admin.example.com"


@pytest.fixture
def app():
    """테스트 설정으로 앱을 만든다."""
    return create_app({"TESTING": True, "ADMIN_ORIGINS": [ADMIN_ORIGIN]})


@pytest.fixture
def client(app):
    """Flask 테스트 클라이언트."""
    return app.test_client()
