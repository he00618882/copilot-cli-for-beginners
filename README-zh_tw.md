![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [你將學到什麼](#你將學到什麼) &ensp; ✅ [先備條件](#先備條件) &ensp; 🤖 [Copilot 家族](#認識-github-copilot-家族) &ensp; 📚 [課程結構](#課程結構) &ensp; 📋 [指令參考](#-github-copilot-cli-指令參考)

# GitHub Copilot CLI 新手入門

> **✨ 學習使用 AI 驅動的命令列助手，大幅提升你的開發工作流程。**

GitHub Copilot CLI 將 AI 助手直接帶入你的終端機。不需要切換到瀏覽器或程式碼編輯器，你可以直接在命令列中提問、產生完整功能的應用程式、審查程式碼、產生測試，以及除錯問題。

把它想成一位隨時待命的資深同事，能閱讀你的程式碼、解釋令人困惑的模式，並幫助你更快地完成工作！

> 📘 **偏好網頁瀏覽？** 你可以直接在 GitHub 上跟著這個課程學習，或在 [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) 上以更傳統的瀏覽體驗檢視。

本課程適合：

- **軟體開發者** — 想從命令列使用 AI
- **終端機使用者** — 偏好鍵盤驅動的工作流程，而非 IDE 整合
- **希望標準化的團隊** — 建立 AI 輔助的程式碼審查與開發實踐

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="./images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - Find or host an event" width="100%" />
  </picture>
</a>

## 🎯 你將學到什麼

這是一門實作課程，帶你從零開始熟練使用 GitHub Copilot CLI。你將在所有章節中使用同一個 Python 書籍收藏應用程式，逐步使用 AI 輔助工作流程來改善它。課程結束後，你將能自信地使用 AI 來審查程式碼、產生測試、除錯問題，以及自動化工作流程——全部在終端機中完成。

**不需要 AI 經驗。** 只要你會使用終端機，就能學會。

**適合對象：** 開發者、學生，以及任何有軟體開發經驗的人。

## ✅ 先備條件

開始之前，請確認你具備：

- **GitHub 帳號**：[免費建立一個](https://github.com/signup)<br>
- **GitHub Copilot 存取權限**：[免費方案](https://github.com/features/copilot/plans)、[月費訂閱](https://github.com/features/copilot/plans)，或[學生/教師免費](https://education.github.com/pack)<br>
- **基本終端機操作**：熟悉 `cd`、`ls` 及執行指令的操作

## 🤖 認識 GitHub Copilot 家族

GitHub Copilot 已經發展成一系列 AI 驅動的工具。以下是各產品的運行環境：

| 產品 | 運行環境 | 說明 |
|------|----------|------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（本課程） | 你的終端機 | 終端機原生的 AI 程式設計助手 |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains 等 | Agent 模式、對話、行內建議 |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | 關於你的 repo 的沉浸式對話、建立 agent 等 |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | 將 issue 指派給 agent，取回 PR |

本課程專注於 **GitHub Copilot CLI**，將 AI 助手直接帶入你的終端機。

## 📚 課程結構

![GitHub Copilot CLI Learning Path](images/learning-path.png)

| 章節 | 標題 | 你將建構的內容 |
|:----:|------|---------------|
| 00 | 🚀 [快速開始](./00-quick-start/README-zh_tw.md) | 安裝與驗證 |
| 01 | 👋 [第一步](./01-setup-and-first-steps/README-zh_tw.md) | 即時示範 + 三種互動模式 |
| 02 | 🔍 [上下文與對話](./02-context-conversations/README-zh_tw.md) | 多檔案專案分析 |
| 03 | ⚡ [開發工作流程](./03-development-workflows/README-zh_tw.md) | 程式碼審查、除錯、測試產生 |
| 04 | 🤖 [建立專屬 AI 助手](./04-agents-custom-instructions/README-zh_tw.md) | 為你的工作流程自訂 agent |
| 05 | 🛠️ [自動化重複性任務](./05-skills/README-zh_tw.md) | 自動載入的 skill |
| 06 | 🔌 [連接 GitHub、資料庫與 API](./06-mcp-servers/README-zh_tw.md) | MCP 伺服器整合 |
| 07 | 🎯 [綜合實戰](./07-putting-it-together/README-zh_tw.md) | 完整功能工作流程 |

## 📖 課程進行方式

每個章節都遵循相同的模式：

1. **生活化比喻**：透過熟悉的比較來理解概念
2. **核心概念**：學習必要的知識
3. **實作範例**：執行實際指令並查看結果
4. **練習作業**：實際演練所學內容
5. **下一步**：預覽下一章節

**程式碼範例可直接執行。** 本課程中每個 copilot 文字區塊都可以複製並在你的終端機中執行。

## 📋 GitHub Copilot CLI 指令參考

**[GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference)** 可幫助你查找指令和鍵盤快捷鍵，有效使用 Copilot CLI。

## 🙋 取得協助

- 🐛 **發現 bug？** [提出 Issue](https://github.com/github/copilot-cli-for-beginners/issues)
- 🤝 **想要貢獻？** 歡迎發送 PR！
- 📚 **官方文件：** [GitHub Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## 授權條款

本專案採用 MIT 開源授權條款。完整條款請參閱 [LICENSE](./LICENSE) 檔案。
