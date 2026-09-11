# Frontend Initialization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立以 npm 管理、可執行、可建置、可測試的 Vue 3 前端殼層，並讓 `/` 只顯示 `RPI GPIO Simple Controller`。

**Architecture:** 先在獨立的 `frontend-bootstrap/` 暫存目錄用官方 create-vue 產生 bare scaffold，再把經審核的工具鏈檔案合併到既有 `frontend/`，避免 create-vue 清空使用者檔案。正式應用維持 `main.ts -> router -> App.vue/RouterView -> HomeView.vue` 的最小資料流，首頁行為以 Vitest 與 memory history 先測試再實作。

**Tech Stack:** Node.js `^22.18.0 || >=24.12.0`、npm、Vue 3、Vite、TypeScript、Vue Router、Vitest、Vue Test Utils、jsdom、ESLint flat config、eslint-config-prettier、Prettier

**Spec:** `docs/superpowers/specs/2026-09-10-frontend-initialization-design.md`

## Global Constraints

- 只使用 npm；提交 `frontend/package-lock.json`，不得加入 Yarn、pnpm、Bun 或其他 lockfile。
- `package.json` 名稱固定為 `rpi-gpio-simple-ctrl-frontend`，並保持 `"private": true` 與 `"type": "module"`。
- Node.js 支援範圍固定為 `^22.18.0 || >=24.12.0`；目前環境 `v24.15.0` 符合需求。
- 啟用 TypeScript、Vue Router、Vitest、ESLint、Prettier；不得加入 JSX、Pinia、E2E、Vue DevTools 或 Oxlint。
- TypeScript 必須設定 `strict: true`、`allowJs: true`、`checkJs: false`。
- Vue Router 必須使用 `createWebHistory()`，正式路由只有 `/`。
- 所有前端測試放在 `frontend/tests/`；不得建立 `src/**/__tests__/`。
- 首頁 body 只顯示一個 `h1`，文字精確為 `RPI GPIO Simple Controller`；不得加入教學元件、示範資源或 GPIO/API 整合。
- `frontend/.prettierrc` 的既有值必須完整移轉至 ESM `frontend/prettier.config.js`。
- ESLint 的 `space-before-function-paren` 必須使用 `{ anonymous: 'always', named: 'never', asyncArrow: 'always' }`。
- `npm run check` 必須依序執行 `format:check`、`lint`、`type-check`、`test:unit`，且不得修改檔案。
- 保留 `backend/app/`、`.agents/` 與所有其他無關工作區變更；每次提交只暫存明列的檔案。

## File Structure

- `frontend/package.json`：套件 metadata、Node engine、正式 npm scripts 與相依套件。
- `frontend/package-lock.json`：npm 解析後的可重現相依版本。
- `frontend/.gitignore`：排除 `node_modules/`、`dist/`、coverage 與本機檔案。
- `frontend/index.html`：Vite HTML entry 與頁面 title。
- `frontend/env.d.ts`：Vite client 型別宣告。
- `frontend/vite.config.ts`：Vue plugin 與 `@` 到 `src/` 的 alias。
- `frontend/vitest.config.ts`：jsdom 測試環境，沿用 Vite alias。
- `frontend/tsconfig.json`：app、node 與 Vitest project references。
- `frontend/tsconfig.app.json`：瀏覽器程式碼與漸進式 TypeScript 設定。
- `frontend/tsconfig.node.json`：Vite、Vitest 與 ESLint 設定檔型別檢查。
- `frontend/tsconfig.vitest.json`：`frontend/tests/**/*.ts` 的測試型別設定。
- `frontend/prettier.config.js`：保留既有格式值的 ESM Prettier 設定。
- `frontend/eslint.config.js`：Vue、TypeScript、Prettier 與專案規則的 flat config。
- `frontend/src/main.ts`：Vue application composition root。
- `frontend/src/App.vue`：只承載 `RouterView` 的根元件。
- `frontend/src/router/index.ts`：輸出可測試的 `routes` 與 production router。
- `frontend/src/views/HomeView.vue`：只呈現專案名稱的首頁。
- `frontend/tests/views/HomeView.spec.ts`：驗證 `/` 路由的可見行為。
- `AGENTS.md`：前端安裝、執行、檢查與建置指令。
- `README.md`：開發者可直接使用的最短前端啟動流程。

---

### Task 1: 建立可建置的 Vue 工具鏈與空白殼層

