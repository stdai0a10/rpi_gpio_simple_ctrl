# Raspberry Pi GPIO Simple Controller

# Color & Theme Specification

版本：Draft v0.1

---

## 1. 文件目的

本文件定義 Raspberry Pi GPIO Simple Controller 的色彩系統，包括：

- Brand / Primary Color
- Neutral Color
- Semantic Color
- Light Theme
- Dark Theme
- Component State Color
- Overlay
- Focus
- Disabled State
- GPIO / System Status Color

本文件會與 UI Style Guide 圖片一起提供給設計師。

### 規格優先順序

若圖片與本文件存在差異：

**以本文件的 Color Token 與色碼為準。**

圖片主要用於：

- 理解整體色調。
- 理解 Light / Dark Mode 的視覺關係。
- 理解 Component 使用色彩的大致方式。

本文件則作為實際設計與實作的色彩基準。

---

# 2. 整體色彩方向

整體採用：

**Neutral + Slightly Cool Tone**

也就是：

- 以中性灰為基礎。
- 色調略偏冷。
- 不呈現明顯藍灰。
- 不使用暖米色、黃灰、棕灰作為主要背景。
- Primary Color 使用 Indigo。
- Semantic Color 使用容易辨識的標準綠／黃／紅／藍。

整體視覺應給人的感覺：

```text
Clean
Neutral
Technical
Calm
Modern
Reliable
```

避免：

```text
Warm Beige
Brown Gray
Highly Saturated Background
Neon
Large Gradient
Pure Black UI
Pure White + Heavy Black Border
```

---

# 3. Primary Color

Primary Color 使用：

**Indigo**

用途：

- Primary Button
- Active Navigation
- Selected State
- Focus
- Link
- Active Switch
- Important interactive emphasis

Primary 不應大量作為背景裝飾。

---

## 3.1 Primary Palette

| Token | Color |
|---|---|
| Primary 50 | `#EEF2FF` |
| Primary 100 | `#E0E7FF` |
| Primary 500 | `#6366F1` |
| Primary 600 | `#4F46E5` |
| Primary 700 | `#4338CA` |

主要基準色：

```text
Primary
#6366F1
```

較強互動狀態：

```text
Primary Strong
#4F46E5
```

---

# 4. Primary 使用規則

一般狀態：

```text
Primary 500
#6366F1
```

Hover：

```text
Primary 600
#4F46E5
```

Pressed / Active：

```text
Primary 700
#4338CA
```

Light Mode 淡色背景：

```text
Primary 50
#EEF2FF
```

例如：

- Active Navigation Background
- Selected Row Background
- Soft Badge

---

# 5. Neutral Palette

Neutral Color 是整套 UI 使用量最大的色彩。

Neutral 不應帶明顯暖色。

---

## 5.1 Neutral Colors

| Token | Color |
|---|---|
| Gray 50 | `#F9FAFB` |
| Gray 100 | `#F3F4F6` |
| Gray 200 | `#E5E7EB` |
| Gray 300 | `#D1D5DB` |
| Gray 400 | `#9CA3AF` |
| Gray 500 | `#6B7280` |
| Gray 600 | `#4B5563` |
| Gray 700 | `#1F2937` |
| Gray 900 | `#111827` |

Neutral Palette 主要負責：

- Background
- Surface
- Text
- Border
- Divider
- Disabled State
- Secondary UI

---

# 6. Semantic Colors

Semantic Color 必須保持固定語意。

| Semantic | Color | 用途 |
|---|---|---|
| Success | `#22C55E` | Online、Success、正常 |
| Warning | `#F59E0B` | Warning、Pending、注意 |
| Danger | `#EF4444` | Error、Delete、Critical |
| Info | `#3B82F6` | Information、Informational State |

---

# 7. Semantic Color 語意

## Success

```text
#22C55E
```

可用於：

- Online
- Successful operation
- GPIO HIGH，若 HIGH 被定義為正常啟用狀態
- Healthy
- Connected

---

## Warning

```text
#F59E0B
```

可用於：

- Warning
- Pending
- Retry
- Degraded
- Temperature approaching warning threshold

---

## Danger

```text
#EF4444
```

可用於：

- Error
- Offline error
- Critical state
- Delete
- Destructive Action

Danger 不應用於一般 Cancel。

---

## Info

```text
#3B82F6
```

可用於：

- Information
- System message
- Neutral progress state
- Informational Badge

---

# 8. Light Theme

Light Mode 應呈現：

```text
Off-white Page
+
White Surface
+
Dark Neutral Text
+
Low Contrast Border
```

不使用整頁純白作為唯一背景。

---

## 8.1 Light Theme Tokens

