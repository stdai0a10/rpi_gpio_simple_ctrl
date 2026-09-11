# 03: 設定 loopback Vite 開發 proxy

**Category:** enhancement

**What to build:** 讓本機前端開發可安全地透過 loopback-only Vite dev server 使用相對 backend URL，同時不將開發 proxy 暴露給區域網路。

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] Vite dev server 只綁定 loopback，且只將 `/health` 與 `/api` 代理至本機 Uvicorn。
- [ ] frontend 可透過相對 URL 使用被代理的 backend paths，不需硬編碼 backend host 或 port。
- [ ] backend 文件 routes 不經由 Vite proxy，仍直接由 Uvicorn 提供。
