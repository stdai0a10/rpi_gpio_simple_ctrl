# Raspberry Pi GPIO Simple Controller
# Web UI Design Specification

版本：Draft v0.1

---

## 1. 文件目的

本文件定義 Raspberry Pi GPIO Simple Controller 的 Web UI 整體視覺、版面、導覽、響應式行為與共用元件設計原則。

本規格的目標是：

- 即使沒有任何圖片、Wireframe 或 Mockup，設計師仍能理解 UI 的預期結構。
- 手機為主要瀏覽裝置，Desktop 為次要裝置。
- 所有主要操作都必須適合觸控。
- 網站應呈現「現代 Web Dashboard」風格，而不是模仿原生手機 App。
- 所有頁面應共用一致的 Layout、Spacing、Typography、Color 與 Interaction Pattern。
- 支援 Light Mode 與 Dark Mode。
- 與常見 Web Design System 保持高相容性。

---

# 2. 產品定位

本系統是一個透過 Web 操作 Raspberry Pi GPIO 的控制介面。

主要使用情境：

- 查看 Raspberry Pi 系統狀態。
- 查看 GPIO 狀態。
- 控制 GPIO 輸出。
- 編輯 Functions。
- 查看執行紀錄。
- 修改系統設定。

UI 應給人的感覺：

- 簡潔。
- 技術感。
- 穩定。
- 清楚。
- 高效率。
- 適合長時間使用。

不應呈現：

- 過度活潑。
- 遊戲化。
- 大量裝飾性圖片。
- 強烈擬物設計。
- 過度 Glassmorphism。
- 大面積 Gradient。
- 類似手機原生 App 的 Bottom Navigation。

---

# 3. 核心設計原則

## 3.1 Mobile First

所有 UI 優先以手機尺寸思考。

設計流程應以：

```text
Mobile
→ Tablet
→ Desktop
→ Large Desktop
```

的順序進行。

Desktop 版本不是重新設計一套 UI，而是將 Mobile UI 延伸到較大的空間。

---

## 3.2 Web First

即使主要使用手機瀏覽，整體仍應具有 Web Application 的視覺與操作邏輯。

手機版不得使用：

- Bottom Navigation Bar。
- Bottom Tab Bar。
- 固定底部主選單。
- iOS / Android 原生 App 式操作框架。

手機版主要 Navigation Pattern 為：

```text
Top Bar
+
Navigation Drawer
+
Main Content
```

---

## 3.3 Minimal Text

UI 中盡量減少不必要文字。

例如不應顯示：

```text
Click this button to turn GPIO 17 on.
```

應顯示：

```text
GPIO 17
LED
HIGH
```

必要說明可透過：

- Tooltip。
- Help。
- Empty State。
- Contextual Hint。

提供。

---

## 3.4 Icon First，但不能只靠 Icon

常用操作可優先使用 Icon。

例如：

```text
Search
Theme
More
Edit
Delete
Refresh
Menu
```

但對第一次使用不容易辨識的功能，不應只顯示 Icon。

例如主要 Navigation 應使用：

```text
[Icon] GPIO
[Icon] Functions
[Icon] Logs
```

而不是只有 Icon。

---

# 4. 整體 Layout

網站使用統一的 Application Shell。

主要結構：

```text
Application
├── Sidebar / Navigation Drawer
├── Top Bar
├── Main Content
├── Dialog Layer
├── Toast Layer
└── Overlay Layer
```

---

# 5. Desktop Layout

Desktop 畫面由左至右分為：

```text
Sidebar
+
Main Area
```

Main Area 再分成：

```text
Top Bar
+
Page Content
```

結構：

```text
┌──────────────┬──────────────────────────────────┐
│              │ Top Bar                          │
│              ├──────────────────────────────────┤
│              │                                  │
│   Sidebar    │                                  │
│              │          Page Content            │
│              │                                  │
│              │                                  │
│              │                                  │
└──────────────┴──────────────────────────────────┘
```

---

# 6. Desktop Sidebar