| Token | Color |
|---|---|
| `background` | `#F7F8FA` |
| `surface` | `#FFFFFF` |
| `surface-raised` | `#FFFFFF` |
| `surface-hover` | `#F1F3F5` |
| `text-primary` | `#111827` |
| `text-secondary` | `#6B7280` |
| `text-muted` | `#9CA3AF` |
| `border` | `#E5E7EB` |
| `divider` | `#E5E7EB` |

---

# 9. Light Mode 視覺階層

Page：

```text
#F7F8FA
```

Card / Input / Sidebar Surface：

```text
#FFFFFF
```

Hover Surface：

```text
#F1F3F5
```

主要文字：

```text
#111827
```

次要文字：

```text
#6B7280
```

Hint / Placeholder：

```text
#9CA3AF
```

一般 Border：

```text
#E5E7EB
```

---

# 10. Dark Theme

Dark Mode 應呈現：

```text
Deep Neutral Background
+
Slightly Brighter Surface
+
Soft Near-white Text
```

不得將：

```text
#000000
```

作為主要 Page Background。

目標不是 OLED Pure Black UI，而是低光環境下仍能清楚辨識資訊階層的 Dashboard。

---

## 10.1 Dark Theme Tokens

| Token | Color |
|---|---|
| `background` | `#0F1115` |
| `surface` | `#171A21` |
| `surface-raised` | `#1E222B` |
| `surface-hover` | `#252A34` |
| `text-primary` | `#F3F4F6` |
| `text-secondary` | `#A1A1AA` |
| `text-muted` | `#71717A` |
| `border` | `#2A2F3A` |
| `divider` | `#252A34` |

---

# 11. Dark Mode 視覺階層

由暗至亮：

```text
Page Background
#0F1115

↓

Surface
#171A21

↓

Raised Surface
#1E222B

↓

Hover
#252A34
```

主要依靠：

**Surface 的明度差**

建立 UI 階層。

不要依靠大量亮 Border。

---

# 12. Light / Dark 對照

| Semantic Token | Light | Dark |
|---|---|---|
| Background | `#F7F8FA` | `#0F1115` |
| Surface | `#FFFFFF` | `#171A21` |
| Raised Surface | `#FFFFFF` | `#1E222B` |
| Surface Hover | `#F1F3F5` | `#252A34` |
| Text Primary | `#111827` | `#F3F4F6` |
| Text Secondary | `#6B7280` | `#A1A1AA` |
| Text Muted | `#9CA3AF` | `#71717A` |
| Border | `#E5E7EB` | `#2A2F3A` |
| Divider | `#E5E7EB` | `#252A34` |

Light / Dark Mode 必須保持相同資訊階層。

Theme 切換不應改變：

- 元件位置。
- Component Priority。
- Semantic Meaning。
- Status Meaning。

---

# 13. Navigation

## Light Mode — Active

Background：

```text
#EEF2FF
```

Icon：

```text
#6366F1
```

Text：

```text
#4F46E5
```

---

## Dark Mode — Active

Active Background 建議：

```text
rgba(99, 102, 241, 0.16)
```

Icon：

```text
#818CF8
```

Text：

```text
#A5B4FC
```

Dark Mode 可以稍微提升 Primary 的亮度，以維持辨識度。

---

# 14. Buttons

## Primary Button

Default：

```text
Background
#6366F1
```

Hover：

```text
#4F46E5
```

Pressed：

```text
#4338CA
```

Text：

```text
#FFFFFF
```

---

## Secondary Button — Light

Background：

```text
#FFFFFF
```

Border：

```text
#E5E7EB
```

Text：

```text
#374151
```

Hover：

```text
#F3F4F6
```

---

## Secondary Button — Dark

Background：

```text
#1E222B
```

Border：

```text
#2A2F3A
```

Text：

```text
#F3F4F6
```

Hover：

```text
#252A34
```

---

# 15. Danger Button

Default：

```text
#EF4444
```

Text：

```text
#FFFFFF
```

Danger Button 只使用於真正具有破壞性的操作：

```text
Delete
Reset
Remove
Stop Critical Service
```

不要使用於：

```text
Cancel
Back
Close
```

---

# 16. Focus

Focus 必須具有明顯可見性。

Focus Ring：

```text
#6366F1
```

建議：

```text
2px solid #6366F1
```

並保留：

```text
2px offset
```

避免 Focus Ring 與 Component 本身融合。

---

# 17. Input

## Light

Background：

```text
#FFFFFF
```

Border：

```text
#D1D5DB
```

Text：

```text
#111827
```

Placeholder：

```text
#9CA3AF
```

Focus Border：

```text
#6366F1
```

---

## Dark

Background：

```text
#171A21
```

Border：

```text
#2A2F3A
```

Text：

```text
#F3F4F6
```

Placeholder：

```text
#71717A
```

Focus Border：

```text
#818CF8
```

---

# 18. Disabled State

Disabled 元件不能只降低透明度到完全看不清楚。

