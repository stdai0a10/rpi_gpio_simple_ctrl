# Domain Docs

工程 Skills 在探索程式碼前，依本文件讀取領域文件。

## 探索前讀取

- 根目錄 `CONTEXT.md`
- `docs/adr/` 中與工作範圍相關的 ADR

檔案尚不存在時應直接繼續，不需事先建立或回報缺少；待領域詞彙或架構決策確立後，再由 `domain-modeling` 建立。

## Single-context 配置

```text
/
├── CONTEXT.md
├── docs/
│   └── adr/
├── backend/
└── frontend/
```

## 使用領域詞彙

Issue、重構建議、假設與測試名稱應使用 `CONTEXT.md` 定義的詞彙，避免改用被明確排除的同義詞。

## ADR 衝突

若變更與既有 ADR 衝突，必須明確指出所衝突的 ADR 及重新檢討的原因，不得靜默覆寫。
