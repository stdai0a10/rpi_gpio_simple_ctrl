# Backend Initialization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立可在 Python 3.13 與 Raspberry Pi OS 32-bit Trixie 運行的 FastAPI 後端骨架，提供 lifespan、`GET /health`、`.env` 設定驗證與 socket-peer trusted-IP 限制。

**Architecture:** `app.main.create_app()` 組合 router、純 ASGI trusted-IP middleware 與由 factory 建立的 lifespan。Settings 在 lifespan 啟動時才從 repository root `.env` 載入，解析後以不可變 IP network sequence 放入 `app.state.settings`，讓 middleware 不必逐次解析設定。

**Tech Stack:** Python 3.13、FastAPI 0.141.1、Uvicorn 0.52.4、pydantic-settings 2.15.0、pytest 9.1.1、HTTPX 0.28.1、Black 26.5.1、isort 9.0.1、setuptools、pip

**Spec:** `docs/superpowers/specs/2026-09-11-backend-initialization-design.md`

## Global Constraints

- Python 必須符合 `>=3.13,<3.14`。
- Python 虛擬環境固定使用 `backend/.venv/`，且不得納入版本控制。
- `backend/pyproject.toml` 是唯一 Python project 與直接相依套件來源；移除空白的 `backend/requirements.txt`。
- Runtime dependencies 固定為 `fastapi==0.141.1`、`uvicorn==0.52.4`、`pydantic-settings==2.15.0`。
- `dev` dependencies 固定為 `pytest==9.1.1`、`httpx==0.28.1`、`black==26.5.1`、`isort==9.0.1`。
- 不使用 `fastapi[standard]`、`uvicorn[standard]`、lock file、constraints file 或 `.python-version`。
- 本階段不加入 GPIO、pigpio client、fake adapter、JSON 業務設定、YAML、SQLite、auth、CORS、systemd、CI/CD 或 pre-commit。
- `TRUSTED_IP_RANGES` 是唯一應用程式設定；未設定或整體空白時預設為 `127.0.0.1/32,::1/128`。
- 非空但無法解析的 network 設定必須讓 lifespan 啟動失敗，不得靜默退回預設值。
- 來源限制只相信 ASGI `scope["client"]`；Uvicorn 一律加上 `--no-proxy-headers`。
- `/health`、`/docs`、`/redoc`、`/openapi.json` 全部受 trusted-IP middleware 限制。
- `/health` 成功回應固定為 `200` 與 `{"status":"ok"}`；拒絕回應固定為 `403` 與 `{"detail":"Forbidden"}`。
- 每個行為都依 `docs/development-process.md` 先測試、再最小實作，並在 Green 後依序執行 isort、Black 與相關測試。
- 不讀取或重用目前 `backend/app/` 內容；實作時只在驗證絕對路徑後清除並重建該目錄。
- 保留不在範圍內的 `frontend/.prettierrc` 與 `frontend/eslint.config.js`。
- Linux 與 Raspberry Pi 未實際執行的檢查只能列為待驗證，不得宣稱通過。

---

## File Map

| 路徑 | 動作 | 責任 |
|---|---|---|
| `backend/pyproject.toml` | Create | 專案中繼資料、runtime/dev dependencies、Black 與 isort 設定 |
| `backend/requirements.txt` | Delete | 移除重複且空白的相依套件來源 |
| `backend/app/__init__.py` | Recreate | Python package 標記 |
| `backend/app/main.py` | Recreate | `create_app()` 與 module-level `app` |
| `backend/app/api/__init__.py` | Recreate | API package 標記 |
| `backend/app/api/router.py` | Recreate | 聚合 health router |
| `backend/app/api/middleware/__init__.py` | Recreate | Middleware package 標記 |
| `backend/app/api/middleware/trusted_ip.py` | Recreate | socket-peer CIDR allowlist 純 ASGI middleware |
| `backend/app/api/routes/__init__.py` | Recreate | Routes package 標記 |
| `backend/app/api/routes/health.py` | Recreate | `GET /health` |
| `backend/app/core/__init__.py` | Recreate | Core package 標記 |
| `backend/app/core/settings.py` | Recreate | root `.env`、預設值與 CIDR parsing |
| `backend/app/core/lifespan.py` | Recreate | 延遲 Settings 載入與 app state |
| `backend/tests/conftest.py` | Create | 注入有效 Settings 的 FastAPI/TestClient fixtures |
| `backend/tests/core/test_settings.py` | Create | Settings 公開契約測試 |
| `backend/tests/api/routes/test_health.py` | Create | app factory、lifespan 與 health 公開契約測試 |
| `backend/tests/api/middleware/test_trusted_ip.py` | Create | trusted-IP HTTP 與 ASGI 邊界測試 |
| `.env.example` | Modify | loopback-only 安全範例 |
| `README.md` | Modify | 後端安裝、啟動、測試與格式化方式 |
| `AGENTS.md` | Modify | 可重現的後端開發指令與格式規範 |

## Execution Preflight

計畫建立時，`CONTEXT.md` 與 spec 已在 staged area；`backend/app/` 以及兩個 frontend 設定檔尚未追蹤。開始實作前必須重新查詢，因為使用者可能已改變工作樹。