Sidebar 固定於畫面左側。

建議寬度：

```text
240px ~ 260px
```

預設建議：

```text
256px
```

Sidebar 高度：

```text
100vh
```

Sidebar 本身不隨 Main Content 捲動。

Sidebar 結構由上至下：

```text
Logo / Product Name

Primary Navigation

Secondary Navigation

Spacer

System Status
```

例如：

```text
Raspberry Pi GPIO

Home
GPIO
Functions
Logs

Settings

● Online
```

---

# 7. Sidebar Navigation Item

Navigation Item 結構：

```text
Icon
+
Label
```

單一 Navigation Item 高度建議：

```text
44px ~ 48px
```

左右 Padding：

```text
12px ~ 16px
```

狀態：

```text
Default
Hover
Active
Focus
Disabled
```

Active Item 應有清楚但不過度強烈的背景色。

建議：

```text
淡 Primary Background
+
Primary Color Icon
+
Primary / Strong Text
```

不要只使用文字顏色表示 Active。

---

# 8. Mobile Layout

Mobile 不顯示固定 Sidebar。

畫面基本結構：

```text
┌────────────────────────────┐
│ ☰   Page Title        ⋮    │
├────────────────────────────┤
│                            │
│                            │
│        Main Content        │
│                            │
│                            │
└────────────────────────────┘
```

---

# 9. Mobile Navigation Drawer

按下 Top Bar 左側 Menu Button 後，從畫面左側顯示 Navigation Drawer。

Pattern：

```text
Off-canvas Navigation Drawer
```

Drawer 寬度：

```text
約 80vw
```

但最大寬度：

```text
320px
```

建議 CSS 邏輯：

```text
min(82vw, 320px)
```

Drawer 顯示時：

- Main Content 保持原位置。
- Drawer 從左側滑入。
- 其餘畫面覆蓋半透明 Overlay。
- 點擊 Overlay 關閉 Drawer。
- 點擊 Navigation Item 後自動關閉 Drawer。
- ESC 可關閉。
- Drawer 關閉後 Focus 回到原 Menu Button。

---

# 10. Top Bar

Top Bar 為所有頁面共同存在的主要橫向區域。

高度：

```text
56px ~ 64px
```

建議：

```text
60px
```

---

# 11. Desktop Top Bar

Desktop Top Bar：

```text
┌──────────────────────────────────────────────┐
│ Page Title              Search  Theme   ⋮   │
└──────────────────────────────────────────────┘
```

左側：

- Page Title。
- Optional Breadcrumb。

右側：

- Page-level Action。
- Search。
- Theme。
- More Menu。

避免一次出現超過 4 個 Icon Button。

---

# 12. Mobile Top Bar

Mobile Top Bar：

```text
┌────────────────────────────┐
│ ☰   Page Title        ⋮    │
└────────────────────────────┘
```

左側：

```text
Menu Button
```

中央或左側：

```text
Page Title
```

右側：

```text
Page Action
或
More Menu
```

手機版應避免塞入過多 Action。

如果 Action 超過 2 個：

```text
保留最重要操作
+
More Menu
```

---

# 13. Content Container

Page Content 使用統一 Container。

Mobile：

```text
16px horizontal padding
```

Tablet：

```text
20px ~ 24px
```

Desktop：

```text
24px ~ 32px
```

Large Desktop：

Main Content 最大建議寬度：

```text
1440px
```

可置中。

但以下頁面可以使用 Full Width：

- GPIO Grid。
- Functions Editor。
- Logs。
- Table-heavy pages。

---

# 14. Breakpoints

初步 Breakpoint：

```text
Mobile:
< 768px

Tablet:
768px ~ 1023px

Desktop:
1024px ~ 1439px

Large Desktop:
>= 1440px
```

切換 Sidebar 的主要 breakpoint：

```text
1024px
```

也就是：

```text
< 1024px
Navigation Drawer

>= 1024px
Fixed Sidebar
```

---

# 15. Color Philosophy

