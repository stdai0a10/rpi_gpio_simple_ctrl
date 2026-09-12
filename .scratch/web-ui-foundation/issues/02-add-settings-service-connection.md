# 02: 在 SETTINGS 提供 Service connection 檢查

**What to build:** 使用者進入 SETTINGS 時，可在既有 Appearance 設定旁看見一次
Service connection 檢查及其準確結果。UI 只描述 browser 可觀察到的 web application
liveness，而不將結果誤稱為 Raspberry Pi、GPIO 或硬體健康；失敗與拒絕時，使用者可自行
重新檢查。

**Blocked by:** 01: 建立 Frontend shell 與 Appearance 設定.

**Status:** ready-for-agent

- [ ] 進入 SETTINGS 時啟動一次相對 `GET /health` 請求，初始顯示檢查中；有效的
  HTTP 200 與預期 payload 顯示 `服務可連線`。
- [ ] HTTP 403 顯示 `存取遭拒`；timeout、transport error、malformed payload 與其他
  非預期結果顯示 `服務無法連線`，且請求在五秒後中止。
- [ ] 失敗與拒絕狀態提供使用者觸發的 `重新檢查`；不輪詢、不自動重試、不快取跨頁結果，
  也不在 HOME、Sidebar、Drawer 或 Top Bar 顯示 global status。
- [ ] 結果使用可存取的文字與 semantic badge、icon 或 spinner 呈現，顏色不會是唯一的
  狀態傳達方式。
- [ ] 所有行為依 Red-Green-Refactor 開發，使用 browser boundary mocks 驗證可見結果；
  完整前端品質檢查、production build 與已核准的 Chrome 驗證通過。