- [ ] **Step 1: Read the governing documents before editing**

Run from repository root:

```powershell
Get-Content -Raw AGENTS.md
Get-Content -Raw docs\development-process.md
Get-Content -Raw docs\superpowers\specs\2026-09-11-backend-initialization-design.md
```

Expected: all three files are readable; the spec status is confirmed.

- [ ] **Step 2: Inspect staged, unstaged, and untracked boundaries**

```powershell
git -c safe.directory=G:/Works/github_com/rpi_gpio_simple_ctrl status --short
git -c safe.directory=G:/Works/github_com/rpi_gpio_simple_ctrl diff --cached --name-only
git -c safe.directory=G:/Works/github_com/rpi_gpio_simple_ctrl diff --name-only
```

Expected before any implementation commit: planning documents are either already committed or explicitly handled by the user. If unrelated paths remain staged, do not unstage or commit them automatically; stop before the first commit and request direction.

- [ ] **Step 3: Verify the exact destructive target without reading its contents**

```powershell
$workspacePath = [System.IO.Path]::GetFullPath((Get-Location).Path)
$expectedAppPath = [System.IO.Path]::GetFullPath((Join-Path $workspacePath 'backend\app'))
$resolvedAppPath = (Resolve-Path -LiteralPath 'backend\app').Path
if ($resolvedAppPath -ne $expectedAppPath) {
    throw "Refusing to clear unexpected path: $resolvedAppPath"
}
if (-not $resolvedAppPath.StartsWith(
    [System.IO.Path]::GetFullPath((Join-Path $workspacePath 'backend')),
    [System.StringComparison]::OrdinalIgnoreCase
)) {
    throw "Resolved app path is outside backend: $resolvedAppPath"
}
$resolvedAppPath
```

Expected exact output:

```text
G:\Works\github_com\rpi_gpio_simple_ctrl\backend\app
```

Do not enumerate or inspect files inside that directory.

---

### Task 1: Rebuild the Installable Backend Package

**Files:**
- Create: `backend/pyproject.toml`
- Delete: `backend/requirements.txt`
- Recreate: `backend/app/__init__.py`
- Recreate: `backend/app/api/__init__.py`
- Recreate: `backend/app/api/middleware/__init__.py`
- Recreate: `backend/app/api/routes/__init__.py`
- Recreate: `backend/app/core/__init__.py`

**Interfaces:**
- Consumes: Python 3.13 interpreter and pip.
- Produces: editable distribution `rpi-gpio-simple-ctrl-backend==0.1.0`, import package `app`, runtime dependencies, `dev` extra, Black/isort configuration.

- [ ] **Step 1: Clear only the verified `backend/app/` target**

Use the same PowerShell process and repeat the preflight path checks immediately before deletion:

```powershell
$workspacePath = [System.IO.Path]::GetFullPath((Get-Location).Path)
$backendPath = [System.IO.Path]::GetFullPath((Join-Path $workspacePath 'backend'))
$expectedAppPath = [System.IO.Path]::GetFullPath((Join-Path $backendPath 'app'))
$resolvedAppPath = (Resolve-Path -LiteralPath 'backend\app').Path
if ($resolvedAppPath -ne $expectedAppPath) {
    throw "Refusing to clear unexpected path: $resolvedAppPath"
}
if (-not $resolvedAppPath.StartsWith(
    $backendPath,
    [System.StringComparison]::OrdinalIgnoreCase
)) {
    throw "Resolved app path is outside backend: $resolvedAppPath"
}
Remove-Item -LiteralPath $resolvedAppPath -Recurse -Force
```

Expected: only `backend/app/` is removed. `backend/tests/`, repository root, `CONTEXT.md`, planning documents, and frontend files remain present.

- [ ] **Step 2: Create the package directories**

```powershell
New-Item -ItemType Directory -Force 'backend\app\api\middleware'
New-Item -ItemType Directory -Force 'backend\app\api\routes'
New-Item -ItemType Directory -Force 'backend\app\core'
```

Expected: the three directories exist under the newly recreated `backend/app/`.

- [ ] **Step 3: Create `backend/pyproject.toml`**

Create the file with exactly this content:

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "rpi-gpio-simple-ctrl-backend"
version = "0.1.0"
description = "FastAPI backend for Raspberry Pi GPIO Simple Controller"
requires-python = ">=3.13,<3.14"
dependencies = [
  "fastapi==0.141.1",
  "uvicorn==0.52.4",
  "pydantic-settings==2.15.0",
]

[project.optional-dependencies]
dev = [
  "pytest==9.1.1",
  "httpx==0.28.1",
  "black==26.5.1",
  "isort==9.0.1",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]

[tool.black]
target-version = ["py313"]