整體使用低飽和中性色作為基礎。

Primary Color 僅用於：

- Active。
- Primary Action。
- Focus。
- Selected。
- 強調狀態。

避免整頁充滿品牌色。

---

# 16. Semantic Color

禁止 Component 直接依賴固定 Hex Color。

應使用 Semantic Token：

```text
primary

success
warning
danger
info

background
surface
surface-raised

text-primary
text-secondary
text-muted

border
divider
focus
```

---

# 17. Light Mode

Light Mode 基本結構：

```text
Page Background
→ 淺灰 / Off-white

Surface
→ White

Raised Surface
→ White + subtle shadow

Primary Text
→ Near Black

Secondary Text
→ Medium Gray
```

建議視覺關係：

```text
Background
#F7F8FA 類型

Surface
#FFFFFF

Text
#111827 類型
```

實際顏色可由設計師調整。

---

# 18. Dark Mode

Dark Mode 不使用：

```text
#000000
```

作為主要背景。

建議：

```text
Background
#0F1115 類型

Surface
#171A21 類型

Raised Surface
#1E222B 類型
```

文字：

```text
Primary
接近白色

Secondary
中度灰色
```

Dark Mode 主要透過：

```text
Surface Brightness Difference
```

建立階層。

避免大量亮色 Border。

---

# 19. Typography

英數主要字型：

```text
Inter
```

中文：

```text
Noto Sans TC
```

Fallback：

```text
system-ui
-apple-system
BlinkMacSystemFont
Segoe UI
sans-serif
```

---

# 20. Typography Scale

建議只使用少數明確層級。

Page Title：

```text
Desktop: 24px
Mobile: 20px
Weight: 600
```

Section Title：

```text
18px
600
```

Card Title：

```text
15px ~ 16px
600
```

Body：

```text
14px
400
```

Secondary：

```text
13px
400
```

Caption：

```text
12px
400
```

不要過度使用大字。

---

# 21. Spacing

使用 4px Grid System。

Spacing Token：

```text
4px
8px
12px
16px
20px
24px
32px
40px
48px
```

最常使用：

```text
8px
12px
16px
24px
```

---

# 22. Standard Page Spacing

建議：

Page Padding：

```text
Mobile
16px

Tablet
24px

Desktop
24px ~ 32px
```

Section 間距：

```text
24px ~ 32px
```

Card Gap：

```text
12px ~ 16px
```

Card Padding：

```text
16px
```

大型 Card：

```text
20px ~ 24px
```

---

# 23. Radius

Rounded Corner 保持現代感，但避免過度。

建議：

```text
Small Control
6px

Button / Input
8px

Card
10px ~ 12px

Dialog
12px ~ 16px
```

禁止所有元件都使用極大圓角。

---

# 24. Shadow

Shadow 應非常克制。

優先使用：

```text
Background Difference
+
Border
```

只有以下元件適合較明顯 Shadow：

- Dialog。
- Drawer。
- Dropdown。
- Floating Toast。

Card 不應呈現很重的浮空效果。

---

# 25. Icon System

所有功能 Icon 優先使用 SVG。

建議 Icon Library：

```text
Lucide
```

替代：

- Material Symbols。
- Heroicons。

同一產品中避免混用多套 Icon Style。

---

# 26. Icon Style

使用：

```text
Outline Icon
```

預設尺寸：

```text
16px
20px
24px
```

常用 Button Icon：

```text
20px
```

Navigation：

```text
20px
```

Decorative / Empty State：

```text
32px ~ 48px
```

---

# 27. Touch Target

所有主要互動元件點擊區域至少：

```text
44 × 44px
```

推薦：

```text
48 × 48px
```

即使 Icon 本身只有：

```text
20 × 20px
```

Button Hit Area 仍需達到 44px。

---

# 28. Buttons

Button 類型：

```text
Primary
Secondary
Ghost
Danger
Icon Button
```

同一區域原則上只有一個 Primary Action。

例如：

```text
Save
```

