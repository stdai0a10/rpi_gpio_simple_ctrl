# Backend Initialization Design Specification

**狀態：** 已確認，待建立實作計畫

**日期：** 2026-09-11

**適用範圍：** `backend/` 與必要的專案層級文件

## 1. 目的

本規格定義 Raspberry Pi GPIO Simple Control 專案第一階段後端骨架。完成後，專案應具備可啟動的 FastAPI 應用程式、存活檢查、設定驗證、可信任來源 IP 限制、自動化測試，以及可重現的安裝與開發指令。

本階段的目標是建立後續 GPIO Function 功能可依賴的穩定 HTTP 與設定基礎，不提前建立尚未使用的 GPIO、儲存或認證抽象。

## 2. 已知執行環境

- 正式硬體為 Raspberry Pi 1 Model B v2。
- 正式作業系統為官方映像檔「Raspberry Pi OS (32-bit), a port of Debian Trixie with Raspberry Pi Desktop」。
- Desktop 是目前驗證使用的映像版本，不代表服務需要圖形介面。
- Python 版本限制為 `>=3.13,<3.14`。
- 使用 pip 與位於 `backend/.venv/` 的虛擬環境。
- 正式環境由 Uvicorn 直接對可信任區域網路提供服務。
- 正式環境不使用 `--reload`，且只啟動一個 worker。
- 使用者已驗證目標環境可以安裝 FastAPI，也已驗證 `pigpiod` 可以運行；完整相容性仍以本規格所列精確版本在實機上的驗證結果為準。
- Legacy Bookworm、64-bit Raspberry Pi OS 及其他 Linux distribution 不在保證範圍內；一般 Linux 僅作為開發環境。

## 3. 本階段範圍

### 3.1 包含

- 使用 application factory 建立 FastAPI 應用程式。
- 使用 FastAPI lifespan 執行啟動與關閉流程。
- 提供 `GET /health` 存活檢查。
- 使用 `pydantic-settings` 從專案根目錄 `.env` 讀取設定。
- 驗證並套用 `TRUSTED_IP_RANGES`。
- 使用純 ASGI middleware 限制 HTTP 請求來源。
- 保留 FastAPI 內建 OpenAPI、Swagger UI 與 ReDoc。
- 使用 pytest 驗證公開 Settings 與 HTTP/ASGI 介面。
- 使用 Black 格式化 Python 程式碼。
- 使用 isort 排序 Python imports。
- 文件化 Windows、一般 Linux 與 Raspberry Pi 三種安裝及啟動方式。

### 3.2 不包含

- GPIO 或 `pigpio` client 程式碼。
- fake GPIO adapter 或 `SIMULATE_GPIO` 設定。
- GPIO 腳位、啟動狀態或關閉狀態。
- JSON 業務設定的載入、儲存或 API。
- YAML。
- SQLite。
- authentication 或 authorization。
- CORS。
- reverse proxy 或 forwarded-header 支援。
- systemd unit 或安裝腳本。
- CI/CD、GitHub Actions 或 pre-commit hook。
- `/` 首頁或 `/api/v1` 路由。
- Black 與 isort 以外的 formatter、linter、type checker 或其他品質工具。

## 4. 後續領域方向

後續階段會讓使用者操作具名的 **GPIO Function**，例如 `door-lock`，再由 JSON 設定把 Function ID 映射到 BCM GPIO Number。HTTP 請求不會直接執行任意腳本或任意 pin command。

本階段只保留足以支援後續功能的目錄與應用程式邊界，不建立未被目前行為使用的 GPIO service 或 repository。

領域用語以專案根目錄的 `CONTEXT.md` 為準。

## 5. Python 套件與版本

`backend/pyproject.toml` 是唯一的 Python 專案及直接相依套件來源。版本是 2026-09-11 規劃時的固定快照。

### 5.1 專案中繼資料

- Distribution name：`rpi-gpio-simple-ctrl-backend`
- Version：`0.1.0`
- Import package：`app`
- Build backend：`setuptools.build_meta`
- Python：`>=3.13,<3.14`