**Files:**
- Create: `frontend/.gitignore`
- Create: `frontend/env.d.ts`
- Create: `frontend/index.html`
- Create: `frontend/package-lock.json`
- Create: `frontend/prettier.config.js`
- Create: `frontend/tsconfig.json`
- Create: `frontend/tsconfig.app.json`
- Create: `frontend/tsconfig.node.json`
- Create: `frontend/tsconfig.vitest.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/vitest.config.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/router/index.ts`
- Modify: `frontend/package.json`
- Modify: `frontend/eslint.config.js`
- Remove after migration: `frontend/.prettierrc`
- Temporary only: `frontend-bootstrap/`

**Interfaces:**
- Consumes: `frontend/.prettierrc` 的七個既有格式值；create-vue 產生的目前官方相依版本與基礎設定。
- Produces: `routes: RouteRecordRaw[]`、default export `router: Router`、`npm run dev|build|preview|format|format:check|lint|lint:fix|type-check|test:unit|test:unit:watch|check`。

- [ ] **Step 1: 記錄工作區與既有設定，確認暫存目錄不存在**

Run from repository root:

```powershell
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' status --short
Get-Content -Raw frontend/.prettierrc
Get-Content -Raw frontend/eslint.config.js
if (Test-Path -LiteralPath 'frontend-bootstrap') {
  throw 'frontend-bootstrap already exists; inspect it before continuing'
}
```

Expected: status 仍可包含使用者的 `backend/app/`、`frontend/.prettierrc` 與
`frontend/eslint.config.js`；`frontend-bootstrap` 不存在；Prettier 值與 spec
一致。

- [ ] **Step 2: 在獨立目錄產生官方 bare scaffold**

Run from repository root in PowerShell:

```powershell
npm create vue@latest frontend-bootstrap '--' --typescript --router --vitest --eslint --prettier --bare
```

Expected: create-vue 建立 `frontend-bootstrap/`；因已提供 feature flags，
不進入功能選擇互動；命令不得包含 `--force`。

- [ ] **Step 3: 驗證 scaffold 的功能與排除項目**

Run:

```powershell
rg --files frontend-bootstrap | Sort-Object
Get-Content -Raw frontend-bootstrap/package.json
```

Expected: package 含 Vue、Vue Router、TypeScript、Vitest、Vue Test Utils、
jsdom、`@types/jsdom`、ESLint、Vitest ESLint plugin、eslint-config-prettier
與 Prettier。若目前 create-vue 自動加入
Oxlint，其檔案與相依套件只能留在暫存 scaffold，後續不得合併；不得出現
Pinia、JSX、Cypress、Playwright 或 Vue DevTools 的正式相依套件。

- [ ] **Step 4: 合併官方基礎設定，不覆寫使用者的兩個設定來源**

Copy only the listed files:

```powershell
$frontendScaffoldFiles = @(
  '.gitignore',
  'env.d.ts',
  'index.html',
  'package.json',
  'tsconfig.json',
  'tsconfig.app.json',
  'tsconfig.node.json',
  'tsconfig.vitest.json',
  'vite.config.ts',
  'vitest.config.ts'
)

foreach ($frontendScaffoldFile in $frontendScaffoldFiles) {
  $sourcePath = Join-Path 'frontend-bootstrap' $frontendScaffoldFile
  if (-not (Test-Path -LiteralPath $sourcePath)) {
    throw "Expected scaffold file is missing: $sourcePath"
  }
  Copy-Item -LiteralPath $sourcePath -Destination (Join-Path 'frontend' $frontendScaffoldFile)
}
```

Expected: `frontend/.prettierrc` 與 `frontend/eslint.config.js` 尚未被 copy
覆寫；`frontend/src/` 與 `frontend/tests/` 仍由本計畫控制。

- [ ] **Step 5: 將 package metadata、scripts 與相依範圍固定為核准內容**

Use `apply_patch` to make `frontend/package.json` exactly:

```json
{
  "name": "rpi-gpio-simple-ctrl-frontend",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": "^22.18.0 || >=24.12.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "npm run type-check && npm run build-only",
    "build-only": "vite build",
    "preview": "vite preview",
    "format": "prettier . --write",
    "format:check": "prettier . --check",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "type-check": "vue-tsc --build",
    "test:unit": "vitest run",
    "test:unit:watch": "vitest",
    "check": "npm run format:check && npm run lint && npm run type-check && npm run test:unit"
  },
  "dependencies": {
    "vue": "^3.5.42",
    "vue-router": "^5.2.0"
  },
  "devDependencies": {
    "@tsconfig/node24": "^24.0.5",
    "@types/jsdom": "^28.0.3",
    "@types/node": "^24.13.3",
    "@vitejs/plugin-vue": "^6.0.8",
    "@vitest/eslint-plugin": "^1.6.21",
    "@vue/eslint-config-typescript": "^14.9.0",
    "@vue/test-utils": "^2.5.0",
    "@vue/tsconfig": "^0.9.1",
    "eslint": "^10.9.1",
    "eslint-config-prettier": "^10.1.8",
    "eslint-plugin-vue": "~10.10.0",
    "jiti": "^2.7.0",
    "jsdom": "^30.0.1",
    "prettier": "3.9.6",
    "typescript": "~6.0.0",
    "vite": "^8.2.2",
    "vitest": "^4.1.11",
    "vue-eslint-parser": "^10.4.1",
    "vue-tsc": "^3.3.11"
  }
}
```

