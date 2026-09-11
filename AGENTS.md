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

`backend/pyproject.toml` 是後端唯一 Python 專案與直接相依套件來源。Python 必須符合 `>=3.13,<3.14`，虛擬環境固定使用 `backend/.venv/`。

Windows 安裝與啟動：

```powershell
py -3.13 -m venv backend/.venv
backend\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

Linux 開發環境：

以下指令本次未在 Linux 環境實際執行，仍待平台驗證：

```shell
python3.13 -m venv backend/.venv
./backend/.venv/bin/python -m pip install -e "backend[dev]"
./backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-proxy-headers
```

Raspberry Pi runtime 只安裝必要套件並使用單一 worker：

以下指令本次未在 Raspberry Pi 實機執行，完整相容性仍待目標映像與硬體驗證：

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

Python 使用四個空白縮排，YAML 與前端程式碼使用兩個空白；禁止使用 Tab。Python 遵循 PEP 8：模組、函式及變數使用 `snake_case`，類別使用 `PascalCase`，常數使用 `UPPER_SNAKE_CASE`。公開函式須加上型別提示，GPIO 存取應封裝於 `backend/app/services/`。函式 ID 使用小寫連字號格式，例如 `open-door`。Python imports 使用 isort 的 Black profile 排序，其他 Python 格式由 Black 處理；自動格式化時固定先執行 isort，再執行 Black。前端由 Prettier 與 ESLint 管理格式及靜態檢查。請避免無關的大範圍格式調整。

## 測試準則

本專案必須遵循 [`docs/development-process.md`](docs/development-process.md) 定義的 TDD 流程。每次行為變更都要先新增或修改會因預期原因失敗的測試，再完成最小實作並重構。後端測試檔命名為 `test_*.py`；前端使用 Vitest，測試放在 `frontend/tests/` 並命名為 `*.spec.ts`。以模擬物件隔離 GPIO 與計時操作，並註明驗證使用模擬環境或實體 Raspberry Pi。

## Agent skills

### Issue tracker

Issues 與規格使用 `.scratch/<feature-slug>/` 下的 Markdown 檔案管理。詳見 `docs/agents/issue-tracker.md`。

### Setup 保護

重新執行 `setup-matt-pocock-skills` 時，必須保留
`docs/agents/issue-tracker.md` 的專案專用欄位約定：triage 使用
`Category:` 與 `Status:`；Wayfinding 使用 `Type:`、`Execution Status:` 與
`Blocked by:`。不得將 Wayfinding 的 `claimed`／`resolved` 寫入 `Status:`。
若 skill 範本與此約定衝突，先提出差異並等待核准，不得直接覆寫。

### Triage labels

Triage 使用五個預設角色：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human` 與 `wontfix`。詳見 `docs/agents/triage-labels.md`。

### Domain docs

本儲存庫採 single-context，由根目錄 `CONTEXT.md` 與 `docs/adr/` 記錄領域詞彙及架構決策。詳見 `docs/agents/domain.md`。

## Commit 與 Pull Request 規範

一般 Commit 採用 Conventional Commits：

```text
<type>(<scope>)!: <subject>
```

* `type` 必填，可使用 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`chore` 或 `revert`。
* `scope` 選填，使用小寫專案範圍，例如 `backend`、`frontend`、`gpio`、`config`、`docs`、`agents` 或 `merge`。
* `subject` 使用簡短英文及動作導向描述，不超過 50 個字元，結尾不加句號。
* 每個 Commit 只處理一個主題。
* 需要補充背景時，以空行分隔 Body，說明 What、Why 與 How，每行不超過 72 個字元。
* Footer 可使用 `Closes #123` 關聯 issue。
* 破壞性變更須在 Header 加上 `!`，並以 `BREAKING CHANGE:` 說明影響與遷移方式。

例如：

```text
docs(agents): define commit message convention
feat(gpio): add output control endpoint
```

### 合併規則

長期分支白名單為 `dev` 與 `main`；`gh-pages` 不適用本節規則。一般功能整合路徑固定為 `topic → dev → main`，其中 topic 是任何非長期分支的短期工作分支。

`topic → dev` 與 `dev → main` 必須使用 `--no-ff`，並以 Conventional Commit 建立 merge commit：

```text
chore(merge): integrate branches into <target-branch>
```

Merge commit Body 使用下列專用欄位，且其規則優先於一般 Commit 的
What／Why／How 說明：

```text
Branches:
- <source-branch>
```

`Branches:` 為必填欄位，須列出所有來源分支。多個來源分支只能在它們必須作為
不可分割單位發布時，才可使用同一 merge commit；一般情況仍是一個 branch 一個
merge commit。

例如：

```shell
git switch dev
git merge --no-ff codex/init-backend \
  -m "chore(merge): integrate branches into dev" \
  -m "Branches:" \
  -m "- codex/init-backend"
```

`dev` 或 `main` 同步至 topic branch 屬上游同步，可使用 Git 預設 merge message，且不強制使用 `--no-ff` 或 Conventional Commits。不要設定 repository-wide `merge.ff=false`，以保留此例外。

一般 topic branch 不得直接整合至 `main`。緊急修正僅限 `hotfix/<slug>` 分支，可依序整合至 `main` 與 `dev`；兩次都必須使用 `--no-ff` 與上述 Conventional Commit 格式。除必填的 `Branches:` 外，Hotfix merge commit Body 至少包含：

```text
Reason: <緊急原因與影響>
Verification: <執行的檢查與結果>
```

若 merge 有人工衝突處理並修改追蹤檔案，Body 必須額外包含：

```text
Conflict: <affected paths or conflict area>
Resolution: <chosen rule or implementation>
Verification: <commands and results>
```

Hotfix 同時有人工衝突處理時，一個 `Verification:` 欄位即可同時滿足兩項規則。

功能整合原則上在本機以 Git 建立 merge commit；只有 Git hosting service 能產生完全符合本節格式的訊息時，才可使用其合併介面。目前為單人開發，hotfix 直接整合至 `main` 不要求 `Approval:` 欄位。

Pull Request 必須說明行為與設定變更、連結相關 issue、列出執行過的檢查及結果，並標明受影響的 GPIO 腳位或啟動／關閉狀態。Vue 介面變更應附截圖，GPIO 變更應附硬體測試說明。禁止提交憑證、裝置專用密鑰或執行期資料。
