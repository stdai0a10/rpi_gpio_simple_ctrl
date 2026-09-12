# 02: 保留 API 與 trusted-IP 契約

**Category:** enhancement

**What to build:** 讓 frontend delivery 不會接管 backend namespace，並讓 SPA、資產、API 與文件 routes 維持相同的 trusted-IP 存取規則。

**Blocked by:** 01: 透過 Uvicorn 提供 Vue bundle。

**Status:** ready-for-agent

- [ ] 未知 `/api` 路徑回傳 FastAPI 預設 JSON `404`，不會取得 SPA fallback。
- [ ] 未受信任來源存取 SPA root、實體資產、SPA route、API 與文件 routes 時，皆得到既有固定 `403` 回應。
- [ ] 已註冊的 backend routes 對受信任來源保持既有公開回應契約。