## Light

Background：

```text
#F3F4F6
```

Text：

```text
#9CA3AF
```

Border：

```text
#E5E7EB
```

---

## Dark

Background：

```text
#1E222B
```

Text：

```text
#71717A
```

Border：

```text
#252A34
```

Disabled 元件不可呈現 Hover / Active Feedback。

---

# 19. Switch

Active Track：

```text
#6366F1
```

Inactive Track — Light：

```text
#CBD5E1
```

Inactive Track — Dark：

```text
#4B5563
```

Thumb：

```text
#FFFFFF
```

Loading 時可保留目前狀態，但增加 Spinner / Progress Indicator。

不要因為 API request 尚未成功，就立即把控制結果視為完成。

---

# 20. Status Badge

狀態 Badge 應使用：

```text
Soft Background
+
Strong Semantic Text
+
Optional Icon
```

不要使用整塊高飽和背景。

例如 Success：

Light：

```text
Background
rgba(34, 197, 94, 0.12)

Text / Icon
#16A34A
```

Dark：

```text
Background
rgba(34, 197, 94, 0.16)

Text / Icon
#4ADE80
```

---

# 21. Warning Badge

Light：

```text
Background
rgba(245, 158, 11, 0.12)

Text
#D97706
```

Dark：

```text
Background
rgba(245, 158, 11, 0.16)

Text
#FBBF24
```

---

# 22. Danger Badge

Light：

```text
Background
rgba(239, 68, 68, 0.10)

Text
#DC2626
```

Dark：

```text
Background
rgba(239, 68, 68, 0.16)

Text
#F87171
```

---

# 23. Info Badge

Light：

```text
Background
rgba(59, 130, 246, 0.10)

Text
#2563EB
```

Dark：

```text
Background
rgba(59, 130, 246, 0.16)

Text
#60A5FA
```

---

# 24. GPIO State

GPIO State 必須保持 Theme-independent Semantic Meaning。

例如：

```text
HIGH
→ Success / Green

LOW
→ Neutral

ERROR
→ Danger / Red
```

LOW 不建議使用紅色，因為 LOW 並不代表 Error。

---

## HIGH

Light：

```text
#16A34A
```

Dark：

```text
#4ADE80
```

---

## LOW

Light：

```text
#6B7280
```

Dark：

```text
#A1A1AA
```

---

## ERROR

Light：

```text
#DC2626
```

Dark：

```text
#F87171
```

---

# 25. Online / Offline

Online：

```text
Success
Green
```

Offline：

一般斷線：

```text
Neutral / Muted
```

連線錯誤：

```text
Danger
```

因此：

```text
Offline
```

與：

```text
Connection Error
```

視覺上不一定相同。

---

# 26. Overlay

Modal / Drawer 開啟時使用 Overlay。

Light Theme：

```text
rgba(17, 24, 39, 0.40)
```

Dark Theme：

```text
rgba(0, 0, 0, 0.55)
```

Overlay 不應完全遮黑背景。

仍應能辨識後方 Page Context。

---

# 27. Shadow

Color：

Light：

```text
rgba(17, 24, 39, 0.08)
```

Dark：

```text
rgba(0, 0, 0, 0.28)
```

Shadow 不應成為主要的層級區隔方法。

優先使用：

```text
Surface
Border
Spacing
```

---

# 28. Toast

Toast 不依種類使用整塊高飽和背景。

建議：

```text
Neutral Surface
+
Semantic Icon
+
Text
```

例如 Success：

```text
[Green Check] Settings saved
```

而不是整個 Toast 都使用亮綠色。

---

# 29. Error Messages

Form Error：

Light：

```text
#DC2626
```

Dark：

```text
#F87171
```

錯誤 Input 可加入：

```text
Danger Border
+
Error Text
```

但避免整個 Input 背景變紅。

---

# 30. Warning Messages

Warning 不應與 Error 產生視覺混淆。

使用：

```text
Amber
```

而不是：

```text
Red
```

---

# 31. Chart / Progress

若未來使用 Progress / Chart：

Primary Series：

```text
#6366F1
```

Success：

```text
#22C55E
```

Warning：

```text
#F59E0B
```

Danger：

```text
#EF4444
```

Info：

```text
#3B82F6
```

避免為 Dashboard 額外建立大量互不相關的彩虹色。

---

# 32. Code Editor

JSON Editor 應維持與 Theme 一致。

Light Editor：

```text
Background
#FFFFFF
```

Dark Editor：

```text
Background
#0F1115 或 #171A21
```

Syntax Highlight 可使用額外色彩，但：

- 飽和度不可過高。
- 不影響 JSON 可讀性。
- Light / Dark 必須分別設計。
- 不需要與 UI Semantic Color 完全一致。

---

# 33. Theme Behavior

Theme 選項：

```text
System
Light
Dark
```

