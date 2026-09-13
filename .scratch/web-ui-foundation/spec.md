Category: enhancement
Status: ready-for-agent

# Web UI foundation: HOME、SETTINGS 與服務連線

## Problem Statement

專案已有可提供 Vue SPA 的 FastAPI 應用程式與最小首頁，但尚未有一致的
Web UI foundation。使用者需要先取得可在手機與桌面使用的導覽殼層、可持久化的
theme 設定，以及對既有服務 liveness 的明確可見回饋；同時不得將尚未存在的
GPIO、Functions、Logs、Dashboard 或硬體狀態功能假裝為可用功能。

現有 liveness endpoint 只能證明 Web application 可否回應，不能證明
Raspberry Pi、GPIO 或硬體健康。因此 UI 必須用精確的 Service connection
語意呈現結果，並將存取遭拒與服務無法連線分開處理。

## Solution

交付一個 mobile-first Web UI foundation，僅包含 HOME 與 SETTINGS。HOME 保持
單一專案標題；SETTINGS 提供 Appearance 的 theme 設定與 Service connection
狀態。應用程式使用同一套 semantic design tokens 支援 Light、Dark 與 System
theme，並在 System 模式下即時跟隨作業系統偏好。

Desktop 使用固定 Sidebar，Mobile 使用 Top Bar 與 Navigation Drawer。導覽僅
列出 HOME 與 SETTINGS，沒有尚未交付功能的 placeholder。Service connection
只顯示在 SETTINGS，使用既有 `GET /health`，不新增後端 API、不輪詢、不快取歷史
結果，也不進行 GPIO 控制。

## Design References

本 tracker spec 是本期交付範圍、行為與測試邊界的 canonical specification。除非本
spec 明確覆寫或延後，實作應引用下列設計文件，而非重複複製其中的 token、版型或
元件規範：

- [Web UI Design Specification](../../docs/design-docs/ui/web-ui-design-spec.md)：
  應用程式殼層、共用元件、互動、accessibility 與 responsive direction。
- [Color & Theme Specification](../../docs/design-docs/ui/color-theme-spec.md)：
  semantic color 與 theme token 的規範來源；若與視覺圖例衝突，以此 Markdown
  specification 為準。
- [Color & Component Guide](../../docs/design-docs/ui/color-component-guide.png)：
  視覺輔助參考，不取代 Color & Theme Specification 的 token 規範。

本期明確覆寫設計文件中的完整初始介面範圍：只交付 HOME 與 SETTINGS、沒有 global
Service connection，且不交付 GPIO、Functions、Logs、Dashboard、Search、Theme quick
action 或 More menu。這些覆寫只限本期 scope，不會改寫設計文件中其他可適用的視覺
與互動規範。

## User Stories

1. As a trusted LAN user, I want to open the HOME page and see only the
   project title, so that the first screen does not imply unavailable device
   controls or telemetry.
2. As a desktop user, I want a stable Sidebar with only HOME and SETTINGS,
   so that I can navigate the delivered scope without encountering empty
   destinations.
3. As a mobile user, I want to open navigation from a Menu button, so that
   the UI fits a small screen without using a bottom navigation bar.
4. As a mobile user, I want the Drawer to close when I choose a navigation
   item or its overlay, so that navigation does not obstruct page content.
5. As a keyboard user, I want to close the Drawer with Escape and return
   focus to the Menu button, so that navigation remains predictable without
   a pointer.
6. As a mobile user, I want body scrolling locked while the Drawer is open,
   so that the overlay and its content remain visually coherent.
7. As a user, I want all UI labels except the product name to use Taiwan
   Traditional Chinese, so that settings are easy to understand.
8. As a user, I want the product name to remain `RPI GPIO Simple Controller`,
   so that the existing product identity and page heading remain stable.
9. As a user, I want to select System, Light, or Dark theme in SETTINGS, so
   that the interface suits my environment and preference.
10. As a user, I want the three theme choices to be visible, labelled, and
    easy to tap, so that I do not need to infer a hidden mode from an icon.
11. As a user, I want my explicit Light or Dark preference to survive a page
    reload, so that I do not need to reselect it every visit.
12. As a user who chooses System, I want the UI to follow operating-system
    theme changes while the page is open, so that the interface stays in
    sync with my system preference.
13. As a user with no valid saved preference, I want System to be used by
    default, so that the UI has a safe and understandable fallback.
14. As a low-light user, I want Dark theme to preserve the same information
    hierarchy and status meanings as Light theme, so that changing theme
    does not change the meaning of the UI.
15. As a user, I want UI controls to use sufficiently large touch targets
    and visible focus indicators, so that they work by touch and keyboard.
