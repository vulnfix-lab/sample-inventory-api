"""재고 API 테스트."""

ITEM = {"sku": "BOX-S", "name": "소형 박스", "quantity": 10}


def test_create_and_get_item(client):
    """품목을 등록하면 조회와 목록에 나온다."""
    assert client.post("/api/items", json=ITEM).status_code == 201

    assert client.get("/api/items/BOX-S").get_json() == ITEM
    assert client.get("/api/items").get_json() == {"items": [ITEM]}


def test_duplicate_sku_returns_409(client):
    """같은 SKU 를 다시 등록하면 409 다."""
    client.post("/api/items", json=ITEM)

    assert client.post("/api/items", json=ITEM).status_code == 409


def test_invalid_item_returns_400(client):
    """SKU 형식, 이름, 수량이 틀리면 400 이다."""
    for bad in [{**ITEM, "sku": "box s"}, {**ITEM, "name": ""}, {**ITEM, "quantity": -1},
                {**ITEM, "quantity": True}, {}]:
        assert client.post("/api/items", json=bad).status_code == 400


def test_unknown_item_returns_404(client):
    """없는 품목은 조회·조정 모두 404 다."""
    assert client.get("/api/items/NONE").status_code == 404
    assert client.post("/api/items/NONE/adjust", json={"delta": 1}).status_code == 404


def test_adjust_stock(client):
    """입고·출고로 재고가 바뀌고, 음수가 되는 출고는 409 다."""
    client.post("/api/items", json=ITEM)

    assert client.post("/api/items/BOX-S/adjust", json={"delta": 5}).get_json()["quantity"] == 15
    assert client.post("/api/items/BOX-S/adjust", json={"delta": -15}).get_json()["quantity"] == 0
    assert client.post("/api/items/BOX-S/adjust", json={"delta": -1}).status_code == 409
    assert client.post("/api/items/BOX-S/adjust", json={"delta": 0}).status_code == 400


def test_health(client):
    """헬스 체크는 200 이다."""
    assert client.get("/health").get_json() == {"status": "ok"}
