"""운영 WSGI 서버(gunicorn) 설정.

실행: gunicorn -c gunicorn.conf.py "inventory:create_app()"
"""

import os

bind = os.environ.get("INVENTORY_BIND", "127.0.0.1:8000")
workers = int(os.environ.get("INVENTORY_WORKERS", "2"))
# 앞단 리버스 프록시가 붙여 주는 X-Forwarded-* 헤더를 믿을 주소
forwarded_allow_ips = os.environ.get("INVENTORY_FORWARDED_ALLOW_IPS", "127.0.0.1")
accesslog = "-"
