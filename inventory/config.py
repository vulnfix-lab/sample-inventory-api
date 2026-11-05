"""환경변수에서 앱 설정을 읽는다."""

import os


def load_config() -> dict:
    """환경변수에서 Flask 설정 값을 읽는다. 필수 값이 없으면 바로 실패한다."""
    origins = os.environ.get("INVENTORY_ADMIN_ORIGINS", "")
    admin_origins = [o.strip() for o in origins.split(",") if o.strip()]
    if not admin_origins:
        raise RuntimeError("환경변수 INVENTORY_ADMIN_ORIGINS 가 필요합니다 (쉼표로 구분)")
    return {"ADMIN_ORIGINS": admin_origins}
