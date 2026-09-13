# 01: 建立 Frontend shell 與 Appearance 設定

**What to build:** 使用者可在 HOME 與 SETTINGS 間使用完整、responsive 的
Frontend shell；HOME 只呈現產品標題，SETTINGS 提供可操作的 Appearance theme
設定。使用者可在 System、Light、Dark 間選擇，明確偏好會保存，System 則在頁面開啟時
跟隨作業系統偏好；桌面與手機使用相應的導覽方式，且沒有尚未交付功能的入口或狀態。

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [x] HOME 與 SETTINGS 都可由真實路由到達，導覽只顯示 HOME 與 SETTINGS，且 HOME
  只顯示 `RPI GPIO Simple Controller` 標題。
- [x] Desktop Sidebar 與 mobile Top Bar／Drawer 遵守已核准的 breakpoint、關閉、焦點
  回復、scroll lock、touch target、focus 與 reduced-motion 行為。
- [x] SETTINGS 的 Appearance 區塊以可存取的三選一控制項提供 跟隨系統、淺色、深色；
  無效或缺失的儲存值安全回退為 System，且 System mode 會即時反映系統偏好變更。
- [x] 視覺實作遵守本 feature spec 引用的 semantic token、字型、outline icon 與
  Light／Dark 語意規範，不引入 CDN 字型、第二套 icon 或 styling system。
- [x] 所有行為依 Red-Green-Refactor 開發，並由 mounted application seam 的自動化
  測試驗證；完整前端品質檢查通過。