可以是 Primary。

而：

```text
Cancel
Duplicate
More
```

應為 Secondary / Ghost。

---

# 29. Primary Button

視覺：

```text
Primary Background
+
White / Contrast Text
```

用途：

- Save。
- Create。
- Apply。
- Confirm。

不可將一般 Navigation 按鈕全部設成 Primary。

---

# 30. Ghost Button

用於：

- Toolbar。
- More Action。
- Secondary Action。
- Compact UI。

例如：

```text
Refresh
Edit
Close
More
```

---

# 31. Icon Button

Icon Button 必須有：

```text
Tooltip
或
aria-label
```

例如：

```text
Refresh
Delete
More
Menu
```

Desktop Hover 時應顯示 Tooltip。

---

# 32. Form Inputs

Input 高度：

```text
40px ~ 44px
```

Mobile 可使用：

```text
44px ~ 48px
```

Label 必須位於 Input 上方。

不應只依賴 Placeholder 表示欄位名稱。

---

# 33. Card

Card 是主要資訊容器。

標準 Card：

```text
┌─────────────────────┐
│ Title        Action │
│                     │
│ Content             │
│                     │
└─────────────────────┘
```

應避免在一個 Card 裡加入過多層 Card。

---

# 34. GPIO Card

Desktop GPIO 建議使用 Grid Card。

結構：

```text
┌────────────────────────┐
│ [Icon] GPIO 17      ⋮  │
│        Living LED      │
│                        │
│ OUTPUT · HIGH   [ON]   │
└────────────────────────┘
```

主要資訊：

1. GPIO Number。
2. User-defined Name。
3. Direction。
4. State。
5. Control。
6. More Action。

---

# 35. GPIO Mobile Item

Mobile 應改成 Compact List Card。

例如：

```text
┌────────────────────────────┐
│ ● GPIO 17           [ON]   │
│   Living LED               │
│   OUTPUT · HIGH        ⋮   │
└────────────────────────────┘
```

高度盡量控制在：

```text
72px ~ 96px
```

避免手機版每一個 GPIO 都成為很高的大 Card。

---

# 36. GPIO State

狀態需同時使用：

```text
Color
+
Text
+
Optional Icon
```

例如：

```text
● HIGH
● LOW
● ERROR
```

不得只用：

```text
Green Dot
Red Dot
```

傳達狀態。

---

# 37. Switch

Boolean GPIO 輸出可以使用 Switch。

Switch 狀態：

```text
ON
OFF
Disabled
Loading
```

操作後若 Server 尚未回覆，Switch 可進入暫時 Loading 狀態。

Server 確認成功後才視為真正完成。

---

# 38. Dashboard

Home Dashboard 應以快速查看狀態為主。

內容可包含：

```text
System Status

GPIO Summary

Recent Activity

Quick Actions
```

不要放過度詳細的設定。

---

# 39. System Status

推薦顯示：

```text
Temperature
CPU
Memory
Uptime
```

Desktop：

```text
[Temperature] [CPU] [Memory] [Uptime]
```

Mobile：

```text
[Temperature] [CPU]
[Memory]      [Uptime]
```

或依可讀性調整為水平小卡。

---

# 40. Functions 頁面

Functions 頁面主要分成：

```text
Functions List
+
Function Editor
```

Functions List 負責：

- 顯示所有 Function。
- 新增 Function。
- 開啟 Function。
- 刪除 / Duplicate 等操作。

---

# 41. Function List Item

Function 項目建議：

```text
┌──────────────────────────────┐
│ Function Name            ⋮   │
│ Brief metadata               │
└──────────────────────────────┘
```

不要在 List 直接顯示完整 JSON。

---

# 42. Function Editor

點擊 Function 或新增 Function 後開啟 Editor。

Desktop：

使用：

```text
Large Modal
或
Near Full-screen Dialog
```

建議尺寸：

```text
width:
min(1200px, calc(100vw - 48px))

height:
calc(100vh - 48px)
```

Mobile：

