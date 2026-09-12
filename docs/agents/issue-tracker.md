# Issue tracker：Local Markdown

本儲存庫的 issues、規格與 Wayfinding artifacts 以 `.scratch/` 下的
Markdown 檔案管理。

## 檔案慣例

- 每項功能使用一個目錄：`.scratch/<feature-slug>/`
- 規格存放於 `.scratch/<feature-slug>/spec.md`
- 實作票存放於 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`
- 討論紀錄附加於檔案底部的 `## Comments`

## Triage 欄位

已進入 triage 的 issue 使用：

- `Category:`：`bug` 或 `enhancement`
- `Status:`：五個 triage 狀態之一；詳見 `triage-labels.md`

## Wayfinding 欄位

Wayfinding map 位於 `.scratch/<effort>/map.md`，child ticket 位於
`.scratch/<effort>/issues/<NN>-<slug>.md`。Wayfinding 另使用：

- `Type:`：`research`、`prototype`、`grilling` 或 `task`
- `Execution Status:`：`claimed` 或 `resolved`
- `Blocked by:`：相依票號，例如 `01, 02`

Wayfinding 必須以 `Execution Status:` 判斷 frontier 與相依是否解除；
不得覆寫 triage 的 `Status:`。
