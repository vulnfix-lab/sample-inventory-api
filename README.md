# sample-inventory-api

오픈소스 취약점 조치 Agent 시연용 **두 번째 테스트 대상 저장소**입니다.
작은 Flask 재고 API이고, poetry로 의존성을 관리합니다. 취약점이 알려진 실제 패키지의 과거 버전을 일부러 고정해 두었습니다.

> **주의: 취약한 의존성을 일부러 쓰는 앱입니다.** 외부에 띄우지 말고 로컬 테스트로만 씁니다.
> Dependabot security updates 는 꺼 둡니다(시연용 상태를 유지하기 위해).

## 구성

| 경로 | 역할 |
|---|---|
| `inventory/__init__.py` | 앱 팩토리, CORS 설정 |
| `inventory/routes.py` | 라우트 (`/health`, `/api/items`) |
| `inventory/store.py` | 메모리 재고 저장소 |
| `inventory/config.py` | 환경변수 설정 |
| `gunicorn.conf.py` | 운영 WSGI 서버 설정 |
| `tests/` | pytest 테스트 |

## 의존성

- `pyproject.toml`: 운영(main)과 개발(dev) 그룹 선언
- `poetry.lock`: 고정 버전
- `poetry.toml`: 가상환경을 저장소 안 `.venv` 에 만든다

## 설치와 테스트

Python 3.14, poetry 2.5 에서 확인했습니다.

```bash
poetry install --no-root
poetry run pytest
```

## 로컬 실행

```bash
export INVENTORY_ADMIN_ORIGINS=http://127.0.0.1:5173
poetry run flask --app "inventory:create_app()" run
```