直接使用：

```text
Full-screen Dialog
```

---

# 43. Function Editor Header

Header：

```text
Function Name

Mode Switch

Save

Close
```

模式：

```text
UI
JSON
```

預設：

```text
UI
```

---

# 44. Function Editor — UI Mode

UI Mode 由多個 Section 組成。

例如：

```text
Basic

Uses

Commands
```

Uses 每一項可獨立展開 / 收合。

Pattern：

```text
Accordion
```

---

# 45. Commands

Commands 以垂直列表呈現。

例如：

```text
Command 1
Command 2
Command 3
+ Add Command
```

新增按鈕必須放：

```text
最後一個 Command 後方
```

而不是放在 Section Header。

---

# 46. Command Sorting

Command 可使用 Drag & Drop 調整順序。

拖曳 Handle：

```text
⠿
```

放在每個 Command 左側或右側。

Mobile Drag Area 必須足夠大。

---

# 47. JSON Mode

JSON Mode 使用 Code Editor。

必須支援：

- Monospace Font。
- Syntax Highlight。
- Line Number。
- Error Indicator。
- Validation。

建議使用：

```text
JetBrains Mono
```

或：

```text
Roboto Mono
```

---

# 48. Save Feedback

Save 成功後不要在頁面固定顯示：

```text
Saved successfully
```

而使用 Toast。

例如：

```text
Settings saved
```

顯示：

```text
3 ~ 5 seconds
```

後自動消失。

---

# 49. Toast

Desktop：

```text
Bottom Right
```

Mobile：

```text
Bottom Center
```

Toast 類型：

```text
Success
Error
Warning
Info
```

Toast 不應遮住主要控制項。

---

# 50. Dialog

Dialog 用於：

- Delete Confirmation。
- Restart。
- Reset。
- Destructive Operation。

標準 Dialog：

```text
Title

Short Description

Cancel
Confirm
```

---

# 51. Dangerous Action

Dangerous Action 不使用過多警告文字。

例如：

```text
Delete Function?

This action cannot be undone.

Cancel
Delete
```

Delete 使用 Danger Button。

---

# 52. Dropdown Menu

More Menu：

```text
⋮
```

打開後：

```text
Edit
Duplicate
Delete
```

Danger Action 放在最底部，並使用 Danger Text。

---

# 53. Accordion

Accordion Header 必須整行可點擊。

不得只有小箭頭可以點。

結構：

```text
Chevron
Title
Optional summary
```

---

# 54. Empty State

Empty State 應簡短。

例如：

```text
No functions

Create your first function.
```

Action：

```text
Create Function
```

可以使用簡單 SVG Icon。

不使用大型插圖。

---

# 55. Loading

資料載入分為三種：

Page Data：

```text
Skeleton
```

Short Action：

```text
Spinner
```

Long-running Operation：

```text
Progress
```

避免頁面載入時整頁只有大型 Spinner。

---

# 56. Error State

Page-level Error：

```text
Unable to load data.

Retry
```

不要顯示完整 Backend Stack Trace。

詳細錯誤可放：

```text
Expandable Details
```

供技術使用者查看。

---

# 57. Logs

Logs 頁面以文字可讀性優先。

Desktop：

```text
Timestamp
Level
Message
```

例如：

```text
10:24:15 INFO  GPIO 17 set HIGH
10:24:18 WARN  Connection retry
```

Mobile：

可縮減欄位：

```text
10:24 INFO
GPIO 17 set HIGH
```

---

# 58. Log Level

使用：

```text
INFO
WARN
ERROR
DEBUG
```

顏色只是輔助。

文字本身必須存在。

---

# 59. Settings

Settings 使用 Section 分組。

例如：

```text
General

Appearance

Server

GPIO

Advanced
```

不應做成大量獨立 Card。

可以使用：

```text
Section
+
Rows
```

---

# 60. Theme Setting

Theme Options：

```text
System
Light
Dark
```

預設：

```text
System
```

Theme 切換後即時套用。