[tool.isort]
profile = "black"
```

- [ ] **Step 4: Create package marker files**

Create these files with the shown contents:

`backend/app/__init__.py`

```python
"""Raspberry Pi GPIO Simple Controller backend."""
```

`backend/app/api/__init__.py`

```python
"""HTTP API package."""
```

`backend/app/api/middleware/__init__.py`

```python
"""HTTP middleware package."""
```

`backend/app/api/routes/__init__.py`

```python
"""HTTP route package."""
```

`backend/app/core/__init__.py`

```python
"""Application core package."""
```

- [ ] **Step 5: Delete the obsolete package source**

Delete only the tracked empty file:

```powershell
Remove-Item -LiteralPath 'backend\requirements.txt'
```

Expected: `backend/requirements.txt` is deleted; no requirements or lock replacement is created outside `backend/pyproject.toml`.

- [ ] **Step 6: Install the editable development package**

If `backend/.venv/` does not exist, create it first:

```powershell
py -3.13 -m venv backend/.venv
```

Install from repository root:

```powershell
backend\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
```

Expected: pip exits `0` and installs the exact direct dependency versions declared in `backend/pyproject.toml`. Network access may require explicit execution approval.

- [ ] **Step 7: Verify package metadata and dependency consistency**

```powershell
backend\.venv\Scripts\python.exe -c "from importlib.metadata import version; assert version('rpi-gpio-simple-ctrl-backend') == '0.1.0'"
backend\.venv\Scripts\python.exe -m pip check
```

Expected: both commands exit `0`; `pip check` reports `No broken requirements found.`

- [ ] **Step 8: Format and verify the scaffold**

```powershell
backend\.venv\Scripts\python.exe -m isort backend/app
backend\.venv\Scripts\python.exe -m black backend/app
backend\.venv\Scripts\python.exe -m compileall backend/app
```

Expected: isort and Black exit `0`; compileall compiles each marker module without errors.

- [ ] **Step 9: Commit the package scaffold when commits are authorized**

```powershell
git add backend/pyproject.toml backend/requirements.txt backend/app/__init__.py backend/app/api/__init__.py backend/app/api/middleware/__init__.py backend/app/api/routes/__init__.py backend/app/core/__init__.py
git diff --cached --name-only
```

Expected staged paths are exactly the five package marker files, `backend/pyproject.toml`, and the deleted `backend/requirements.txt`. If any planning or frontend path appears, do not commit.

```powershell
git commit -m "chore(backend): initialize Python package"
```

---

### Task 2: Load and Validate Trusted IP Settings

**Files:**
- Create: `backend/app/core/settings.py`
- Test: `backend/tests/core/test_settings.py`

**Interfaces:**
- Consumes: `pydantic_settings.BaseSettings`, `pydantic_settings.NoDecode`, repository root `.env`, Python `ipaddress`.
- Produces: `IpNetwork = IPv4Network | IPv6Network`, `DEFAULT_TRUSTED_IP_RANGES: tuple[IpNetwork, ...]`, and `Settings.trusted_ip_ranges: tuple[IpNetwork, ...]`.

- [ ] **Step 1: Write the Settings contract tests before implementation**

Create `backend/tests/core/test_settings.py`:

```python
from ipaddress import ip_network
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.settings import Settings


LOOPBACK_NETWORKS = (
    ip_network("127.0.0.1/32"),
    ip_network("::1/128"),
)


@pytest.fixture(autouse=True)
def clear_trusted_ip_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TRUSTED_IP_RANGES", raising=False)
    monkeypatch.delenv("trusted_ip_ranges", raising=False)


def test_missing_trusted_ip_ranges_uses_loopback_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == LOOPBACK_NETWORKS


