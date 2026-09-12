---
title: Raspberry Pi GPIO Simple Controller
---

# Raspberry Pi GPIO Simple Controller

為 Raspberry Pi GPIO 控制服務建立的輕量 Web 應用基礎。專案以 Vue.js
提供瀏覽器端介面，並由 FastAPI 與 Uvicorn 提供後端與已編譯的單頁應用程式。

## 目前狀態

專案目前完成應用程式與前端交付基礎；實際 GPIO 控制功能及對應操作介面仍在後續開發範圍內。
Raspberry Pi 的作業系統映像、Node.js 與硬體相容性也仍須在目標裝置上驗證。

## 已具備的基礎

- FastAPI application 與 Uvicorn 執行流程
- Vue.js 前端的建置與交付流程，由 FastAPI 提供已編譯的 SPA
- `/health` health check，用於確認 ASGI application 可回應請求
- 可信任來源 IP 限制：預設僅允許 IPv4 與 IPv6 loopback，部署時可透過設定調整可信任 CIDR
- Python 與前端的自動化測試、格式與型別檢查流程

## 架構概覽

```text
Browser
  |
  v
Vue.js SPA (compiled bundle)
  |
  v
FastAPI + Uvicorn
  |- trusted source IP middleware
  |- /health
  `- future GPIO functions and API
```

## 技術選擇

- Frontend: Vue.js、Vite、TypeScript、Vitest
- Backend: Python 3.13、FastAPI、Uvicorn、pydantic-settings
- Quality checks: pytest、isort、Black、Prettier、ESLint、TypeScript

## 原始碼與授權

- [查看原始碼](https://github.com/stdai0a10/rpi_gpio_simple_ctrl)
- [MIT License](LICENSE)
