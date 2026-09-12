# 01: 透過 Uvicorn 提供 Vue bundle

**Category:** enhancement

**What to build:** 讓受信任來源可透過同一個 Uvicorn application 取得已編譯的 Vue SPA root、實體資產與 history-mode 導覽；若必要的 SPA entry bundle 缺失，服務在開始接受請求前明確失敗，同時保留既有 health 與文件行為。

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] 受信任來源可取得 SPA root、實際前端資產與 HTML 導覽 fallback；遺失實體資產維持 `404`。
- [ ] 不完整的 frontend bundle 會使 lifespan 啟動失敗；完整 bundle 啟動後既有 `/health`、`/docs`、`/redoc` 與 `/openapi.json` 行為不變。
- [ ] 後端測試使用 temporary frontend distribution 驗證公開 HTTP 與 lifecycle 行為，不依賴 Vite build 或工作樹中的 `dist`。