build-system 使用 setuptools，但不把 build-system 套件列入應用程式 runtime dependencies。

### 5.2 Runtime dependencies

| 套件 | 固定版本 | 套件宣告的最低 Python |
|---|---:|---:|
| [FastAPI](https://pypi.org/project/fastapi/) | `0.141.1` | `>=3.10` |
| [Uvicorn](https://pypi.org/project/uvicorn/) | `0.52.4` | `>=3.10` |
| [pydantic-settings](https://pypi.org/project/pydantic-settings/) | `2.15.0` | `>=3.10` |

不得使用 `fastapi[standard]` 或 `uvicorn[standard]`。

### 5.3 Development optional dependencies

`dev` extra 包含：

| 套件 | 固定版本 | 套件宣告的最低 Python |
|---|---:|---:|
| [pytest](https://pypi.org/project/pytest/) | `9.1.1` | `>=3.10` |
| [HTTPX](https://pypi.org/project/httpx/) | `0.28.1` | `>=3.8` |
| [Black](https://pypi.org/project/black/) | `26.5.1` | `>=3.10` |
| [isort](https://pypi.org/project/isort/) | `9.0.1` | `>=3.10` |

開發工具不得成為 Raspberry Pi runtime install 的必要套件。

### 5.4 相依套件策略

- runtime 與 development 的直接相依套件使用精確版本。
- 遞移相依套件不在本階段逐一固定。
- 本階段不建立 lock file 或 constraints file。
- 完成 Raspberry Pi 實機驗證後，應記錄完整安裝版本；是否建立跨平台 constraints 留待後續決定。
- 移除目前空白的 `backend/requirements.txt`，避免同時存在兩個套件來源。
- 不建立 `.python-version`。

## 6. 目錄與責任

```text
backend/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── trusted_ip.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── health.py
│   └── core/
│       ├── __init__.py
│       ├── settings.py
│       └── lifespan.py
└── tests/
    ├── conftest.py
    ├── api/
    │   ├── middleware/
    │   │   └── test_trusted_ip.py
    │   └── routes/
    │       └── test_health.py
    └── core/
        └── test_settings.py
```

各檔案責任如下：

| 檔案 | 單一責任 |
|---|---|
| `app/main.py` | 定義 `create_app()` 與 module-level `app` |
| `app/api/router.py` | 聚合本階段 HTTP routers |
| `app/api/routes/health.py` | 定義 `/health` 路由與回應 |
| `app/api/middleware/trusted_ip.py` | 以 ASGI socket peer 套用 CIDR allowlist |
| `app/core/settings.py` | 定義設定模型、`.env` 位置與 CIDR 驗證 |
| `app/core/lifespan.py` | 載入設定並管理啟動及關閉事件 |
| `tests/conftest.py` | 提供只透過公開介面建立應用程式的測試 fixtures |

不建立獨立 logging 模組，也不在 `services/` 預先放置 GPIO 介面。

## 7. Settings 契約

### 7.1 公開設定

本階段唯一的應用程式設定為：

```dotenv
TRUSTED_IP_RANGES=127.0.0.1/32,::1/128
```

程式內預設值包含 IPv4 與 IPv6 loopback：

```text
127.0.0.1/32
::1/128
```

### 7.2 載入規則

- `.env` 固定從 repository root 載入。
- repository root 必須從 `app/core/settings.py` 的實際檔案位置推導，不得依賴 process current working directory。
- `.env` 使用 UTF-8。
- OS environment 優先於 `.env`。
- 環境變數名稱大小寫不敏感。
- `.env` 內不屬於本 Settings model 的欄位予以忽略，讓根目錄 `.env` 可以由前後端共用。
- 匯入 `app.main` 或建立 module-level `app` 時不得讀取 `.env`。
- 未注入 Settings 時，lifespan 啟動階段才建立 Settings instance。

### 7.3 `TRUSTED_IP_RANGES` 規則

- 未設定時使用程式預設值。
- 整個值是空字串或只包含 whitespace 時使用程式預設值。
- 非空值以逗號分隔多個 IPv4 或 IPv6 network。
- 每個項目前後的 whitespace 可以忽略。
- 每個非空項目必須能由 Python `ipaddress` 標準函式庫解析為 IPv4 或 IPv6 network。
- 非空值只要包含無法解析的項目，整份設定即為無效，服務啟動失敗。
- 明確提供的有效清單完整取代預設清單，不自動追加 loopback。
- 內部以不可變 network sequence 表示，middleware 不在每次 request 重新解析字串。

### 7.4 `.env.example`

根目錄 `.env.example` 只加入安全的 loopback 範例：

```dotenv
TRUSTED_IP_RANGES=127.0.0.1/32,::1/128
```

不加入 host、port、environment、debug、GPIO 或 fake-adapter 變數。

## 8. FastAPI 應用程式契約

### 8.1 Application factory

公開介面固定為：

```python
def create_app(settings: Settings | None = None) -> FastAPI:
    ...


app = create_app()
```

- 測試可以注入已建立且有效的 Settings。
- 未注入時，設定由 lifespan 延遲建立。
- application factory 設定 router、middleware、lifespan 與 metadata。
- FastAPI title 為 `Raspberry Pi GPIO Simple Control`。
- FastAPI version 為 `0.1.0`。

### 8.2 Lifespan

啟動順序：

1. 使用注入的 Settings，或從 root `.env` 建立 Settings。
2. 完成所有設定驗證。
3. 將有效設定放入 `app.state.settings`。
4. 記錄啟動訊息。
5. 開始接受 HTTP requests。

關閉時記錄關閉訊息。本階段沒有需要建立或釋放的外部資源。

明確但無效的 `TRUSTED_IP_RANGES` 必須在啟動時拋出設定驗證錯誤，不得退回預設值，也不得讓服務以部分設定啟動。

### 8.3 Logging

- 每個有需要的 module 使用 `logging.getLogger(__name__)`。
- 不設定 application-owned formatter、handler 或全域 log level。
- Uvicorn 控制輸出格式、handler 與 level。
- lifespan 啟動及關閉訊息使用一般資訊層級。
- trusted-IP 拒絕訊息使用 warning 層級。
- 拒絕訊息只包含 socket source IP、HTTP method 與 path。
- 不記錄 request headers、query string、request body 或 Settings 完整內容。

## 9. HTTP 契約

### 9.1 Health endpoint

```http
GET /health
```

允許的來源取得：

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{"status":"ok"}
```

回應只代表 ASGI application 已啟動並能處理請求。不檢查 GPIO、資料庫、檔案、網路或其他外部資源，也不暴露版本或內部狀態。

### 9.2 其他路由

- 不提供 `/`。
- 不建立 `/api/v1` prefix。
- 保留 `/docs`。
- 保留 `/redoc`。
- 保留 `/openapi.json`。
- `/health`、文件與 OpenAPI 全部受相同 trusted-IP middleware 限制。

## 10. Trusted-IP middleware 契約

### 10.1 邊界

- 實作為純 ASGI middleware。
- 只處理 `scope["type"] == "http"`。
- 非 HTTP scope 原樣交給下一層 ASGI application。
- middleware 從 `app.state.settings` 取得已驗證的 network sequence。

### 10.2 來源位址

- 唯一可信來源為 ASGI `scope["client"]` 的 socket peer address。
- 不讀取 `X-Forwarded-For`、`X-Real-IP`、`Forwarded` 或其他 request header。
- `scope["client"]` 遺漏、為 `None`、結構不合法或 host 不是有效 IP 時，一律拒絕。
- IPv4 address 只和 IPv4 networks 比對，IPv6 address 只和 IPv6 networks 比對。
- 位址落在任一設定 network 時允許請求繼續。

Uvicorn 啟動指令必須包含 `--no-proxy-headers`，避免 Uvicorn 在 request 到達應用程式前用 forwarded headers 改寫 `scope["client"]`。此選項由 [Uvicorn 官方設定](https://www.uvicorn.org/settings/)支援。

### 10.3 拒絕回應

所有拒絕情況固定回傳：

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json
```

```json
{"detail":"Forbidden"}
```

不得讓未受信任請求進入 router，也不依路由是否存在而改變拒絕內容。

### 10.4 安全邊界

本 middleware 是可信任區域網路的來源限制，不是使用者認證，也不取代 TLS、reverse proxy、firewall 或網路分段。若未來加入 reverse proxy，必須重新設計 socket peer 與 proxy trust chain，本階段不得先行信任 forwarded headers。

## 11. 測試策略

所有行為變更遵循 `docs/development-process.md` 的 Red–Green–Refactor。每次只完成一個可觀察行為的垂直切片。

### 11.1 測試邊界

- Settings 測試只透過公開 Settings interface。
- HTTP 測試透過 TestClient 或等價的 ASGI HTTP client。
- lifespan 透過 TestClient context 間接啟動，不直接呼叫 lifespan 私人實作。
- 缺少 `scope["client"]` 等 TestClient 不便建立的邊界條件，可以透過最小 ASGI harness 驗證 middleware 的公開 ASGI interface。
- 不直接測試私人 parser function。
- 不 mock 本專案自己的 Settings、lifespan、middleware 或 route module。
- 不以 logger method 呼叫次數作為行為驗收。
- 測試不得依賴實體 Raspberry Pi、GPIO 或網路服務。

### 11.2 Settings 必要案例

1. 未設定 `TRUSTED_IP_RANGES` 時得到 IPv4/IPv6 loopback 預設值。
2. 空字串時得到預設值。
3. whitespace-only 時得到預設值。
4. 合法 IPv4 CIDR 可以載入。
5. 合法 IPv6 CIDR 可以載入。
6. 逗號分隔的多個 CIDR 可以載入。
7. 非空但不合法的項目造成 Settings validation failure。
8. OS environment 覆蓋 root `.env` 的值。

### 11.3 HTTP 必要案例

1. 允許來源呼叫 `/health`，取得精確的 `200` 與 `{"status":"ok"}`。
2. 未受信任來源呼叫 `/health`，取得精確的 `403` 與 `{"detail":"Forbidden"}`。
3. 缺少 client address 時拒絕請求。
4. 未受信任 socket peer 即使提供允許的 `X-Forwarded-For` 仍被拒絕。
5. `/docs`、`/redoc` 與 `/openapi.json` 對未受信任來源均回傳固定 `403`。
6. `/docs`、`/redoc` 與 `/openapi.json` 對允許來源保持可用。
7. TestClient context 內可以觀察到 `app.state.settings` 已設定。

### 11.4 TDD 與格式化順序

每個行為切片採用：

```text
Red：加入一個因預期原因失敗的公開行為測試
Green：加入讓該測試通過的最小實作
Format：依序執行 isort、Black
Verify：重新執行相關測試
Refactor：在測試保持通過時改善結構
```

不得一次先建立完整實作再補測試。

## 12. 格式化設定

Black 設定放在 `backend/pyproject.toml`：

```toml
[tool.black]
target-version = ["py313"]
```

- 使用 Black 預設行寬 88。
- 不啟用 `preview` 或 `unstable`。

isort 設定放在同一檔案：

```toml
[tool.isort]
profile = "black"
```

- 不建立 `.isort.cfg`。
- 不增加其他 import 分組規則。
- 固定先執行 isort，再執行 Black。

從 repository root 執行：

```shell
python -m isort backend/app backend/tests
python -m black backend/app backend/tests
```

檢查模式：

```shell
python -m isort --check-only --diff backend/app backend/tests
python -m black --check --diff backend/app backend/tests
```

實際文件中的 `python` 應替換為各平台 `backend/.venv` 內的 interpreter 路徑。

## 13. 安裝與啟動介面

所有環境都使用 editable install。服務依賴目前 Git checkout，因為 root `.env` 是相對於 source tree 定位；本階段不以 wheel 作為部署產物。

### 13.1 Windows 開發

```powershell
py -3.13 -m venv backend/.venv
backend\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

### 13.2 一般 Linux 開發

```shell
python3.13 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e "backend[dev]"
./backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

### 13.3 Raspberry Pi runtime

```shell
python3 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e backend
./backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --no-proxy-headers
```

- Raspberry Pi 不安裝 `[dev]` extra。
- Raspberry Pi 不使用 `--reload`。
- host 與 port 是 Uvicorn CLI 設定，不加入 application `.env`。
- 預設 allowlist 只允許 loopback。若要從區域網路存取，部署者必須在 root `.env` 明確設定實際可信任 CIDR。
- systemd 管理方式留待後續階段。

## 14. 驗證要求

### 14.1 Windows

交付前必須在目前 Windows workspace 實際執行：

```powershell
backend\.venv\Scripts\python.exe -m pytest backend/tests
backend\.venv\Scripts\python.exe -m compileall backend/app
backend\.venv\Scripts\python.exe -m isort --check-only --diff backend/app backend/tests
backend\.venv\Scripts\python.exe -m black --check --diff backend/app backend/tests
git diff --check
```

另外啟動 Uvicorn，實際確認允許來源的 `/health` 回應。

### 14.2 一般 Linux

若有可用環境，執行等價的 pytest、compileall、isort、Black 與 `/health` smoke test。沒有實際執行時，文件只能說明支援方式，不得宣稱已驗證。

### 14.3 Raspberry Pi

在實機執行：

1. 使用 runtime dependencies 完成 editable install。
2. 使用 Python 3.13 啟動單一 Uvicorn worker。
3. 從 loopback 呼叫 `/health`。
4. 設定實際 LAN CIDR 後，從允許的 LAN client 呼叫 `/health`。
5. 從不允許來源確認固定 `403` 回應。

未在本次工作中實際完成的 Raspberry Pi 步驟必須列為待實機驗證，不得以 Windows 測試結果代替。

## 15. 文件異動

實作完成時同步更新：

- 根目錄 `README.md`：Python 版本、三種安裝/啟動方式、`.env`、health check、測試及格式化指令。
- 根目錄 `.env.example`：只加入安全 loopback allowlist。
- 根目錄 `AGENTS.md`：取代目前「requirements 為空、尚無 FastAPI 流程」的過時說明。
- `CONTEXT.md`：本階段不需追加內容；後續 GPIO Function 實作沿用既有術語。

不得在本階段加入 systemd、GPIO、JSON/YAML/SQLite 或 auth 的操作文件。

## 16. 既有檔案處理與安全界線

實作階段獲准清除並重建的唯一目標為：

```text
G:\Works\github_com\rpi_gpio_simple_ctrl\backend\app
```

執行清除前必須再次解析並驗證絕對路徑位於目前 workspace 的 `backend/app/`。不得把清除範圍擴大到 `backend/`、`backend/tests/`、repository root 或其他未追蹤檔案。

以下目前已知的 frontend 未追蹤檔案不屬於本規格，必須保留：

```text
frontend/.prettierrc
frontend/eslint.config.js
```

製作本規格不代表授權安裝套件、清除 `backend/app/`、提交 Git commit 或開始實作。

## 17. 驗收條件

本階段只有在下列條件全部滿足時才算完成：

1. `backend/pyproject.toml` 是唯一 Python project/dependency definition，且精確符合本規格版本。
2. Python 3.13 可以安裝 development dependencies 並匯入 `app.main`。
3. module import 不讀取 `.env`，lifespan 才載入或接受注入 Settings。
4. 遺漏或空白 allowlist 使用 loopback 預設值；非空錯誤值阻止啟動。
5. 允許來源得到精確 `/health` 成功回應。
6. 未允許或缺少來源得到精確固定 `403` 回應。
7. forwarded headers 無法繞過 socket-peer allowlist。
8. 文件與 OpenAPI routes 套用相同來源限制。
9. 所有必要 pytest cases 通過。
10. compileall、isort、Black 與 `git diff --check` 通過。
11. README、`.env.example` 與 AGENTS 的指令和實際專案一致。
12. Windows 以外未執行的驗證被明確標示，不做未經證實的相容性宣稱。
