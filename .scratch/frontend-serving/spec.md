Category: enhancement
Status: ready-for-agent

# FastAPI 提供 Vue 編譯前端規格

## Problem Statement

專案的 Vue 前端與 FastAPI 後端以獨立原始碼與開發流程維護，但正式部署需要讓使用者僅透過 Uvicorn 存取同一個 HTTP 服務。現有後端已提供 `/health`、OpenAPI 文件與 socket-peer trusted-IP 限制；若以手寫 catch-all 提供 SPA，容易誤將遺失的靜態資產或未知的 API URL 回傳為 `index.html`，也會重複實作靜態路徑安全與瀏覽器導覽判斷。

使用者需要由 FastAPI 載入已編譯的 Vue 靜態產物，同時維持前後端原始碼分離、既有 backend HTTP 契約與 trusted-IP 安全界線。Raspberry Pi 型號僅作為使用者選擇部署方式時的參考，不構成效能或相容性保證。

## Solution

正式服務由 Uvicorn 執行既有 FastAPI application，並使用目前釘選 FastAPI 版本內建的 frontend serving 能力提供 repository root 的 Vue build output。Vue SPA 位於 `/`；既有一般 path operation 優先處理，只有未匹配的合格瀏覽器導覽才會由 `index.html` 回應。已編譯的 JavaScript、CSS、圖片與其他實體檔案由同一個 frontend serving 機制提供，遺失的靜態資產保持 `404`。

frontend serving 遵守既有 trusted-IP middleware，因此靜態檔案、SPA route、health check、OpenAPI 與文件頁都在相同的來源限制下。應用程式在 lifespan 先驗證 Settings，再確認 frontend bundle 目錄與 `index.html` 可用，兩者皆成功後才開始接受請求。Vue build output 是部署產物，維持不納入 Git；文件提供多種產生與交付方式，但正式 runtime 都期待相同位置的 bundle 已存在。

## User Stories

1. As a trusted LAN user, I want to open `/` through Uvicorn and receive the Vue application, so that I do not need a second production web server.
2. As a trusted LAN user, I want compiled JavaScript, CSS, images, and other frontend files to load from the same origin as the application, so that the SPA can start normally.
3. As a Vue SPA user, I want to directly open or refresh a client-side route, so that browser navigation remains usable when history mode is used.
4. As a browser user, I want a missing JavaScript, CSS, image, or other physical frontend asset to return `404`, so that broken deployments are visible instead of silently loading the SPA shell.
5. As an API consumer, I want an unknown `/api/...` URL to return FastAPI's normal JSON `404`, so that an API typo is never treated as a frontend page.
6. As an operator, I want `/health` to retain its exact existing success response, so that current monitoring and smoke checks continue to work unchanged.
7. As an API explorer, I want `/docs`, `/redoc`, and `/openapi.json` to keep their existing behavior, so that frontend delivery does not hide backend documentation.
8. As a network administrator, I want frontend routes and assets to obey `TRUSTED_IP_RANGES`, so that serving the UI does not create a second, less restricted access path.
9. As an untrusted requester, I want every frontend and backend HTTP request to receive the existing fixed `403` response, so that source restrictions remain uniform.
10. As a deployer, I want Uvicorn startup to fail clearly when the frontend bundle or its `index.html` is absent, so that an incomplete deployment is detected before users receive traffic.
11. As a deployer, I want the failure to identify the expected frontend bundle location and remediation, so that I can build or copy the correct artifact without exposing sensitive configuration.
12. As a Windows-based builder, I want to build and check the frontend outside the Raspberry Pi and copy only the compiled bundle, so that deployment need not install Node.js on the target device.
13. As a Raspberry Pi operator, I want an alternative documented way to build the frontend on the device, so that I can choose a self-contained workflow when a compatible Node.js installation is available.
14. As a release manager, I want to deploy a release archive containing source and the compiled bundle but no dependency directories, virtual environment, `.env`, or runtime data, so that the archive is portable and does not carry secrets or platform-specific state.
15. As a deployer, I want each transferred frontend bundle to come from the same checkout or release as the backend, so that the two parts do not accidentally drift apart.
16. As a repository maintainer, I want compiled frontend output to remain ignored by Git, so that source code and generated artifacts do not require duplicate version control.
17. As a frontend developer, I want to use Vite's dev server on loopback during local development, so that I retain fast feedback without exposing a development proxy to the LAN.
18. As a frontend developer, I want `/health` and future `/api/...` calls to use relative URLs and be proxied to local Uvicorn during development, so that production and development do not require different backend origins in frontend code.
19. As a backend developer, I want documentation pages to remain directly available from Uvicorn instead of being proxied through Vite, so that the development proxy has a small, explicit interface.
20. As a test author, I want to construct an application with a temporary frontend bundle, so that backend HTTP tests do not depend on Node.js, a committed build artifact, or a developer's local `dist` directory.
21. As a test author, I want to test frontend serving through the application factory and HTTP client, so that tests verify externally observable routing, lifecycle, security, and response behavior rather than private file-handling details.
22. As a maintainer, I want frontend serving, bundle validation, and default bundle-location knowledge concentrated in one focused module, so that the application factory remains an assembly point and later changes have good locality.
23. As a maintainer, I want deployment instructions summarized in the README and detailed in a dedicated deployment document, so that common usage is easy to find while alternative delivery procedures remain clear.
24. As a project owner, I want Uvicorn to remain the only production web server, so that this phase does not introduce Nginx, Caddy, a CDN, or another reverse proxy.

