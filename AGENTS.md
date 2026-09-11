# 儲存庫指南

## 專案結構與模組配置

### 後端結構

`backend/` 存放 Python/FastAPI 後端、後端測試及相依套件定義。測試放在 `backend/tests/`，Python 虛擬環境使用 `backend/.venv/`，且不得納入版本控制。

### 前端結構

`frontend/` 存放 Vue.js 前端原始碼、前端測試及 npm 套件設定。原始碼放在 `frontend/src/`，測試放在 `frontend/tests/`。

### 共用與專案層級檔案

根目錄 `tests/` 存放跨前後端的整合或端對端測試。`config/` 存放可納入版本控制的共用設定與範例，`data/` 存放應用程式資料及執行階段定義，`docs/` 存放正式文件，`scripts/` 存放安裝與維護腳本。

專案級 Codex Skills 位於 `.agents/skills/`，安裝紀錄由 `skills-lock.json` 管理；`.vscode/` 僅供編輯器設定使用。

## 建置、測試與開發指令

### 後端

`backend/requirements.txt` 目前為空，尚未定義相依套件、測試或 FastAPI 啟動流程。可先建立虛擬環境並檢查 Python 語法：

```shell
python -m venv backend/.venv
```

Windows：

```powershell
backend\.venv\Scripts\python.exe -m compileall backend/app
```

macOS／Linux：

```shell
./backend/.venv/bin/python -m compileall backend/app
```

### 前端

前端需要 Node.js `^22.18.0 || >=24.12.0`，套件管理統一使用 npm。
首次取得或 lockfile 更新後安裝相依套件：

```shell
cd frontend
npm ci
```

常用指令：

```shell
npm run dev
npm run format
npm run format:check
npm run lint
npm run lint:fix
npm run type-check
npm run test:unit
npm run test:unit:watch
npm run check
npm run build
npm run preview
```

`npm run check` 依序執行格式檢查、ESLint、TypeScript 型別檢查與 Vitest，
且不會修改追蹤或未追蹤的專案檔案；型別檢查可能更新
`node_modules/.tmp` 中已忽略的快取。

### 共用檢查

所有平台在交付前都應執行：

```shell
git diff --check
```

新增相依套件或執行流程時，須一併提交可重現的套件清單，並在本章節補上對應的安裝、啟動、測試及建置指令。

## 程式風格與命名慣例

Python 使用四個空白縮排，YAML 與前端程式碼使用兩個空白；禁止使用 Tab。Python 遵循 PEP 8：模組、函式及變數使用 `snake_case`，類別使用 `PascalCase`，常數使用 `UPPER_SNAKE_CASE`。公開函式須加上型別提示，GPIO 存取應封裝於 `backend/app/services/`。函式 ID 使用小寫連字號格式，例如 `open-door`。前端由 Prettier 與 ESLint 管理格式及靜態檢查，請避免無關的大範圍格式調整。

## 測試準則

本專案必須遵循 [`docs/development-process.md`](docs/development-process.md) 定義的 TDD 流程。每次行為變更都要先新增或修改會因預期原因失敗的測試，再完成最小實作並重構。後端測試檔命名為 `test_*.py`；前端測試框架與命名方式須在前端骨架完成時一併確立。以模擬物件隔離 GPIO 與計時操作，並註明驗證使用模擬環境或實體 Raspberry Pi。

## Agent skills

### Issue tracker

Issues 與規格使用 `.scratch/<feature-slug>/` 下的 Markdown 檔案管理。詳見 `docs/agents/issue-tracker.md`。

### Triage labels

Triage 使用五個預設角色：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human` 與 `wontfix`。詳見 `docs/agents/triage-labels.md`。

### Domain docs

本儲存庫採 single-context，由根目錄 `CONTEXT.md` 與 `docs/adr/` 記錄領域詞彙及架構決策。詳見 `docs/agents/domain.md`。

## Commit 與 Pull Request 規範

Commit message 採用 Conventional Commits：

```text
<type>(<scope>)!: <subject>
```

* `type` 必填，可使用 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`chore` 或 `revert`。
* `scope` 選填，使用小寫專案範圍，例如 `backend`、`frontend`、`gpio`、`config`、`docs` 或 `agents`。
* `subject` 使用簡短英文及動作導向描述，不超過 50 個字元，結尾不加句號。
* 每個 Commit 只處理一個主題。
* 需要補充背景時，以空行分隔 Body，說明 What、Why 與 How，每行不超過 72 個字元。
* Footer 可使用 `Closes #123` 關聯 issue。
* 破壞性變更須在 Header 加上 `!`，並以 `BREAKING CHANGE:` 說明影響與遷移方式。

例如：

```text
docs(agents): define commit message convention
feat(gpio): add output control endpoint`。
```

Pull Request 必須說明行為與設定變更、連結相關 issue、列出執行過的檢查及結果，並標明受影響的 GPIO 腳位或啟動／關閉狀態。Vue 介面變更應附截圖，GPIO 變更應附硬體測試說明。禁止提交憑證、裝置專用密鑰或執行期資料。
