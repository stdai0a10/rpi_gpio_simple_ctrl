# 前端初始化設計

## 目標

在既有 `frontend/` 目錄中建立可執行、可建置、可測試的 Vue 3
前端殼層，並以 npm、漸進式 TypeScript、Vue Router、Vitest、ESLint
與 Prettier 作為後續開發基礎。

完成後，瀏覽器進入 `/` 時只顯示 `RPI GPIO Simple Controller`。
本階段不建立任何 GPIO 控制行為或後端整合。

## 現況與限制

- `frontend/package.json` 是空檔案，尚無可執行的前端工作流程。
- `frontend/src/` 與 `frontend/tests/` 尚無應用程式或測試。
- 既有 `frontend/.prettierrc` 與 `frontend/eslint.config.js` 是使用者提供的
  未追蹤設定，必須納入初始化，而非直接捨棄。
- create-vue 會在確認後清空非空的目標目錄，因此不得直接以現有
  `frontend/` 作為 scaffold 目標，也不得使用 `--force`。
- `backend/app/`、`.agents/` 與其他非前端變更不在本次範圍內。
- 本專案要求前端程式碼使用兩個空白縮排，並以 Red–Green–Refactor
  進行行為開發。

## 初始化策略

採用 Vue 官方 Quick Start 的 `npm create vue@latest`，但先在一個獨立、
可明確辨識的暫存目錄產生骨架。產生時選擇：

- TypeScript：是
- JSX：否
- Vue Router：是
- Pinia：否
- Vitest：是
- E2E：否
- ESLint：是
- Prettier：是
- Vue DevTools：否

產生完成後，先檢查骨架內容與套件版本，再把需要的檔案合併至
`frontend/`。不得用整個目錄覆寫的方式搬移。暫存骨架只作為官方範本，
驗證合併結果後移除，且不得提交。

套件管理只使用 npm。`package.json` 名稱固定為
`rpi-gpio-simple-ctrl-frontend` 且保持私有；`package-lock.json` 必須提交，
開發者安裝既有相依套件時使用 `npm ci`。不得加入 Yarn、pnpm、Bun 或其
lockfile。

Node.js 支援範圍以執行初始化時的 create-vue/Vite 官方需求為準，並寫入
`package.json` 的 `engines.node`。目前環境 Node.js `v24.15.0` 符合已確認
的官方需求 `^22.18.0 || >=24.12.0`。

## 應用程式結構

前端殼層只包含下列責任：

- `src/main.ts`：建立 Vue 應用程式、安裝 router 並掛載根元件。
- `src/App.vue`：只提供 `RouterView`，不承載頁面內容。
- `src/router/index.ts`：使用 `createWebHistory()`，只定義 `/` 路由。
- `src/views/HomeView.vue`：以語意化的 `h1` 顯示
  `RPI GPIO Simple Controller`。

不保留 create-vue 的 welcome、about、icons、示範元件、示範資源或示範
樣式。本階段不要求自訂視覺設計；瀏覽器只需呈現專案名稱。

資料流只有：

```text
src/main.ts -> Vue Router -> App.vue/RouterView -> HomeView.vue
```

本階段不建立 API client、Vite proxy、CORS 設定、執行環境變數、GPIO
操作、載入狀態或錯誤畫面。未知路由也不新增 fallback 頁面；新增第二個
應用路由或部署前，伺服器必須能把非檔案路徑回退至 `index.html`，以支援
`createWebHistory()`。

## TypeScript 策略

TypeScript 採漸進式使用：

- 保持嚴格型別檢查。
- `allowJs` 設為 `true`。
- `checkJs` 設為 `false`。
- `.js`、`.ts` 與 `.vue` 可以共存。
- 新增的共用邏輯優先使用 TypeScript。

Vue 入口、router 與測試使用 TypeScript。單純呈現內容的 Vue 元件不因
本次初始化而被迫加入沒有實際用途的 script 區塊。

## 測試設計

使用 Vitest、Vue Test Utils 與 jsdom。測試放在 `frontend/tests/`，不採用
create-vue 預設可能產生的 `src/**/__tests__/` 位置。

首頁是本次唯一的行為增量，依 TDD 完成：

1. 先建立失敗測試，掛載使用 router 的根應用並前往 `/`。
2. 驗證頁面包含 `h1`，且文字精確等於
   `RPI GPIO Simple Controller`。
