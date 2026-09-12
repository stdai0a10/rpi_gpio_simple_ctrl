# Vue 前端交付與部署

本文件說明如何把已編譯的 Vue 前端交給既有的 FastAPI application。正式環境只以
Uvicorn 提供 HTTP 服務；本階段不使用 Nginx、Caddy、CDN 或另一個 Node.js
frontend server。

## 共通條件

- 前端建置輸出固定為 repository root 下的 `frontend/dist/`，且不納入 Git。
- backend source 與 `frontend/dist/` 必須來自同一個 checkout 或 release；不要把
  不同 revision 的 bundle 與 backend 混用。
- 前端建置需要 Node.js `^22.18.0 || >=24.12.0`，套件管理器固定為 npm。
- Uvicorn 啟動時會先驗證 Settings，再驗證 `frontend/dist/` 與
  `frontend/dist/index.html`。任一項缺失都會在開始接受請求前失敗，錯誤會指出
  預期位置並建議重新建置或複製 bundle。
- FastAPI 會同時提供 SPA、已編譯 asset、`/health`、`/api`、`/docs`、`/redoc`
  與 `/openapi.json`；它們都遵守 `TRUSTED_IP_RANGES`。

## 方式一：在相容的 Raspberry Pi 環境建置

適合已安裝相容 Node.js 的目標裝置。Raspberry Pi 型號只用於選擇工作流程的參考；
本文件不對特定型號的相容性或效能做保證。

```shell
npm --prefix frontend ci
npm --prefix frontend run check
npm --prefix frontend run build
```

完成後，依本專案既有 Raspberry Pi runtime 指示建立只含 backend runtime 依賴的
`backend/.venv/`，再由 repository root 啟動單一 Uvicorn worker：

```shell
./backend/.venv/bin/python -m uvicorn app.main:app \
  --app-dir backend --host 0.0.0.0 --port 8000 --workers 1 --no-proxy-headers
```

`npm ci` 只用於此建置階段；它不是正式服務的一部分。

## 方式二：在 Windows 或其他建置機建置後複製

這是資源受限 Raspberry Pi 的建議流程。先在與 backend 相同 revision 的建置機上：

```shell
npm --prefix frontend ci
npm --prefix frontend run check
npm --prefix frontend run build
```

只把產生的 `frontend/dist/` 複製到目標機相同 checkout 或 release 的
`frontend/dist/`。目標機不需要為了提供已編譯前端安裝 Node.js；安裝 backend runtime
依賴並以 Uvicorn 啟動即可。

複製完成後，先確認目標位置至少包含 `frontend/dist/index.html`，再啟動服務。不要將
建置機的 `node_modules/`、`backend/.venv/`、`.env` 或 `data/` 一併傳送。

## 方式三：交付包含 bundle 的 release archive

先在同一 revision 建置 `frontend/dist/`，然後建立一個只含 release 所需檔案的暫存目錄
再壓縮。archive 應包含 backend source、frontend source、已編譯的 `frontend/dist/`、
設定範例與必要文件；部署者在目標上建立自己的 runtime virtual environment 和 `.env`。

archive 必須排除：

- `frontend/node_modules/` 與其他 dependency directories
- `backend/.venv/` 與所有 virtual environments
- `.env` 與任何憑證、裝置專用密鑰
- `data/` 及其他 runtime data
- Python/Node 快取、測試輸出與本機 editor state

壓縮前請檢查檔案清單：確保 `frontend/dist/index.html` 已包含、排除項目沒有被收進去，
且 archive 與 backend source 的 revision 相同。本文件只定義交付內容；不提供 archive
產生腳本或 release publishing automation。

## 本機開發

開發時保持 Vite 與 Uvicorn 為兩個只在 loopback 使用的程序。Windows：

```powershell
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --no-proxy-headers
npm --prefix frontend run dev
```

Linux：

```shell
./backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --no-proxy-headers
npm --prefix frontend run dev
```

Vite 只綁定 `127.0.0.1`，並將相對的 `/health` 與 `/api` request proxy 到
`http://127.0.0.1:8000`。前端程式碼應使用相對 URL，不要硬編碼 backend host 或 port。
`/docs`、`/redoc` 與 `/openapi.json` 不經 Vite proxy，請直接由 Uvicorn 存取。

## 部署後檢查

從可信任來源確認：

```shell
curl http://127.0.0.1:8000/health
curl -I http://127.0.0.1:8000/
```

瀏覽器也應能載入 `/`、已編譯 asset 與直接開啟的 SPA history route。遺失 asset 與未知
`/api/...` URL 都應回傳 `404`，而不應載入 SPA shell。Raspberry Pi 實機的 Node.js、
作業系統映像與硬體相容性仍須由實際部署環境驗證。

## 本次實作驗證紀錄

2026-09-12 在 Windows 開發環境實際執行：

- `npm --prefix frontend run check` 通過 Prettier、ESLint、TypeScript 與 Vitest
  （2 個 test files、3 個 tests）。
- `npm --prefix frontend run build-only -- --outDir <temporary-directory>` 成功產生
  production bundle（Vite 處理 24 個 modules）。輸出刻意放在 temporary directory，
  因此沒有覆寫本機既有且被 Git 忽略的 `frontend/dist/`。
- `backend\\.venv\\Scripts\\python.exe -m pytest backend/tests` 通過 77 個 tests。
- 以 temporary production bundle 啟動 loopback Uvicorn，確認 `/`、已編譯 asset、
  SPA history route、遺失 asset 的 `404`、未知 `/api/...` 的 JSON `404`、`/health` 與
  `/docs` 都符合預期。

Raspberry Pi 實機的 Node.js、作業系統映像與 GPIO 硬體相容性未在此環境驗證，仍須在目標
部署環境完成確認。