16. As a user, I want SETTINGS to use an Appearance section and rows rather
    than unrelated decorative cards, so that settings remain compact and
    scannable.
17. As a user entering SETTINGS, I want the application to check Service
    connection once, so that I can tell whether the Web service is reachable.
18. As a user waiting for that check, I want an explicit checking state, so
    that a missing result is not mistaken for a successful connection.
19. As a user, I want a valid liveness response to be labelled as service
    reachable, so that the UI accurately describes what the endpoint proves.
20. As a user outside the trusted network, I want an HTTP 403 response to be
    labelled as access denied, so that I do not mistake an access policy for
    a Raspberry Pi failure.
21. As a user facing a timeout, transport failure, malformed response, or
    unexpected response, I want a service-unavailable state, so that I know
    the current reachability result is not usable.
22. As a user facing a failed or denied connection check, I want a manual
    recheck action, so that I can try again after correcting my network or
    access context.
23. As a user, I do not want background polling or automatic retries, so
    that the first delivery does not create hidden client traffic or stale
    retry behaviour.
24. As a user, I do not want Service connection displayed globally in HOME,
    Sidebar, or Drawer during this scope, so that HOME remains minimal and
    the first API-backed information stays in SETTINGS.
25. As a user, I do not want GPIO, Functions, Logs, or Dashboard information
    represented as available before their own work is delivered, so that the
    UI does not overpromise functionality.
26. As a user, I want the same Service connection behavior in local
    development and production, so that the UI does not require a different
    backend origin configuration.
27. As a user, I want status to be communicated by text together with
    semantic color and optional iconography, so that color is never the only
    source of meaning.
28. As a user, I want the initial UI to avoid external font downloads, so
    that basic presentation does not depend on an unrelated remote service.
29. As a maintainer, I want a single outline icon system and shared semantic
    tokens, so that visual styles do not drift between HOME and SETTINGS.
30. As a tester, I want visible routing, navigation, theme, and Service
    connection behavior covered at the mounted application boundary, so that
    tests describe user-observable outcomes rather than implementation
    details.
31. As a reviewer, I want the reduced scope recorded explicitly, so that the
    approved visual direction is not later mistaken for a complete initial
    five-page implementation.

## Implementation Decisions

- The scope has exactly two client-side destinations: HOME and SETTINGS.
  Direct navigation to SETTINGS remains supported by the existing SPA
  history behavior.
- HOME renders `RPI GPIO Simple Controller` as its sole visible content
  heading. It has no dashboard data, controls, status information, Search,
  Theme quick action, More menu, or page-specific actions.
- SETTINGS contains two delivered sections: Appearance and Service
  connection. It does not render empty General, Server, GPIO, Advanced, or
  future-feature placeholders.
- All general UI copy uses Taiwan Traditional Chinese. The product name is
  the sole approved English product label; no i18n framework is introduced
  in this scope.
- The visual system uses global CSS custom properties for semantic tokens and
  component-local styles for component layout. No CSS framework, full UI
  component library, or second styling system is added.
- Components reference semantic roles rather than literal hexadecimal colors.
  Light and Dark themes preserve primary, success, warning, danger, info,
  text, surface, border, and focus semantics.
- The application uses System, Light, and Dark theme modes. System is the
  default and the fallback for absent or invalid browser storage. Explicit
  Light and Dark choices persist in browser-local storage.
- In System mode, the rendered theme listens for operating-system preference
  changes and updates without a page reload. Explicit Light or Dark choices
  take precedence over subsequent operating-system changes.
- Theme selection uses one accessible Radio group with three full-width,
  touch-friendly rows: 跟隨系統, 淺色, and 深色.
- The first delivery uses the approved CSS font stack with system fallbacks;
  it does not load a font from a CDN or bundle font files.
- A single Lucide Vue icon dependency provides the outline icons used by the
  delivered shell and feedback controls. Additional icon families are not
  introduced.
- At viewport widths below 1024px, the shell uses a Top Bar with Menu and
  title plus an off-canvas Drawer. At 1024px and above, it uses a fixed
  256px Sidebar and a minimal title-only Top Bar.
- The delivered navigation lists only HOME and SETTINGS. The shell does not
  render navigation items, disabled entries, Search, Theme quick actions,
  More menus, or global Service connection status for deferred features.
- Drawer behavior includes an overlay, overlay-click close, navigation-item
  close, Escape close, focus return to the originating Menu button, and body
  scroll locking while open.
- Interactive controls preserve visible keyboard focus, have at least a
  44px touch target, do not depend on hover to be operable, and respect
  reduced-motion preferences for nonessential transitions.