---

# 61. Responsive Table

Desktop 可使用 Table。

Mobile 不應強制縮小整張 Table。

優先順序：

```text
Hide secondary columns
→ Stack content
→ Horizontal Scroll
```

Horizontal Scroll 是最後選項。

---

# 62. Focus State

Keyboard Focus 必須清楚。

例如：

```text
2px Primary Focus Ring
```

不能完全移除：

```text
outline
```

---

# 63. Hover

Hover 只能是增強效果。

任何功能不能依賴 Hover 才能操作，因為主要裝置是手機。

---

# 64. Motion

動畫時間：

```text
150ms ~ 250ms
```

適合：

- Drawer。
- Dialog。
- Accordion。
- Dropdown。
- Toast。
- Switch。

避免：

- Bounce。
- Parallax。
- 大幅度位移。
- 長動畫。

---

# 65. Reduced Motion

如果系統設定：

```text
prefers-reduced-motion
```

應減少或停用非必要動畫。

---

# 66. Scroll Behavior

主要內容區正常垂直捲動。

Desktop Sidebar 固定。

Drawer 開啟時：

```text
Body Scroll Lock
```

Dialog 開啟時：

```text
Body Scroll Lock
```

---

# 67. Accessibility

至少遵守基本 WCAG AA 原則。

必須包含：

- 合理 Contrast。
- Keyboard Navigation。
- Visible Focus。
- ARIA Label。
- Accessible Form Label。
- Touch Target >= 44px。
- 不只靠顏色傳遞資訊。

---

# 68. SVG

所有 Icon、Logo、簡單圖形：

```text
SVG Preferred
```

避免：

```text
PNG icon
JPEG icon
Raster icon
```

圖片只使用於真正需要照片或複雜圖像的情境。

目前產品 UI 原則上不需要照片。

---

# 69. Design System Compatibility

所有元件設計應盡量接近常見 Design System Pattern。

參考方向：

```text
Material Design
Radix UI
shadcn/ui
Tailwind UI
Ant Design
Fluent UI
```

但不完全模仿其中任何一套。

---

# 70. Shared Component List

設計師至少需建立下列共用 Component：

```text
Button

IconButton

Input

Textarea

Select

Checkbox

Radio

Switch

Card

Badge

Tooltip

Dropdown

Dialog

Drawer

Toast

Accordion

Tabs

Table

Skeleton

Spinner

Progress

Divider
```

---

# 71. Layout Components

另外建立：

```text
AppShell

Sidebar

TopBar

PageHeader

PageContainer

Section

MobileDrawer
```

---

# 72. Status Components

建議建立：

```text
StatusDot

StatusBadge

ConnectionStatus

GPIOState
```

避免每一頁各自設計 Online / Offline 狀態。

---

# 73. Navigation Structure

初版 Navigation：

```text
Home

GPIO

Functions

Logs

Settings
```

建議 Icon：

```text
Home
→ House

GPIO
→ Microchip

Functions
→ Workflow / Braces

Logs
→ ScrollText

Settings
→ Settings
```

---

# 74. Information Density

Mobile：

```text
Medium Density
```

Desktop：

```text
Medium to High Density
```

不要設計成大型 Consumer App。

控制介面應讓使用者：

```text
一個畫面看到更多有效資訊
```

但仍保持足夠 Touch Target。

---

# 75. Desktop Card Density

Desktop Card 不應過高。

例如 GPIO Card 建議：

```text
140px ~ 180px
```

視資訊量調整。

---

# 76. Mobile Density

手機畫面優先採用：

```text
Compact Row
+
List
```

而不是大量：

```text
Large Square Card
```

這是整體設計的重要原則。

---

# 77. Recommended Grid

Desktop：

```text
12-column conceptual grid
```

實際 CSS 不一定需要固定 12 Columns。

常用區域：

```text
2 columns
3 columns
4 columns
```

應使用：

```text
auto-fit
minmax
```

概念進行 Responsive。

---

# 78. Page Header

