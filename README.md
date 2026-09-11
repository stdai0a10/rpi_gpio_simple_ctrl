# RPI_GPIO_SIMPLE_CTRL

簡易的 Raspberry Pi GPIO 控制器。

## 技術框架

- 前端（Frontend）：Vue.js
- 後端（Backend）：Python + FastAPI

## 前端開發

前端需要 Node.js `^22.18.0 || >=24.12.0`，並統一使用 npm：

```shell
cd frontend
npm ci
npm run dev
```

提交前執行完整檢查與 production build：

```shell
npm run check
npm run build
```

## 開發流程

本專案採用 TDD（Test-Driven Development，測試驅動開發）。實作與審查方式請參閱[開發流程需求](docs/development-process.md)。
