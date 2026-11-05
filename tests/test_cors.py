"""CORS 허용 범위 테스트."""

import pytest

from inventory import create_app

ADMIN_ORIGIN = "https://admin.example.com"


def test_admin_origin_is_allowed_on_api(client):
    """관리자 화면 Origin 은 /api 응답에 허용 헤더가 붙는다."""
    resp = client.get("/api/items", headers={"Origin": ADMIN_ORIGIN})

    assert resp.headers.get("Access-Control-Allow-Origin") == ADMIN_ORIGIN


def test_other_origin_is_not_allowed(client):
    """다른 Origin 에는 허용 헤더가 붙지 않는다."""
    resp = client.get("/api/items", headers={"Origin": "https://evil.example.com"})

    assert "Access-Control-Allow-Origin" not in resp.headers


def test_cors_applies_only_to_api(client):
    """/api 밖의 경로에는 CORS 를 적용하지 않는다."""
    resp = client.get("/health", headers={"Origin": ADMIN_ORIGIN})

    assert "Access-Control-Allow-Origin" not in resp.headers


def test_preflight_for_admin_origin(client):
    """관리자 화면의 사전 요청(OPTIONS)에 POST 를 허용한다."""
    resp = client.options("/api/items", headers={
        "Origin": ADMIN_ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == ADMIN_ORIGIN
    assert "POST" in resp.headers.get("Access-Control-Allow-Methods", "")


def test_config_from_env(monkeypatch):
    """환경변수에서 허용 Origin 목록을 읽고, 없으면 바로 실패한다."""
    monkeypatch.setenv("INVENTORY_ADMIN_ORIGINS", f"{ADMIN_ORIGIN}, https://ops.example.com")
    assert create_app().config["ADMIN_ORIGINS"] == [ADMIN_ORIGIN, "https://ops.example.com"]

    monkeypatch.delenv("INVENTORY_ADMIN_ORIGINS")
    with pytest.raises(RuntimeError):
        create_app()