## Implementation Decisions

- Use FastAPI's built-in frontend serving interface, available in the project's pinned FastAPI version, rather than a hand-written `StaticFiles` mount plus catch-all path operation.
- Serve the Vue build at `/` with `index.html` as the SPA fallback. FastAPI's normal path operations retain priority over frontend delivery.
- Keep `/health`, `/docs`, `/redoc`, and `/openapi.json` unchanged. Do not move health check to `/api`.
- Reserve `/api` for future business HTTP routes. Unmatched `/api` paths, including the namespace root, must produce FastAPI's default JSON `404` instead of SPA fallback output.
- Keep Vite's root deployment base. The current frontend is served at `/`, not a subpath such as `/app`.
- Add one focused frontend-serving module. It owns the default build-output location, validates that the output directory and `index.html` exist, and registers frontend serving on an application.
- Keep the application factory as the composition seam. It gains an optional frontend-directory input for tests; runtime construction uses the fixed repository-relative output directory and does not add an environment variable or CLI setting for that location.
- Validate frontend availability during lifespan startup rather than import time. This preserves importability for test setup while causing Uvicorn startup to fail before it accepts requests when the required bundle is absent.
- Lifespan validates application Settings first, validates the frontend bundle second, then stores active Settings, logs startup, and accepts requests. Shutdown behavior remains unchanged apart from the existing lifecycle logging.
- Do not require a particular hashed asset filename or asset subdirectory at startup. `index.html` is the required SPA entry point; asset names are build-output details.
- Continue using the existing pure ASGI trusted-IP middleware without a frontend-specific exception. It applies before routing to frontend files, SPA fallback, API routes, health check, and documentation.
- Configure Vite development serving to bind only to `127.0.0.1`. It proxies `/health` and `/api` to local Uvicorn, but does not proxy documentation routes.
- Do not add CORS configuration. Production uses a same-origin frontend and backend, and local development uses the Vite proxy.
- Do not add custom compression or cache policy in this phase. Use FastAPI's normal static file behavior and Vite's fingerprinted build assets; reassess only after measured performance evidence.
- Keep compiled output ignored by Git. Document three deployment choices: build on a compatible Raspberry Pi environment, build elsewhere and copy the output, or deploy an archive that contains source plus the output. The latter two are recommended for resource-constrained targets.
- The release archive workflow is documentation only. Do not add an archive-generation script, a release publishing system, or runtime frontend/backend version matching in this phase.
- Document that a transferred bundle and backend source must come from the same checkout or release. Do not add a Git SHA, version manifest, or runtime compatibility check in this phase.
- Add concise deployment guidance to the README and place detailed, platform-aware procedures in a dedicated deployment document. Raspberry Pi model references are informational only and must not imply unverified compatibility or performance claims.

## Testing Decisions

- The primary test seam is the public application factory exercised through an HTTP client. Existing backend route and trusted-IP tests establish the preferred style: inject valid Settings, enter lifespan through the client context, and assert HTTP status, headers, and response bodies.
- Tests create a minimal temporary frontend distribution containing `index.html` and representative files. They do not invoke Vite or depend on an ignored working-tree bundle.
- Backend tests cover a trusted client loading the SPA root, an actual static asset, and a history-mode route. They assert that the existing health and documentation behavior remains available to trusted clients.
- Backend tests cover a missing frontend asset, non-HTML frontend request, and unknown `/api` path returning `404` rather than the SPA shell.
- Backend tests cover untrusted clients receiving the established fixed `403` response for frontend root, static assets, SPA routes, health, documentation, and API paths.
- Backend tests cover lifespan failure when the temporary distribution lacks the directory or required `index.html`, while preserving the existing Settings validation behavior and health response format.
- Frontend configuration tests or equivalent configuration-level verification confirm that Vite binds to loopback and proxies only `/health` and `/api` to the local Uvicorn target. Frontend quality checks remain `npm run check`; the deployment build verification remains `npm run build`.
- Deployment documentation verification confirms each documented workflow excludes `node_modules`, virtual environments, `.env`, and runtime data from artifacts, and states the same-revision requirement.
- Tests verify public outcomes and error contracts, not private path-resolution helpers, FastAPI route-registration order, logger invocation counts, or implementation-specific static-file classes.

## Out of Scope

- Nginx, Caddy, a CDN, reverse proxy configuration, or any second production web server.
- Server-side rendering, prerendering, or a Node.js frontend server in production.
- GPIO Function behavior, pigpio access, JSON/YAML/SQLite business storage, authentication, authorization, or CORS.
- A new frontend page, new client-side business route, or changes to the existing frontend shell content.
- Changing the `/health` response, moving it below `/api`, or changing OpenAPI and documentation URLs.
- Custom API error schemas, custom frontend 404 pages, or a runtime frontend/backend version manifest.
- Custom cache headers, gzip/Brotli compression, performance tuning, or Raspberry Pi compatibility and throughput claims.
- Committing `dist`, archiving scripts, release publishing automation, CI/CD, systemd configuration, or deployment-data migration.

## Further Notes

- Uvicorn remains the only production web server. Vite's dev server is an optional local development tool and is not a deployed service.
- The frontend source and backend source remain separate. Only the compiled frontend output is made available to the FastAPI application at runtime.
- Existing backend initialization and frontend initialization specs remain historical, completed work and are not modified by this feature.
- This spec records the approved design. It must be decomposed into Local Markdown tickets before implementation, and implementation must follow the repository's Red-Green-Refactor process.
