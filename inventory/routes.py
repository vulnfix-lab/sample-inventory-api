"""재고 API 라우트."""

import re

from flask import Blueprint, current_app, jsonify, request

from inventory.store import DuplicateSkuError, InventoryStore, OutOfStockError

bp = Blueprint("inventory", __name__)

SKU_PATTERN = re.compile(r"^[A-Z0-9-]{1,32}$")


def _store() -> InventoryStore:
    """현재 앱의 재고 저장소를 꺼낸다."""
    return current_app.extensions["inventory_store"]


def _error(status: int, message: str):
    """오류 응답을 만든다."""
    return jsonify({"error": message}), status


def _int_field(body: dict, key: str) -> int | None:
    """본문에서 정수 필드를 꺼낸다. bool 이나 다른 타입이면 None."""
    value = body.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


@bp.get("/health")
def health():
    """헬스 체크."""
    return jsonify({"status": "ok"})


@bp.get("/api/items")
def list_items():
    """모든 품목을 돌려준다."""
    return jsonify({"items": _store().list()})


@bp.post("/api/items")
def create_item():
    """품목을 등록한다. 형식이 틀리면 400, SKU 가 겹치면 409."""
    body = request.get_json(silent=True) or {}
    sku, name, quantity = body.get("sku"), body.get("name"), _int_field(body, "quantity")
    if not isinstance(sku, str) or not SKU_PATTERN.fullmatch(sku):
        return _error(400, "sku 는 대문자·숫자·하이픈 1~32자입니다")
    if not isinstance(name, str) or not 1 <= len(name) <= 100:
        return _error(400, "name 은 1~100자입니다")
    if quantity is None or quantity < 0:
        return _error(400, "quantity 는 0 이상의 정수입니다")
    try:
        item = _store().add(sku, name, quantity)
    except DuplicateSkuError:
        return _error(409, "이미 등록된 sku 입니다")
    return jsonify(item), 201


@bp.get("/api/items/<sku>")
def get_item(sku: str):
    """품목 하나를 돌려준다. 없으면 404."""
    item = _store().get(sku)
    if item is None:
        return _error(404, "품목이 없습니다")
    return jsonify(item)


@bp.post("/api/items/<sku>/adjust")
def adjust_item(sku: str):
    """입고(+)·출고(-)로 재고를 조정한다. 재고가 음수가 되면 409."""
    body = request.get_json(silent=True) or {}
    delta = _int_field(body, "delta")
    if delta is None or delta == 0:
        return _error(400, "delta 는 0 이 아닌 정수입니다")
    try:
        item = _store().adjust(sku, delta)
    except KeyError:
        return _error(404, "품목이 없습니다")
    except OutOfStockError:
        return _error(409, "재고가 부족합니다")
    return jsonify(item)
