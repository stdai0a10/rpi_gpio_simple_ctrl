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

> 驗證狀態：以下指令本次未在 Linux 環境實際執行，仍待平台驗證。

```shell
python3.13 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e "backend[dev]"
./backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

## Raspberry Pi 執行

> 驗證狀態：以下指令本次未在 Raspberry Pi 實機執行，完整相容性仍待目標映像與硬體驗證。

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