標準頁面：

```text
Page Title

Optional Description

Optional Primary Action
```

例如：

```text
Functions                       + New Function
Manage reusable GPIO commands.
```

手機可省略 Description。

---

# 79. Description Text

Description 不應超過：

```text
1 ~ 2 lines
```

如果不是必要資訊，直接移除。

---

# 80. Breadcrumb

Breadcrumb 只在多層級頁面使用。

例如：

```text
Functions / Living Room Light
```

手機可以隱藏或簡化。

---

# 81. Naming

UI 用語保持簡短一致。

例如：

```text
New Function
Save
Cancel
Delete
Edit
Duplicate
Retry
Refresh
```

避免：

```text
Click here to add a new function
```

---

# 82. Online / Offline

系統連線狀態應固定有明確入口。

Desktop：

可放 Sidebar 底部。

例如：

```text
● Raspberry Pi
Online
```

Mobile：

可放 Drawer 底部。

---

# 83. Offline Behavior

Offline 時：

不可讓 UI 看起來仍可正常操作 GPIO。

應：

```text
Disable GPIO control

Show Offline State

Keep read-only cached data if available
```

並顯示 Toast / Banner：

```text
Connection lost
```

---

# 84. Banner

Banner 只用於：

- Offline。
- Critical Error。
- Required Action。

不要用於一般 Save Success。

一般成功訊息使用 Toast。

---

# 85. Responsive Design Summary

## Mobile

```text
Top Bar
Navigation Drawer
Single-column primary layout
Compact list-oriented controls
No bottom navigation
```

## Tablet

```text
Top Bar
Navigation Drawer
2-column layouts where appropriate
```

## Desktop

```text
Fixed Sidebar
Top Bar
Multi-column Content
Higher information density
```

---

# 86. Visual Style Summary

整體 Style Keywords：

```text
Clean

Minimal

Technical

Modern

Professional

Compact

Functional
```

---

# 87. Avoid

設計上避免：

```text
Bottom Navigation

Large Hero Banner

Large Illustration

Photo Background

Heavy Gradient

Strong Glassmorphism

Excessive Shadow

Excessive Rounded Corners

Huge Typography

Repeated explanatory text

Too many primary-colored buttons

Mobile App imitation
```

---

# 88. Design Tokens Summary

初步建議：

```text
Sidebar Width
256px

Top Bar Height
60px

Mobile Padding
16px

Desktop Padding
24px ~ 32px

Card Padding
16px

Standard Gap
16px

Section Gap
24px ~ 32px

Touch Target
44px minimum

Icon
20px standard

Radius
8px control
12px card
16px dialog

Animation
150ms ~ 250ms
```

---

# 89. Primary Navigation Summary

```text
Home
GPIO
Functions
Logs
Settings
```

未來增加功能時，應避免讓 Sidebar 無限制增加項目。

超過約 7 個主要功能時，應考慮：

```text
Navigation Group
```

---

# 90. Overall UX Rule

每一個畫面設計時都應先回答三個問題：

```text
使用者現在在哪裡？

這個畫面的主要資訊是什麼？

這個畫面的主要操作是什麼？
```

若一個畫面同時出現多個同等醒目的主要操作，代表資訊階層可能需要重新調整。

---

# 91. 最終設計方向

本專案的核心 UI 架構定義如下。

Mobile：

```text
Top Bar
+
Navigation Drawer
+
Main Content
```

Desktop：

```text
Fixed Sidebar
+
Top Bar
+
Main Content
```

主要視覺：

```text
Neutral Background
+
Simple Surface
+
SVG Icons
+
Minimal Text
+
Compact Controls
```

整體應看起來像：

```text
現代化 Web 管理介面 / Web Dashboard
```

而不是：

```text
手機原生 App
```

也不是：

```text
傳統企業後台系統
```

最終目標是讓 Raspberry Pi GPIO 的日常操作：

```text
快速
清楚
可靠
容易理解
適合手機
同時保有 Desktop 的資訊密度
```