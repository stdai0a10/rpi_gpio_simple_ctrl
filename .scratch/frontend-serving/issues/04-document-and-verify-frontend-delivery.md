# 04: 文件化並驗證 frontend delivery

**Category:** enhancement

**What to build:** 讓部署者可依需求選擇建置位置與交付方式，並取得與實際 Uvicorn frontend delivery 一致的文件和整合驗證結果。

**Blocked by:** 01: 透過 Uvicorn 提供 Vue bundle；02: 保留 API 與 trusted-IP 契約；03: 設定 loopback Vite 開發 proxy。

**Status:** ready-for-agent

- [ ] README 提供摘要，專屬部署文件完整說明 Pi 建置、外部建置後複製，以及含 bundle release archive 三種流程。
- [ ] 文件說明 bundle 與 backend 必須來自同一 checkout 或 release，並排除 dependency directories、virtual environment、`.env` 與 runtime data；Raspberry Pi 型號僅供參考。
- [ ] 執行 frontend quality/build、backend tests 與 Uvicorn static/health smoke test，並記錄實際結果與未驗證的平台界線。
