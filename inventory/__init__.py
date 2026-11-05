"""샘플 재고 API 앱 팩토리."""

from flask import Flask
from flask_cors import CORS

from inventory.config import load_config
from inventory.routes import bp
from inventory.store import InventoryStore


def create_app(config: dict | None = None) -> Flask:
    """설정을 읽어 Flask 앱을 만들고 CORS 와 라우트를 붙인다."""
    app = Flask(__name__)
    app.config.update(config or load_config())
    app.extensions["inventory_store"] = InventoryStore()
    # 관리자 화면에서만 API 를 호출한다
    CORS(app, resources={r"/api/*": {"origins": app.config["ADMIN_ORIGINS"]}})
    app.register_blueprint(bp)
    return app