- Service connection is a user-facing liveness result, not a Raspberry Pi,
  GPIO, or hardware-health assertion.
- SETTINGS starts one Service connection request when entered. The request
  uses the existing relative `GET /health` contract, so local development
  uses the established proxy and production uses the same-origin service.
- A valid Service connection result is only HTTP 200 with the expected
  liveness payload. It is presented as 服務可連線.
- The Service connection state begins as 檢查中. A 403 response is presented
  as 存取遭拒. A timeout, transport error, malformed response, or other
  unexpected result is presented as 服務無法連線.
- The Service connection request has a five-second client timeout. It does
  not poll, automatically retry, retain cross-page history, or display
  telemetry. Failed and denied states offer a user-triggered 重新檢查 action.
- Service connection is presented as a SETTINGS section containing a single
  row with text, semantic badge or icon, and a checking spinner when needed.
  It is deliberately absent from HOME, Sidebar, and Drawer in this scope.
- The frontend consumes the existing liveness endpoint only. It does not
  add, change, or call business API routes, and it does not make backend,
  GPIO, authentication, authorization, CORS, or trusted-IP behavior changes.
- GPIO, Functions, Logs, Dashboard system information, full initial
  navigation, global ConnectionStatus, and all hardware controls are
  explicitly deferred. They require their own approved specification before
  becoming visible or interactive.

## Testing Decisions

- Development follows the repository's Red-Green-Refactor process. Each
  behavior begins with a failing test that asserts observable user behavior,
  followed by the smallest implementation needed to pass it.
- The primary frontend test seam is a mounted root Vue application using its
  real route records and an in-memory browser history. This extends the
  existing HOME route testing style at the highest available frontend seam.
- Browser-bound dependencies are replaced only at their boundaries: browser
  storage for persisted theme preferences, system-theme media queries for
  System mode, and network fetch for Service connection responses.
- Route tests cover HOME and SETTINGS, the sole HOME heading, absence of
  deferred navigation destinations, and direct SETTINGS navigation.
- Shell tests cover the breakpoint-specific navigation contract and Drawer
  behavior: open, overlay close, navigation close, Escape close, focus
  restoration, and scroll-lock cleanup.
- Theme tests cover the three visible choices, default/fallback System mode,
  persisted explicit preferences, immediate System-mode changes, semantic
  theme application, and accessible selection behavior.
- Service connection tests cover checking, valid liveness success, 403 access
  denied, timeout, transport or malformed-response failure, manual recheck,
  lack of automatic retry, and absence of a global status display.
- Tests assert rendered text, accessible roles, user-triggered effects, and
  public HTTP outcomes. They do not assert private component state, internal
  CSS variable names, framework lifecycle calls, or implementation-specific
  timer details.
- Delivery verification includes the complete frontend quality command,
  production build, whitespace validation, and Chrome checks at Desktop and
  Mobile viewports. Chrome checks cover Drawer keyboard behavior, System
  theme changes, and every Service connection visual state without relying
  on manually supplied screenshots.

## Out of Scope

- GPIO, Function, or Log routes, views, navigation items, fixtures, controls,
  editors, drag-and-drop interactions, and hardware actions.
- Dashboard cards, Raspberry Pi temperature, CPU, memory, uptime, activity,
  quick actions, or any other telemetry.
- Any API other than the existing relative `GET /health` liveness request.
- Backend endpoint, data model, middleware, trusted-IP, CORS, authentication,
  authorization, deployment, or hardware changes.
- Global Service connection display in HOME, Sidebar, Drawer, or Top Bar.
- Search, Theme quick actions, More menus, breadcrumbs, bottom navigation,
  empty future-feature placeholders, and global notifications unrelated to
  the delivered settings flow.
- Background polling, automatic retry, request history, health metrics,
  caching, or a claim that liveness proves device or hardware health.
- CDN fonts, bundled fonts, a CSS framework, a broad UI component library,
  a second icon library, or an i18n framework.
- A custom frontend error page, server-side rendering, a second production
  web server, or changes to the SPA serving contract.

## Further Notes

- `Service connection` is the project glossary term for application liveness
  observed by the browser. It must not be relabelled as Raspberry Pi online,
  GPIO healthy, or hardware status.
- This is a deliberate partial delivery of the approved Web UI direction.
  Deferred navigation and Dashboard requirements are not rejected; they are
  reserved for later approved work.
- This tracker entry is the canonical specification for the initial Web UI
  foundation. Follow-on implementation tickets must preserve its scope and
  test seams.
- The referenced design documents must be present in this branch's eventual
  documentation commit so the canonical specification retains resolvable
  source references.