Expected: 沒有 `oxlint`、`eslint-plugin-oxlint`、`npm-run-all2`、Pinia、
JSX、E2E 或 Vue DevTools dependency；所有會修改檔案的動作都有獨立
script，`check` 只串接 read-only scripts。

- [ ] **Step 6: 固定 Vite 與 Vitest 設定**

Use `apply_patch` to make `frontend/vite.config.ts`:

```ts
import { fileURLToPath, URL } from 'node:url';

import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
});
```

Use `apply_patch` to make `frontend/vitest.config.ts`:

```ts
import { fileURLToPath } from 'node:url';

import { defineConfig, mergeConfig } from 'vitest/config';

import viteConfig from './vite.config';

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',
      include: ['tests/**/*.spec.ts'],
      root: fileURLToPath(new URL('./', import.meta.url))
    }
  })
);
```

Expected: Vite 只載入 Vue plugin；Vitest 只搜尋 `frontend/tests/**/*.spec.ts`。

- [ ] **Step 7: 設定漸進式 TypeScript**

Keep the create-vue project references in `frontend/tsconfig.json` and the
Node settings in `frontend/tsconfig.node.json`. Use `apply_patch` to make
`frontend/tsconfig.app.json`:

```json
{
  "extends": "@vue/tsconfig/tsconfig.dom.json",
  "include": ["env.d.ts", "src/**/*", "src/**/*.vue"],
  "exclude": ["src/**/__tests__/*"],
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "paths": {
      "@/*": ["./src/*"]
    },
    "strict": true,
    "allowJs": true,
    "checkJs": false
  }
}
```

Use `apply_patch` to make `frontend/tsconfig.vitest.json`:

```json
{
  "extends": "./tsconfig.app.json",
  "exclude": [],
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.vitest.tsbuildinfo",
    "lib": [],
    "types": ["node", "jsdom"]
  },
  "include": ["env.d.ts", "tests/**/*.ts"]
}
```

Expected: application TypeScript remains strict, JavaScript is accepted but
not type-checked, and test files are included from the repository-mandated
directory.

- [ ] **Step 8: 將 Prettier 設定移轉為 ESM JavaScript**

Use `apply_patch` to create `frontend/prettier.config.js`:

```js
export default {
  endOfLine: 'lf',
  jsxSingleQuote: true,
  semi: true,
  singleQuote: true,
  tabWidth: 2,
  trailingComma: 'none',
  useTabs: false
};
```

Verify the values before removing the old untracked file:

```powershell
Get-Content -Raw frontend/.prettierrc
Get-Content -Raw frontend/prettier.config.js
Remove-Item -LiteralPath 'frontend/.prettierrc'
```

Expected: all seven values are represented in `prettier.config.js`, then only
the old `frontend/.prettierrc` is removed.

- [ ] **Step 9: 將 ESLint 設定改為 Vue/TypeScript/Prettier ESM flat config**

Use `apply_patch` to make `frontend/eslint.config.js`:

```js
import { withVueTs, vueTsConfigs } from '@vue/eslint-config-typescript';
import skipFormatting from 'eslint-config-prettier/flat';
import { globalIgnores } from 'eslint/config';
import pluginVue from 'eslint-plugin-vue';
import pluginVitest from '@vitest/eslint-plugin';

export default withVueTs(
  {
    rootDir: import.meta.dirname,
    scriptLangs: ['ts', 'js']
  },
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,cjs,vue,ts,mts,cts}']
  },
  globalIgnores(['**/dist/**', '**/coverage/**']),
  pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,
  {
    ...pluginVitest.configs.recommended,
    files: ['tests/**/*.spec.ts']
  },
  skipFormatting,
  {
    name: 'app/project-rules',
    rules: {
      'space-before-function-paren': [
        'error',
        {
          anonymous: 'always',
          named: 'never',
          asyncArrow: 'always'
        }
      ]
    }
  }
);
```

Expected: `skipFormatting` closes upstream Prettier conflicts, then the final
project config re-enables the Prettier-compatible function-spacing rule.
There must be no Oxlint import or `.oxlintrc.json` in `frontend/`.

