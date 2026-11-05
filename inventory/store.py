"""재고 품목을 메모리에 보관하는 저장소."""

import threading


class DuplicateSkuError(Exception):
    """이미 등록된 SKU 다."""


class OutOfStockError(Exception):
    """재고가 음수가 되는 조정이다."""


class InventoryStore:
    """프로세스 메모리에 품목을 보관한다. 재시작하면 사라진다."""

    def __init__(self) -> None:
        self._items: dict[str, dict] = {}
        self._lock = threading.Lock()

    def add(self, sku: str, name: str, quantity: int) -> dict:
        """새 품목을 등록하고 돌려준다. SKU 가 겹치면 DuplicateSkuError."""
        with self._lock:
            if sku in self._items:
                raise DuplicateSkuError(sku)
            item = {"sku": sku, "name": name, "quantity": quantity}
            self._items[sku] = item
            return dict(item)

    def get(self, sku: str) -> dict | None:
        """SKU 로 품목을 찾는다. 없으면 None."""
        item = self._items.get(sku)
        return dict(item) if item else None

    def list(self) -> list[dict]:
        """모든 품목을 SKU 순서로 돌려준다."""
        return [dict(self._items[sku]) for sku in sorted(self._items)]

    def adjust(self, sku: str, delta: int) -> dict:
        """재고 수량을 delta 만큼 바꾼다. 없는 SKU 는 KeyError, 음수가 되면 OutOfStockError."""
        with self._lock:
            item = self._items[sku]
            if item["quantity"] + delta < 0:
                raise OutOfStockError(sku)
            item["quantity"] += delta
            return dict(item)