3. 再加入最小的 router、`App.vue` 與 `HomeView.vue` 實作使測試通過。
4. 移除未使用的官方示範內容後重跑測試。

初始化工具本身不是產品行為，不為 scaffold 命令撰寫測試；它以安裝、
型別檢查、單元測試與 production build 成功作為驗證。

## Prettier 設計

移除 `frontend/.prettierrc`，改為 ESM 格式的
`frontend/prettier.config.js`，並保留既有值：

```js
export default {
  endOfLine: 'lf',
  jsxSingleQuote: true,
  semi: true,
  singleQuote: true,
  tabWidth: 2,
  trailingComma: 'none',
  useTabs: false
}
```

Prettier 是實際套用格式的唯一工具。`format` 可以改寫檔案，
`format:check` 只能檢查且不得修改工作區；ESLint 的相容格式規則只負責
驗證，不負責取代 Prettier 重新排版。

## ESLint 設計

`package.json` 使用 `"type": "module"`，`frontend/eslint.config.js` 也使用
ESM flat config。設定須依 create-vue 實際產生的 Vue、TypeScript 與
ESLint 套件版本組合，不沿用目前只有單一規則的 CommonJS 結構。

安裝並加入 `eslint-config-prettier/flat`，置於 Vue、TypeScript 等上游
設定之後，以關閉會與 Prettier 衝突的格式規則。接著在最後一個自訂
config object 重新啟用下列與 Prettier 輸出相容的規則：

```js
'space-before-function-paren': [
  'error',
  {
    anonymous: 'always',
    named: 'never',
    asyncArrow: 'always'
  }
]
```

`lint` 只檢查且不得改寫檔案；`lint:fix` 才能執行可自動修正的 ESLint
變更。

## npm scripts 與品質閘門

`frontend/package.json` 至少提供：

- `dev`：啟動 Vite 開發伺服器。
- `build`：執行 production build，並確保型別檢查成功。
- `preview`：預覽 production build。
- `format`：以 Prettier 改寫目標檔案。
- `format:check`：只檢查 Prettier 格式。
- `lint`：只執行 ESLint 檢查。
- `lint:fix`：執行 ESLint 自動修正。
- `type-check`：以 vue-tsc 進行型別檢查。
- `test:unit`：以非互動模式執行 Vitest。
- `test:unit:watch`：在本機以 watch 模式執行 Vitest。
- `check`：依序執行 `format:check`、`lint`、`type-check`、
  `test:unit`。

`check` 的每一段都必須回傳正確的非零失敗狀態，且整個指令不得修改
追蹤或未追蹤檔案。

## 文件更新

- 更新 `AGENTS.md` 的前端章節，移除 package 尚未初始化的舊敘述，補上
  npm 安裝、開發、測試、型別檢查、格式、lint、完整檢查與建置指令。
- 更新 `README.md`，提供開發者足以啟動前端的精簡步驟與 Node.js 需求。
- 文件不得要求全域安裝 Yarn，因為 npm 是唯一套件管理工具。

## 預期檔案邊界

預期建立或完成下列前端責任：

- package metadata 與 lockfile
- Vite、Vue、TypeScript 與 Vitest 設定
- ESM Prettier 與 ESLint flat config
- Vue entry、router、根元件與首頁元件
- `frontend/tests/` 中的首頁路由測試
- frontend 專用 `.gitignore`

預期移除 `frontend/.prettierrc`。官方示範檔案不應合併進正式
`frontend/`，因此不需要在正式目錄先建立再刪除。

## 驗證標準

在 `frontend/` 執行並確認：

```shell
npm ci
npm run check
npm run build
```

另從儲存庫根目錄執行：

```shell
git diff --check
```

最後人工確認：

- `npm run dev` 可啟動前端。
- `/` 只顯示 `RPI GPIO Simple Controller`。
- 瀏覽器 console 無初始化錯誤。
- UI 變更備有可供 Pull Request 使用的截圖。
- Git diff 不包含 `backend/app/`、`.agents/`、暫存 scaffold 或其他無關
  變更。

## 參考資料

- [Vue Quick Start](https://vuejs.org/guide/quick-start.html)
- [create-vue](https://github.com/vuejs/create-vue)
- [`docs/development-process.md`](../../development-process.md)
- [`CONTEXT.md`](../../../CONTEXT.md)