- [ ] **Step 10: 建立可建置但沒有產品行為的空白殼層**

Use `apply_patch` to make `frontend/index.html` contain this body and title;
retain Vite's normal charset and viewport metadata:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="data:," />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>RPI GPIO Simple Controller</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

Use `apply_patch` to create `frontend/src/main.ts`:

```ts
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

createApp(App).use(router).mount('#app');
```

Use `apply_patch` to create `frontend/src/App.vue`:

```vue
<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <RouterView />
</template>
```

Use `apply_patch` to create `frontend/src/router/index.ts`:

```ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
```

Expected: application builds and shows no create-vue tutorial content; no `/`
route has been added yet, preserving a real Red step for Task 2.

- [ ] **Step 11: 安裝相依套件並產生 npm lockfile**

Run:

```powershell
Set-Location frontend
npm install
Set-Location ..
```

Expected: `frontend/package-lock.json` and ignored `frontend/node_modules/`
exist; npm reports no engine mismatch on Node.js `v24.15.0`.

- [ ] **Step 12: 格式化並驗證空白工具鏈**

Run:

```powershell
Set-Location frontend
npm run format
npm run format:check
npm run lint
npm run type-check
npm run test:unit -- --passWithNoTests
npm run build
Set-Location ..
```

Expected: every command exits 0; Vitest reports no test files but exits 0 only
because this bootstrap verification explicitly passes `--passWithNoTests`;
Vite emits `frontend/dist/` without tutorial text.

- [ ] **Step 13: 驗證後安全移除暫存 scaffold**

Run from repository root:

```powershell
$repositoryRoot = (Resolve-Path -LiteralPath '.').Path
$frontendBootstrapPath = (Resolve-Path -LiteralPath 'frontend-bootstrap').Path
$expectedFrontendBootstrapPath = Join-Path $repositoryRoot 'frontend-bootstrap'

if ($frontendBootstrapPath -ne $expectedFrontendBootstrapPath) {
  throw "Refusing to remove unexpected path: $frontendBootstrapPath"
}

Remove-Item -LiteralPath $frontendBootstrapPath -Recurse -Force
Test-Path -LiteralPath 'frontend-bootstrap'
```

Expected: the final command prints `False`; only the verified
`frontend-bootstrap/` directory is removed.

- [ ] **Step 14: Review and commit only the frontend foundation**

Run:

```powershell
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' status --short
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --check
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' add -- frontend/.gitignore frontend/env.d.ts frontend/index.html frontend/package.json frontend/package-lock.json frontend/prettier.config.js frontend/eslint.config.js frontend/tsconfig.json frontend/tsconfig.app.json frontend/tsconfig.node.json frontend/tsconfig.vitest.json frontend/vite.config.ts frontend/vitest.config.ts frontend/src/App.vue frontend/src/main.ts frontend/src/router/index.ts
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --cached --check
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --cached --stat
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' commit -m "chore(frontend): initialize Vue toolchain"
```

Expected: commit contains only the listed frontend foundation files. The
untracked `backend/app/` and any unrelated `.agents/` changes remain outside
the index.

---

### Task 2: 以 TDD 加入唯一首頁路由

**Files:**
- Create: `frontend/tests/views/HomeView.spec.ts`
- Create: `frontend/src/views/HomeView.vue`
- Modify: `frontend/src/router/index.ts`

**Interfaces:**
- Consumes: Task 1 exported `routes: RouteRecordRaw[]`, `App.vue`'s `RouterView`, Vitest jsdom environment, and `@` alias.
- Produces: route record `{ path: '/', name: 'home', component: HomeView }`; `/` renders one `h1` with exact text `RPI GPIO Simple Controller`.

- [ ] **Step 1: Write the failing home-route test**

Use `apply_patch` to create `frontend/tests/views/HomeView.spec.ts`:

```ts
import { mount } from '@vue/test-utils';
import { createMemoryHistory, createRouter } from 'vue-router';
import { describe, expect, it } from 'vitest';

import App from '@/App.vue';
import { routes } from '@/router';

describe('home route', () => {
  it('renders the project name at the root path', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes
    });

    await router.push('/');
    await router.isReady();

    const wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    });

    expect(wrapper.get('h1').text()).toBe('RPI GPIO Simple Controller');
  });
});
```

- [ ] **Step 2: Run the test and verify the Red state**

Run:

```powershell
Set-Location frontend
npm run test:unit -- tests/views/HomeView.spec.ts
Set-Location ..
```