@pytest.mark.parametrize("value", ["", "   \t"])
def test_blank_trusted_ip_ranges_uses_loopback_defaults(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", value)

    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == LOOPBACK_NETWORKS


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("192.0.2.0/24", (ip_network("192.0.2.0/24"),)),
        ("2001:db8::/32", (ip_network("2001:db8::/32"),)),
        (
            "192.0.2.0/24, 2001:db8::/32",
            (ip_network("192.0.2.0/24"), ip_network("2001:db8::/32")),
        ),
    ],
)
def test_valid_trusted_ip_ranges_are_parsed(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
    expected: tuple[object, ...],
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", value)

    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == expected


@pytest.mark.parametrize("value", ["not-a-network", "192.0.2.0/24,"])
def test_invalid_nonblank_trusted_ip_ranges_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", value)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_os_environment_overrides_dotenv(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "TRUSTED_IP_RANGES=192.0.2.0/24\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("TRUSTED_IP_RANGES", "198.51.100.0/24")

    settings = Settings(_env_file=env_file)

    assert settings.trusted_ip_ranges == (ip_network("198.51.100.0/24"),)


def test_dotenv_ignores_unknown_keys(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "UNRELATED_FRONTEND_VALUE=kept-outside-settings\n"
        "TRUSTED_IP_RANGES=192.0.2.0/24\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.trusted_ip_ranges == (ip_network("192.0.2.0/24"),)


def test_environment_name_is_case_insensitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("trusted_ip_ranges", "192.0.2.0/24")

    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == (ip_network("192.0.2.0/24"),)
```

- [ ] **Step 2: Run the Settings tests to verify Red**

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests/core/test_settings.py -v
```

Expected: collection fails because `app.core.settings` does not exist. The failure must be limited to the missing implementation module.

- [ ] **Step 3: Implement the Settings model**

Create `backend/app/core/settings.py`:

```python
from ipaddress import IPv4Network, IPv6Network, ip_network
from pathlib import Path
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


IpNetwork = IPv4Network | IPv6Network
ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"
DEFAULT_TRUSTED_IP_RANGES: tuple[IpNetwork, ...] = (
    ip_network("127.0.0.1/32"),
    ip_network("::1/128"),
)
TrustedIpRanges = Annotated[tuple[IpNetwork, ...], NoDecode]


class Settings(BaseSettings):
    """Validated application settings."""

    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    trusted_ip_ranges: TrustedIpRanges = DEFAULT_TRUSTED_IP_RANGES

    @field_validator("trusted_ip_ranges", mode="before")
    @classmethod
    def parse_trusted_ip_ranges(cls, value: object) -> object:
        """Parse a comma-separated list while treating a blank value as default."""
        if not isinstance(value, str):
            return value

        if not value.strip():
            return DEFAULT_TRUSTED_IP_RANGES

        return tuple(ip_network(item.strip()) for item in value.split(","))
```

`NoDecode` is required because pydantic-settings otherwise attempts JSON decoding for tuple fields before the field validator receives the comma-separated string.

- [ ] **Step 4: Run the Settings tests to verify Green**

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests/core/test_settings.py -v
```

Expected: all Settings tests pass, including defaults, blank values, IPv4, IPv6, multiple networks, invalid input, source priority, unknown dotenv keys, and case-insensitive names.

- [ ] **Step 5: Format and rerun the Settings slice**

```powershell
backend\.venv\Scripts\python.exe -m isort backend/app backend/tests
backend\.venv\Scripts\python.exe -m black backend/app backend/tests
backend\.venv\Scripts\python.exe -m pytest backend/tests/core/test_settings.py -v
```

Expected: formatting commands exit `0`; the same Settings tests remain green.

- [ ] **Step 6: Commit the Settings slice when commits are authorized**

```powershell
git add backend/app/core/settings.py backend/tests/core/test_settings.py
git diff --cached --name-only
```

Expected staged paths are exactly the implementation and its test. If any other path appears, do not commit.

```powershell
git commit -m "feat(config): load trusted IP ranges"
```

---

### Task 3: Add the Application Lifecycle and Health Endpoint

**Files:**
- Create: `backend/app/core/lifespan.py`
- Create: `backend/app/api/routes/health.py`
- Create: `backend/app/api/router.py`
- Create: `backend/app/main.py`
- Create: `backend/tests/conftest.py`
- Test: `backend/tests/api/routes/test_health.py`

**Interfaces:**
- Consumes: `Settings`, `FastAPI`, `APIRouter`, context-managed `TestClient`.
- Produces: `create_lifespan(settings: Settings | None) -> Lifespan`, `GET /health`, `api_router`, `create_app(settings: Settings | None = None) -> FastAPI`, and module-level `app`.

- [ ] **Step 1: Create public-interface test fixtures**

Create `backend/tests/conftest.py`:

```python
from collections.abc import Iterator
from ipaddress import ip_network

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.main import create_app


@pytest.fixture
def loopback_settings() -> Settings:
    return Settings(
        trusted_ip_ranges=(
            ip_network("127.0.0.1/32"),
            ip_network("::1/128"),
        ),
        _env_file=None,
    )


@pytest.fixture
def application(loopback_settings: Settings) -> FastAPI:
    return create_app(loopback_settings)


@pytest.fixture
def client(application: FastAPI) -> Iterator[TestClient]:
    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as test_client:
        yield test_client
```

- [ ] **Step 2: Write lifecycle and health tests before implementation**

Create `backend/tests/api/routes/test_health.py`:

```python
import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.settings import Settings
from app.main import create_app


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


def test_importing_main_does_not_load_settings() -> None:
    environment = os.environ.copy()
    environment["TRUSTED_IP_RANGES"] = "not-a-network"

    result = subprocess.run(
        [sys.executable, "-c", "import app.main"],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_application_metadata(application: FastAPI) -> None:
    assert application.title == "Raspberry Pi GPIO Simple Controller"
    assert application.version == "0.1.0"


def test_lifespan_stores_injected_settings(
    application: FastAPI,
    loopback_settings: Settings,
) -> None:
    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ):
        assert application.state.settings is loopback_settings


def test_lifespan_rejects_invalid_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", "not-a-network")
    application = create_app()

    with pytest.raises(ValidationError):
        with TestClient(
            application,
            client=("127.0.0.1", 50000),
        ):
            raise AssertionError("Invalid settings unexpectedly started the app")


def test_health_returns_exact_liveness_response(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("path", ["/", "/api/v1", "/api/v1/health"])
def test_unplanned_routes_are_not_defined(
    client: TestClient,
    path: str,
) -> None:
    response = client.get(path)

    assert response.status_code == 404
```

- [ ] **Step 3: Run the lifecycle/health tests to verify Red**

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests/api/routes/test_health.py -v
```

Expected: collection fails because `app.main` does not exist. This is the expected missing-public-interface failure.

- [ ] **Step 4: Implement the lifespan factory**

Create `backend/app/core/lifespan.py`:

```python
import logging
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.core.settings import Settings


logger = logging.getLogger(__name__)
Lifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_lifespan(settings: Settings | None = None) -> Lifespan:
    """Create an application lifespan with optional injected settings."""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        active_settings = settings if settings is not None else Settings()
        application.state.settings = active_settings
        logger.info("Application started")
        try:
            yield
        finally:
            logger.info("Application stopped")

    return lifespan
```

- [ ] **Step 5: Implement the health route and router aggregation**

Create `backend/app/api/routes/health.py`:

```python
from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Report that the ASGI application can serve requests."""
    return {"status": "ok"}
```

Create `backend/app/api/router.py`:

```python
from fastapi import APIRouter

from app.api.routes.health import router as health_router


api_router = APIRouter()
api_router.include_router(health_router)
```

- [ ] **Step 6: Implement the application factory and module-level app**

Create `backend/app/main.py`:

```python
from fastapi import FastAPI

from app.api.router import api_router
from app.core.lifespan import create_lifespan
from app.core.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Raspberry Pi GPIO Simple Controller",
        version="0.1.0",
        lifespan=create_lifespan(settings),
    )
    application.include_router(api_router)
    return application


app = create_app()
```

Creating the module-level `app` only creates a lifespan closure. It must not instantiate `Settings`; the subprocess test with an invalid environment proves this import boundary.

- [ ] **Step 7: Run the lifecycle and health tests to verify Green**

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests/api/routes/test_health.py -v
```

Expected: import, metadata, injected state, invalid-startup, exact health response, and unplanned-route tests all pass.

- [ ] **Step 8: Run the complete suite and format the slice**

```powershell
backend\.venv\Scripts\python.exe -m isort backend/app backend/tests
backend\.venv\Scripts\python.exe -m black backend/app backend/tests
backend\.venv\Scripts\python.exe -m pytest backend/tests -v
```

Expected: all Settings and lifecycle/health tests pass after formatting.

- [ ] **Step 9: Commit the runnable application slice when commits are authorized**

```powershell
git add backend/app/core/lifespan.py backend/app/api/routes/health.py backend/app/api/router.py backend/app/main.py backend/tests/conftest.py backend/tests/api/routes/test_health.py
git diff --cached --name-only
```

Expected staged paths are exactly the six paths listed above. If any other path appears, do not commit.

```powershell
git commit -m "feat(backend): add health endpoint"
```

---

### Task 4: Restrict HTTP Requests by Socket Peer

**Files:**
- Create: `backend/app/api/middleware/trusted_ip.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/api/middleware/test_trusted_ip.py`

**Interfaces:**
- Consumes: `scope["client"]`, `scope["app"].state.settings`, `Settings.trusted_ip_ranges`, Starlette ASGI types.
- Produces: `TrustedIPMiddleware(app: ASGIApp)`, pass-through for non-HTTP scopes, fixed JSON `403` for missing/invalid/untrusted peers.

- [ ] **Step 1: Write trusted-IP HTTP and ASGI tests before implementation**

Create `backend/tests/api/middleware/test_trusted_ip.py`:

```python
import asyncio
import json
from ipaddress import ip_network
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from starlette.types import Message, Receive, Scope, Send

from app.api.middleware.trusted_ip import TrustedIPMiddleware
from app.core.settings import Settings
from app.main import create_app


def build_settings(*ranges: str) -> Settings:
    return Settings(
        trusted_ip_ranges=tuple(ip_network(value) for value in ranges),
        _env_file=None,
    )


def build_http_scope(client_address: object) -> Scope:
    application = SimpleNamespace(
        state=SimpleNamespace(
            settings=build_settings("127.0.0.1/32"),
        )
    )
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/health",
        "raw_path": b"/health",
        "query_string": b"",
        "root_path": "",
        "headers": [],
        "server": ("testserver", 80),
        "client": client_address,
        "state": {},
        "app": application,
    }


async def invoke_middleware(scope: Scope) -> tuple[bool, list[Message]]:
    downstream_called = False
    messages: list[Message] = []

    async def downstream(
        downstream_scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        nonlocal downstream_called
        downstream_called = True
        await send(
            {
                "type": "http.response.start",
                "status": 204,
                "headers": [],
            }
        )
        await send({"type": "http.response.body", "body": b""})

    async def receive() -> Message:
        return {
            "type": "http.request",
            "body": b"",
            "more_body": False,
        }

    async def send(message: Message) -> None:
        messages.append(message)

    middleware = TrustedIPMiddleware(downstream)
    await middleware(scope, receive, send)
    return downstream_called, messages


def assert_forbidden(messages: list[Message]) -> None:
    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 403
    assert messages[1]["type"] == "http.response.body"
    assert json.loads(messages[1]["body"]) == {"detail": "Forbidden"}


def test_allows_ipv4_socket_peer_inside_configured_network() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("192.0.2.10", 50000),
    ) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_allows_ipv6_socket_peer_inside_configured_network() -> None:
    application = create_app(build_settings("2001:db8::/32"))

    with TestClient(
        application,
        client=("2001:db8::10", 50000),
    ) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_denies_socket_peer_outside_configured_network() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get("/health")

    assert response.status_code == 403
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Forbidden"}


def test_x_forwarded_for_cannot_override_socket_peer() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get(
            "/health",
            headers={"X-Forwarded-For": "192.0.2.10"},
        )

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_untrusted_peer_is_denied_before_routing() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get("/route-that-does-not-exist")

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_missing_client_address_is_denied() -> None:
    scope = build_http_scope(("127.0.0.1", 50000))
    scope.pop("client")

    downstream_called, messages = asyncio.run(invoke_middleware(scope))

    assert downstream_called is False
    assert_forbidden(messages)


@pytest.mark.parametrize(
    "client_address",
    [None, (), ("not-an-ip", 50000)],
)
def test_invalid_client_address_is_denied(client_address: object) -> None:
    scope = build_http_scope(client_address)

    downstream_called, messages = asyncio.run(invoke_middleware(scope))

    assert downstream_called is False
    assert_forbidden(messages)


def test_non_http_scope_passes_through() -> None:
    scope: Scope = {
        "type": "lifespan",
        "asgi": {"version": "3.0"},
        "state": {},
    }

    downstream_called, messages = asyncio.run(invoke_middleware(scope))

    assert downstream_called is True
    assert messages[0]["status"] == 204


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_documentation_routes_are_denied_to_untrusted_peers(path: str) -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get(path)

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_documentation_routes_are_available_to_trusted_peers(path: str) -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("192.0.2.10", 50000),
    ) as client:
        response = client.get(path)

    assert response.status_code == 200
```

- [ ] **Step 2: Run middleware tests to verify Red**

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests/api/middleware/test_trusted_ip.py -v
```

Expected: collection fails because `app.api.middleware.trusted_ip` does not exist. No production middleware should be present yet.

- [ ] **Step 3: Implement the pure ASGI middleware**

Create `backend/app/api/middleware/trusted_ip.py`:

```python
import logging
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import cast

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.settings import Settings


logger = logging.getLogger(__name__)
IpAddress = IPv4Address | IPv6Address


class TrustedIPMiddleware:
    """Allow HTTP requests only when the socket peer is in a trusted network."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        source_address = self._source_address(scope)
        application = cast(FastAPI, scope["app"])
        settings: Settings = application.state.settings

        if source_address is not None and self._is_trusted(
            source_address,
            settings,
        ):
            await self.app(scope, receive, send)
            return

        source_label = (
            str(source_address)
            if source_address is not None
            else "<missing-or-invalid>"
        )
        logger.warning(
            "Blocked request from %s: %s %s",
            source_label,
            scope.get("method", "UNKNOWN"),
            scope.get("path", ""),
        )
        response = JSONResponse(
            status_code=403,
            content={"detail": "Forbidden"},
        )
        await response(scope, receive, send)

    @staticmethod
    def _source_address(scope: Scope) -> IpAddress | None:
        client = scope.get("client")
        if not isinstance(client, (tuple, list)) or not client:
            return None

        host = client[0]
        if not isinstance(host, str):
            return None

        try:
            return ip_address(host)
        except ValueError:
            return None

    @staticmethod
    def _is_trusted(address: IpAddress, settings: Settings) -> bool:
        return any(
            address.version == network.version and address in network
            for network in settings.trusted_ip_ranges
        )
```

The warning contains only source-address status, method, and path. Do not add headers, query strings, body content, or full Settings data.

- [ ] **Step 4: Register the middleware for all routes**

Modify `backend/app/main.py` to this final content:

```python
from fastapi import FastAPI

from app.api.middleware.trusted_ip import TrustedIPMiddleware
from app.api.router import api_router
from app.core.lifespan import create_lifespan
from app.core.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Raspberry Pi GPIO Simple Controller",
        version="0.1.0",
        lifespan=create_lifespan(settings),
    )
    application.add_middleware(TrustedIPMiddleware)
    application.include_router(api_router)
    return application


app = create_app()
```

- [ ] **Step 5: Run middleware tests to verify Green**

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests/api/middleware/test_trusted_ip.py -v
```

Expected: IPv4, IPv6, deny, spoofed header, missing/invalid client, non-HTTP pass-through, and documentation-route tests all pass.

- [ ] **Step 6: Run the complete suite and format the slice**

```powershell
backend\.venv\Scripts\python.exe -m isort backend/app backend/tests
backend\.venv\Scripts\python.exe -m black backend/app backend/tests
backend\.venv\Scripts\python.exe -m pytest backend/tests -v
```

Expected: all Settings, lifecycle, health, and trusted-IP tests pass after formatting.

- [ ] **Step 7: Commit the trusted-IP slice when commits are authorized**

```powershell
git add backend/app/api/middleware/trusted_ip.py backend/app/main.py backend/tests/api/middleware/test_trusted_ip.py
git diff --cached --name-only
```

Expected staged paths are exactly the middleware, application composition change, and middleware test. If any other path appears, do not commit.

```powershell
git commit -m "feat(backend): restrict trusted IPs"
```

---

### Task 5: Document and Verify the Backend Workflow

**Files:**
- Modify: `.env.example`
- Modify: `README.md`
- Modify: `AGENTS.md:21-39`
- Modify: `AGENTS.md:57`

**Interfaces:**
- Consumes: all runnable commands and behavior produced by Tasks 1–4.
- Produces: safe root environment example, three platform run profiles, repository instructions matching actual commands, and fresh Windows verification evidence.

- [ ] **Step 1: Add the safe environment example**

Replace `.env.example` with exactly:

```dotenv
TRUSTED_IP_RANGES=127.0.0.1/32,::1/128
```

- [ ] **Step 2: Replace `README.md` with runnable backend documentation**

Use this content:

````markdown
# RPI_GPIO_SIMPLE_CTRL

簡易的 Raspberry Pi GPIO 控制器。目前後端初始化階段提供 FastAPI 存活檢查與可信任來源 IP 限制；GPIO 控制將於後續階段加入。

## 技術框架

- 前端：Vue.js
- 後端：Python 3.13、FastAPI、Uvicorn
- 後端設定：pydantic-settings 與根目錄 `.env`
- 後端測試：pytest
- Python 格式化：isort、Black

## 後端需求

- Python `>=3.13,<3.14`
- pip
- Raspberry Pi 正式目標：Raspberry Pi OS 32-bit Trixie

Python 虛擬環境固定使用 `backend/.venv/`。

## 後端設定

應用程式從專案根目錄 `.env` 讀取：

```dotenv
TRUSTED_IP_RANGES=127.0.0.1/32,::1/128
```

未設定或留空時只允許 IPv4/IPv6 loopback。要讓區域網路裝置存取服務，請以實際可信任 CIDR 完整取代預設值，例如：

```dotenv
TRUSTED_IP_RANGES=192.0.2.0/24
```

請勿把示例網段直接當成實際部署設定。

## Windows 開發

```powershell
py -3.13 -m venv backend/.venv
backend\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

## Linux 開發

```shell
python3.13 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e "backend[dev]"
./backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

## Raspberry Pi 執行

```shell
python3 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e backend
./backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --no-proxy-headers
```

Raspberry Pi 不安裝 development extra、不使用 `--reload`，且本階段不提供 systemd unit。

## Health check

從允許的來源呼叫：

```shell
curl http://127.0.0.1:8000/health
```

成功回應：

```json
{"status":"ok"}
```

`/health` 只確認 ASGI application 可以回應，不檢查 GPIO 或外部資源。`/docs`、`/redoc` 與 `/openapi.json` 也受相同來源限制。

## 後端測試與檢查

Windows：

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests
backend\.venv\Scripts\python.exe -m compileall backend/app
backend\.venv\Scripts\python.exe -m isort --check-only --diff backend/app backend/tests
backend\.venv\Scripts\python.exe -m black --check --diff backend/app backend/tests
git diff --check
```

Linux：

```shell
./backend/.venv/bin/python -m pytest backend/tests
./backend/.venv/bin/python -m compileall backend/app
./backend/.venv/bin/python -m isort --check-only --diff backend/app backend/tests
./backend/.venv/bin/python -m black --check --diff backend/app backend/tests
git diff --check
```

自動修改格式時固定先執行 isort，再執行 Black：

```powershell
backend\.venv\Scripts\python.exe -m isort backend/app backend/tests
backend\.venv\Scripts\python.exe -m black backend/app backend/tests
```

## 開發流程

本專案採用 TDD（Test-Driven Development，測試驅動開發）。實作與審查方式請參閱[開發流程需求](docs/development-process.md)。
````

- [ ] **Step 3: Replace the obsolete backend command section in `AGENTS.md`**

Replace the content from `### 後端` through the line immediately before `### 前端` with:

````markdown
### 後端

`backend/pyproject.toml` 是後端唯一 Python 專案與直接相依套件來源。Python 必須符合 `>=3.13,<3.14`，虛擬環境固定使用 `backend/.venv/`。

Windows 安裝與啟動：

```powershell
py -3.13 -m venv backend/.venv
backend\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

Linux 開發環境：

```shell
python3.13 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e "backend[dev]"
./backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

Raspberry Pi runtime 只安裝必要套件並使用單一 worker：

```shell
python3 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e backend
./backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --no-proxy-headers
```

後端測試與檢查：

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests
backend\.venv\Scripts\python.exe -m compileall backend/app
backend\.venv\Scripts\python.exe -m isort --check-only --diff backend/app backend/tests
backend\.venv\Scripts\python.exe -m black --check --diff backend/app backend/tests
```

````

- [ ] **Step 4: Update the Python style paragraph in `AGENTS.md`**

Replace the current paragraph beginning with `Python 使用四個空白縮排` with:

```markdown
Python 使用四個空白縮排，YAML 與前端程式碼使用兩個空白；禁止使用 Tab。Python 遵循 PEP 8：模組、函式及變數使用 `snake_case`，類別使用 `PascalCase`，常數使用 `UPPER_SNAKE_CASE`。公開函式須加上型別提示，GPIO 存取應封裝於 `backend/app/services/`。函式 ID 使用小寫連字號格式，例如 `open-door`。Python imports 使用 isort 的 Black profile 排序，其他 Python 格式由 Black 處理；自動格式化時固定先執行 isort，再執行 Black。請避免無關的大範圍格式調整。
```

- [ ] **Step 5: Run the complete automated verification suite**

Run from repository root using the project interpreter:

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests -v
backend\.venv\Scripts\python.exe -m compileall backend/app
backend\.venv\Scripts\python.exe -m isort --check-only --diff backend/app backend/tests
backend\.venv\Scripts\python.exe -m black --check --diff backend/app backend/tests
backend\.venv\Scripts\python.exe -m pip check
git -c safe.directory=G:/Works/github_com/rpi_gpio_simple_ctrl diff --check
```

Expected: pytest reports zero failures, compileall reports no syntax errors, isort and Black report no changes required, pip reports no broken requirements, and Git reports no whitespace errors.

- [ ] **Step 6: Run a real Uvicorn health smoke test**

Use a hidden process and restore the caller's process environment afterward:

```powershell
$previousTrustedIpRanges = [Environment]::GetEnvironmentVariable(
    'TRUSTED_IP_RANGES',
    'Process'
)
[Environment]::SetEnvironmentVariable(
    'TRUSTED_IP_RANGES',
    '127.0.0.1/32,::1/128',
    'Process'
)
$server = Start-Process `
    -FilePath 'backend\.venv\Scripts\python.exe' `
    -ArgumentList @(
        '-m',
        'uvicorn',
        'app.main:app',
        '--host',
        '127.0.0.1',
        '--port',
        '8765',
        '--no-proxy-headers'
    ) `
    -PassThru `
    -WindowStyle Hidden
try {
    Start-Sleep -Seconds 2
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/health'
    if ($response.status -ne 'ok') {
        throw "Unexpected health response: $($response | ConvertTo-Json -Compress)"
    }
    $response | ConvertTo-Json -Compress
}
finally {
    if (-not $server.HasExited) {
        Stop-Process -Id $server.Id
        Wait-Process -Id $server.Id -ErrorAction SilentlyContinue
    }
    [Environment]::SetEnvironmentVariable(
        'TRUSTED_IP_RANGES',
        $previousTrustedIpRanges,
        'Process'
    )
}
```

Expected output:

```json
{"status":"ok"}
```

- [ ] **Step 7: Confirm scope boundaries and platform claims**

```powershell
git -c safe.directory=G:/Works/github_com/rpi_gpio_simple_ctrl status --short
git -c safe.directory=G:/Works/github_com/rpi_gpio_simple_ctrl diff --name-only
rg -n "pigpio|SIMULATE_GPIO|sqlite|yaml|systemd|CORSMiddleware" backend README.md AGENTS.md .env.example
```

Expected:

- No frontend path was modified by this implementation.
- No GPIO, fake-adapter, SQLite, YAML, systemd, auth, or CORS implementation was added.
- Documentation may mention excluded features only to state that they are not part of this phase.
- Windows is the only environment claimed as freshly verified unless Linux or Raspberry Pi commands were actually run and their output was recorded.

- [ ] **Step 8: Commit documentation after all checks pass and commits are authorized**

```powershell
git add .env.example README.md AGENTS.md
git diff --cached --name-only
```

Expected staged paths are exactly `.env.example`, `README.md`, and `AGENTS.md`. If any implementation, planning, or frontend path appears, do not commit.

```powershell
git commit -m "docs(backend): document service workflow"
```

## Raspberry Pi Follow-up Verification

These steps are not satisfied by Windows execution. Run them on the named Raspberry Pi image after transferring or checking out the completed implementation:

```shell
python3 --version
python3 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e backend
./backend/.venv/bin/python -m pip check
TRUSTED_IP_RANGES=127.0.0.1/32,::1/128 ./backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --no-proxy-headers
```

Expected prerequisites and observations:

- `python3 --version` reports Python 3.13.x.
- Runtime installation succeeds without installing the `dev` extra.
- Uvicorn starts one worker without reload.
- `curl http://127.0.0.1:8000/health` returns `{"status":"ok"}`.
- After setting the real trusted LAN CIDR in root `.env`, an allowed LAN client succeeds and an untrusted source receives the fixed `403` JSON response.
- Record exact installed package versions and command output before claiming Raspberry Pi compatibility verified.

## Reference Contracts

- Pydantic Settings uses `NoDecode` to let a field validator parse comma-separated complex values: <https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/#disabling-json-parsing>
- Pydantic environment variables override dotenv values: <https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/#dotenv-env-support>
- Starlette TestClient accepts an explicit `(host, port)` client address and runs lifespan when used as a context manager: <https://www.starlette.io/testclient/>
- FastAPI recommends context-managed TestClient for lifespan tests: <https://fastapi.tiangolo.com/advanced/testing-events/>
- Uvicorn provides `--no-proxy-headers`, which prevents forwarded headers from rewriting remote-address information before the ASGI app: <https://www.uvicorn.org/settings/>
