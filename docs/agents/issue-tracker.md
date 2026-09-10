# Issue tracker：Local Markdown

本儲存庫的 issues 與規格以 `.scratch/` 下的 Markdown 檔案管理。

## 檔案慣例

- 每項功能使用一個目錄：`.scratch/<feature-slug>/`
- 規格存放於 `.scratch/<feature-slug>/spec.md`
- 每張實作票各自存放於 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`
- 票號由 `01` 開始遞增，不得合併為單一 tickets 檔案
- Triage 狀態以 issue 檔案開頭附近的 `Status:` 記錄；可用值詳見 `triage-labels.md`
- 討論紀錄附加於檔案底部的 `## Comments`

## 發布與讀取

當 Skill 要求「publish to the issue tracker」時，建立對應的 `.scratch/<feature-slug>/` 及 Markdown 檔案。

當 Skill 要求「fetch the relevant ticket」時，讀取使用者指定的檔案路徑或票號。

## Wayfinding 操作

- Map：`.scratch/<effort>/map.md`
- Child ticket：`.scratch/<effort>/issues/<NN>-<slug>.md`
- `Type:` 可為 `research`、`prototype`、`grilling` 或 `task`
- `Status:` 可為 `claimed` 或 `resolved`
- `Blocked by: NN, NN` 記錄相依票號
- Claim 時先將狀態改為 `claimed`
- Resolve 時加入 `## Answer`、將狀態改為 `resolved`，並更新 map