System：

跟隨：

```text
prefers-color-scheme
```

Theme 切換時：

不重新載入頁面。

所有 Component 應即時切換。

---

# 34. Theme 不得改變語意

例如：

```text
Success
```

Light 與 Dark 都必須維持 Green 系。

```text
Danger
```

Light 與 Dark 都必須維持 Red 系。

```text
Primary
```

Light 與 Dark 都必須維持 Indigo 系。

Dark Mode 可以提高亮度，但不能改變 Hue Family。

---

# 35. Accessibility

Color Contrast 至少以：

**WCAG AA**

為設計目標。

一般文字：

```text
Contrast Ratio >= 4.5:1
```

大型文字：

```text
Contrast Ratio >= 3:1
```

Interactive Element Boundary / State：

應維持足夠辨識度。

---

# 36. 不只使用顏色表達狀態

錯誤：

```text
●
```

只有紅色 Dot。

正確：

```text
● ERROR
```

或：

```text
[Error Icon] Connection failed
```

同樣適用於：

- HIGH / LOW
- Online / Offline
- Success
- Warning
- Error

---

# 37. Color Usage Ratio

整體畫面應主要由 Neutral 組成。

概念比例：

```text
Neutral
約 80%+

Primary
約 10% 以下

Semantic / Status
少量、按需求使用
```

這不是硬性數值，而是視覺方向。

Primary 不應成為大量 Card Background。

---

# 38. 不使用 Primary 的地方

以下通常保持 Neutral：

- 普通 Card。
- Page Background。
- Sidebar Background。
- Form Background。
- Dialog Background。
- Table Background。
- Logs Background。

Primary 只負責：

```text
Action
Selection
Focus
Emphasis
```

---

# 39. Light Mode Overall Reference

期望：

```text
Cool Off-white Background

White Surface

Dark Neutral Typography

Subtle Gray Border

Indigo Interaction

Small Amount of Semantic Color
```

不是：

```text
Pure White Everywhere
+
Black Border Everywhere
```

---

# 40. Dark Mode Overall Reference

期望：

```text
Deep Charcoal Background

Layered Dark Gray Surfaces

Soft White Typography

Low Contrast Borders

Brighter Indigo Interaction

Controlled Semantic Highlights
```

不是：

```text
Pure Black Background

Neon Icons

High Saturation Everywhere
```

---

# 41. CSS Token Reference

實作時建議不要讓 Component 直接寫 Hex。

例如：

```css
:root {
  --color-primary: #6366F1;
  --color-primary-hover: #4F46E5;
  --color-primary-active: #4338CA;

  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-info: #3B82F6;

  --bg-page: #F7F8FA;
  --bg-surface: #FFFFFF;
  --bg-raised: #FFFFFF;
  --bg-hover: #F1F3F5;

  --text-primary: #111827;
  --text-secondary: #6B7280;
  --text-muted: #9CA3AF;

  --border-default: #E5E7EB;
}
```

Dark：

```css
[data-theme="dark"] {
  --bg-page: #0F1115;
  --bg-surface: #171A21;
  --bg-raised: #1E222B;
  --bg-hover: #252A34;

  --text-primary: #F3F4F6;
  --text-secondary: #A1A1AA;
  --text-muted: #71717A;

  --border-default: #2A2F3A;
}
```

以上 CSS 僅作 Token 關係說明，不限制實際 Frontend 的 Theme 實作方式。

---

# 42. Designer Adjustment Rule

本文件中的色碼為設計基準。

設計師可以因以下原因微調：

- WCAG Contrast。
- OLED / LCD 顯示效果。
- Component State 可辨識性。
- Disabled State 清晰度。
- Dark Mode readability。

但原則上：

**不可任意改變 Hue Family 與整體色溫。**

例如：

可以：

```text
#6366F1
→ #6265EE
```

做非常小幅度調整。

不應：

```text
Indigo
→ Cyan

Neutral Cool Gray
→ Beige

Success Green
→ Blue
```

---

# 43. Source of Truth

最終實作時應建立一套共用 Theme Token。

Component 只能引用：

```text
Semantic Token
```

而不是：

```text
直接 Hex Color
```

例如：

正確：

```text
Button Primary
→ primary
```

錯誤：

```text
Button Primary
→ #6366F1
```

元件應關心：

```text
「這是 Primary」
```

而不是：

```text
「這是紫藍色」
```

---

# 44. Final Color Direction

整體視覺定義為：

```text
Neutral
+
Cool Gray
+
Indigo Primary
+
Controlled Semantic Color
```

Light Mode：

```text
Bright
Clean
Low Contrast Surface
```

Dark Mode：

```text
Deep
Calm
Layered
Low-light Friendly
```

兩者必須看起來是：

**同一套 Design System 的兩個 Theme。**

而不是兩套獨立的 UI。