Expected: FAIL because `routes` is empty and the mounted `RouterView` has no
`h1`; the failure must be an assertion/DOM lookup failure, not an import or
configuration error.

- [ ] **Step 3: Add the minimal home view**

Use `apply_patch` to create `frontend/src/views/HomeView.vue`:

```vue
<template>
  <main>
    <h1>RPI GPIO Simple Controller</h1>
  </main>
</template>
```

- [ ] **Step 4: Register the root route**

Use `apply_patch` to make `frontend/src/router/index.ts`:

```ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

import HomeView from '@/views/HomeView.vue';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
```

- [ ] **Step 5: Run the focused test and verify the Green state**

Run:

```powershell
Set-Location frontend
npm run test:unit -- tests/views/HomeView.spec.ts
Set-Location ..
```

Expected: one test passes; `/` resolves to `HomeView` and the `h1` text matches
exactly.

- [ ] **Step 6: Refactor only if the full quality gate stays green**

Run:

```powershell
Set-Location frontend
npm run check
npm run build
Set-Location ..
```

Expected: formatting, ESLint, type-check, unit test and production build all
exit 0. Keep the three-file route/view/test split; do not add a shared title
constant because it would add indirection for a single value.

- [ ] **Step 7: Verify the browser-visible result and capture evidence**

Run in `frontend/`:

```powershell
npm run dev -- --host 127.0.0.1
```

Open the printed local URL and verify:

```text
Rendered body content: RPI GPIO Simple Controller
Browser console errors: none
Additional navigation, tutorial copy, icons, buttons, or API requests: none
```

Capture one screenshot showing the page for the future Pull Request. Stop the
development server with Ctrl+C after inspection.

- [ ] **Step 8: Verify the scope and commit the home route**

Run:

```powershell
rg -n "HelloWorld|WelcomeItem|TheWelcome|AboutView|fetch\(|axios|/api" frontend/src frontend/tests
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --check
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' add -- frontend/src/router/index.ts frontend/src/views/HomeView.vue frontend/tests/views/HomeView.spec.ts
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --cached --check
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --cached --stat
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' commit -m "feat(frontend): add initial home route"
```

Expected: `rg` returns no matches; commit includes only the route, view and
test. The test proves the behavior without requiring a production web-history
server fallback.

---

### Task 3: 更新開發文件並完成可重現驗證

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 1 npm scripts and Node engine; Task 2 verified `/` behavior.
- Produces: developer instructions for `npm ci`, development, formatting, linting, type-checking, unit testing, the full quality gate, production build and preview.

- [ ] **Step 1: Replace the stale frontend command section in AGENTS.md**

Use `apply_patch` to replace the paragraph claiming `frontend/package.json`
is empty with:

````markdown
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
且不會修改檔案。
````

Expected: AGENTS no longer says npm commands are unavailable and documents
every script added by Task 1.

- [ ] **Step 2: Add the concise frontend workflow to README.md**

Use `apply_patch` to insert after the existing `Vue.js` and `FastAPI`
technology bullets and before `## 開發流程`:

````markdown
## 前端開發

前端需要 Node.js `^22.18.0 || >=24.12.0`，並統一使用 npm：

```shell
cd frontend
npm ci
npm run dev
```

提交前執行完整檢查與 production build：

```shell
npm run check
npm run build
```
````

Expected: README gives a fresh developer the shortest reproducible setup and
verification path without mentioning Yarn.

- [ ] **Step 3: Check documentation for stale or conflicting instructions**

Run:

```powershell
rg -n "package.json.*目前為空|尚未建立可執行|npm install|Yarn|yarn" AGENTS.md README.md
```

Expected: no stale empty-package statement, no `npm install` instruction for
developers, and no Yarn reference. `npm ci` is present in both files.

- [ ] **Step 4: Reinstall from the lockfile and run all final checks**

Run:

```powershell
Set-Location frontend
npm ci
npm run check
npm run build
Set-Location ..
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --check
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' status --short
```

Expected: all commands exit 0; `npm ci` reproduces the installation;
`frontend/dist/` and `frontend/node_modules/` remain ignored; no
`frontend-bootstrap/`, non-npm lockfile, tutorial file or API integration is
present. Unrelated pre-existing files remain untouched and unstaged.

- [ ] **Step 5: Commit only the developer documentation**

Run:

```powershell
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' add -- AGENTS.md README.md
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --cached --check
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' diff --cached --stat
git -c safe.directory='G:/Works/github_com/rpi_gpio_simple_ctrl' commit -m "docs: document frontend workflow"
```

Expected: final commit contains only `AGENTS.md` and `README.md`; implementation
history contains one toolchain commit, one tested home-route commit and one
documentation commit.
