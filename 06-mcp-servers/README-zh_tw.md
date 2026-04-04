![第 06 章：MCP 伺服器](images/chapter-header.png)

> **如果 Copilot 能夠讀取你的 GitHub issue、查詢資料庫，並從終端機建立 PR，那會如何？**

目前為止，Copilot 只能處理你直接提供的內容：透過 `@` 參照的檔案、對話歷史，以及它本身的訓練資料。但如果它能夠主動查看你的 GitHub 儲存庫、瀏覽專案檔案，或查詢函式庫的最新文件呢？

這正是 MCP（Model Context Protocol）的用途。它能將 Copilot 連接到外部服務，讓它存取即時的真實資料。Copilot 連接的每個服務稱為「MCP 伺服器」。在本章中，你將設定幾個這樣的連線，並了解它們如何讓 Copilot 變得更加實用。

> 💡 **已經熟悉 MCP 了嗎？** [跳至快速開始](#-use-the-built-in-github-mcp)確認是否正常運作，並開始設定伺服器。

## 🎯 學習目標

完成本章後，你將能夠：

- 了解 MCP 是什麼以及為何重要
- 使用 `/mcp` 指令管理 MCP 伺服器
- 為 GitHub、檔案系統和文件設定 MCP 伺服器
- 在書籍應用程式專案中使用 MCP 驅動的工作流程
- 了解何時以及如何建立自訂 MCP 伺服器（選用）

> ⏱️ **預估時間**：約 50 分鐘（閱讀 15 分鐘 + 實作 35 分鐘）

---

## 🧩 實際類比：瀏覽器擴充功能

<img src="images/browser-extensions-analogy.png" alt="MCP 伺服器就像瀏覽器擴充功能" width="800"/>

把 MCP 伺服器想像成瀏覽器擴充功能。瀏覽器本身可以顯示網頁，但擴充功能能將它連接到額外的服務：

| 瀏覽器擴充功能 | 連接的服務 | MCP 對應項目 |
|----------------|-----------|-------------|
| 密碼管理器 | 你的密碼保存庫 | **GitHub MCP** → 你的儲存庫、issue、PR |
| Grammarly | 寫作分析服務 | **Context7 MCP** → 函式庫文件 |
| 檔案管理器 | 雲端儲存 | **Filesystem MCP** → 本地專案檔案 |

沒有擴充功能，你的瀏覽器仍然有用，但有了擴充功能，它就成了強大的工具。MCP 伺服器對 Copilot 的作用也是如此。它們將 Copilot 連接到真實的即時資料來源，讓它能夠讀取你的 GitHub issue、探索你的檔案系統、獲取最新文件等等。

***MCP 伺服器將 Copilot 連接到外部世界：GitHub、儲存庫、文件等***

> 💡 **關鍵洞察**：沒有 MCP，Copilot 只能看到你明確透過 `@` 分享的檔案。有了 MCP，它可以主動探索你的專案、查看你的 GitHub 儲存庫，以及查詢文件，全部自動完成。

---

<img src="images/quick-start-mcp.png" alt="電源線連接產生明亮電火花，周圍漂浮著代表 MCP 伺服器連線的科技圖示" width="800"/>

# 快速開始：30 秒了解 MCP

## 開始使用內建的 GitHub MCP 伺服器
在進行任何設定之前，讓我們先看看 MCP 的實際效果。
GitHub MCP 伺服器預設已包含在內。試試這個：

```bash
copilot
> List the recent commits in this repository
```

如果 Copilot 回傳了真實的提交資料，你已經看到 MCP 的實際運作了。那就是 GitHub MCP 伺服器代表你存取 GitHub 的結果。但 GitHub 只是*其中一個*伺服器。本章將向你展示如何新增更多伺服器（檔案系統存取、最新文件等），讓 Copilot 能做更多事情。

---

## `/mcp show` 指令

使用 `/mcp show` 查看哪些 MCP 伺服器已設定並啟用：

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **只看到 GitHub 伺服器？** 這是正常的！如果你還沒有新增其他 MCP 伺服器，GitHub 是唯一列出的那個。你將在下一節新增更多。

> 📚 **想查看所有 `/mcp` 指令？** 還有其他用於新增、編輯、啟用和刪除伺服器的指令。請參閱本章末尾的[完整指令參考](#-additional-mcp-commands)。

<details>
<summary>🎬 看看實際效果！</summary>

![MCP 狀態示範](images/mcp-status-demo.gif)

*示範輸出結果僅供參考。你的模型、工具和回應可能與此處顯示的有所不同。*

</details>

---

## MCP 帶來什麼改變？

以下是 MCP 在實際使用中的差異：

**沒有 MCP：**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**有了 MCP：**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP 讓 Copilot 了解你的實際開發環境。

> 📚 **官方文件**：[關於 MCP](https://docs.github.com/copilot/concepts/context/mcp)，深入了解 MCP 如何與 GitHub Copilot 協作。

---

# 設定 MCP 伺服器

<img src="images/configuring-mcp-servers.png" alt="雙手調整專業音響混音台上的旋鈕和滑桿，代表 MCP 伺服器設定" width="800"/>

現在你已經看過 MCP 的實際效果，讓我們設定額外的伺服器。本節涵蓋設定檔格式以及如何新增新伺服器。

---

## MCP 設定檔

MCP 伺服器設定在 `~/.copilot/mcp-config.json`（使用者層級，適用於所有專案）或 `.vscode/mcp.json`（專案層級，僅適用於目前工作區）。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*大多數 MCP 伺服器以 npm 套件形式發布，透過 `npx` 指令執行。*

<details>
<summary>💡 <strong>JSON 新手？</strong> 點此了解每個欄位的含義</summary>

| 欄位 | 含義 |
|------|------|
| `"mcpServers"` | 所有 MCP 伺服器設定的容器 |
| `"server-name"` | 你自訂的名稱（例如 "github"、"filesystem"） |
| `"type": "local"` | 伺服器在你的機器上執行 |
| `"command": "npx"` | 要執行的程式（npx 用來執行 npm 套件） |
| `"args": [...]` | 傳遞給指令的參數 |
| `"tools": ["*"]` | 允許此伺服器的所有工具 |

**重要的 JSON 規則：**
- 字串使用雙引號 `"`（不是單引號）
- 最後一個項目後不加逗號
- 檔案必須是有效的 JSON（如不確定，請使用 [JSON 驗證器](https://jsonlint.com/)）

</details>

---

## 新增 MCP 伺服器

GitHub MCP 伺服器為內建，不需要任何設定。以下是你可以新增的其他伺服器。**依照你的興趣選擇，或按順序逐一設定。**

| 我想要… | 跳至 |
|---------|------|
| 讓 Copilot 瀏覽我的專案檔案 | [Filesystem 伺服器](#filesystem-server) |
| 取得最新的函式庫文件 | [Context7 伺服器](#context7-server-documentation) |
| 探索選用的進階功能（自訂伺服器、web_fetch） | [進階功能](#beyond-the-basics) |

<details>
<summary><strong>Filesystem 伺服器</strong> - 讓 Copilot 探索你的專案檔案</summary>
<a id="filesystem-server"></a>

### Filesystem 伺服器

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` 路徑**：`.` 表示「目前目錄」。Copilot 可以存取相對於你啟動它的位置的檔案。在 Codespace 中，這是你的工作區根目錄。如果你偏好，也可以使用絕對路徑，例如 `/workspaces/copilot-cli-for-beginners`。

將此設定加入 `~/.copilot/mcp-config.json` 並重新啟動 Copilot。

</details>

<details>
<summary><strong>Context7 伺服器</strong> - 取得最新的函式庫文件</summary>
<a id="context7-server-documentation"></a>

### Context7 伺服器（文件）

Context7 讓 Copilot 能存取熱門框架和函式庫的最新文件。Copilot 不再依賴可能過時的訓練資料，而是抓取真正當前的官方文件。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **不需要 API 金鑰**
- ✅ **不需要帳號**
- ✅ **你的程式碼保留在本地**

將此設定加入 `~/.copilot/mcp-config.json` 並重新啟動 Copilot。

</details>

<details>
<summary><strong>進階功能</strong> - 自訂伺服器和網路存取（選用）</summary>
<a id="beyond-the-basics"></a>

這些是選用的進階功能，適合在你熟悉上述核心伺服器之後使用。

### Microsoft Learn MCP 伺服器

到目前為止你看到的每個 MCP 伺服器（filesystem、Context7）都在你的機器上本地執行。但 MCP 伺服器也可以遠端執行，也就是說你只需讓 Copilot CLI 指向一個 URL，它就會處理其餘的事情。不需要 `npx` 或 `python`，沒有本地進程，也沒有需要安裝的相依套件。

[Microsoft Learn MCP 伺服器](https://github.com/microsoftdocs/mcp)就是一個好例子。它讓 Copilot CLI 直接存取官方 Microsoft 文件（Azure、Microsoft Foundry 和其他 AI 主題、.NET、Microsoft 365 等），讓它可以搜尋文件、抓取完整頁面，並找到官方程式碼範例，而不是依賴模型的訓練資料。

- ✅ **不需要 API 金鑰**
- ✅ **不需要帳號**
- ✅ **不需要本地安裝**

**使用 `/plugin install` 快速安裝：**

你可以用一個指令安裝，而不必手動編輯 JSON 設定檔：

```bash
copilot

> /plugin install microsoftdocs/mcp
```

這會自動新增伺服器及其相關的 agent skill。安裝的 skill 包括：

- **microsoft-docs**：概念、教學和事實查詢
- **microsoft-code-reference**：API 查詢、程式碼範例和疑難排解
- **microsoft-skill-creator**：用於產生 Microsoft 技術相關自訂 skill 的 meta-skill

**使用方式：**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 了解更多：[Microsoft Learn MCP 伺服器概觀](https://learn.microsoft.com/training/support/mcp-get-started)

### 使用 `web_fetch` 存取網路

Copilot CLI 內建 `web_fetch` 工具，可以從任何 URL 抓取內容。這對於在不離開終端機的情況下引入 README、API 文件或更新說明非常有用。不需要 MCP 伺服器。

你可以透過 `~/.copilot/config.json`（一般 Copilot 設定）控制哪些 URL 可以存取，這與 `~/.copilot/mcp-config.json`（MCP 伺服器定義）是分開的。

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**使用方式：**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### 建立自訂 MCP 伺服器

想要將 Copilot 連接到你自己的 API、資料庫或內部工具嗎？你可以用 Python 建立自訂 MCP 伺服器。這完全是選用的，因為預建的伺服器（GitHub、filesystem、Context7）已涵蓋大多數使用案例。

📖 請參閱[自訂 MCP 伺服器指南](mcp-custom-server-zh_tw.md)，以書籍應用程式為例的完整操作說明。

📚 更多背景資訊，請參閱 [MCP for Beginners 課程](https://github.com/microsoft/mcp-for-beginners)。

</details>

<a id="complete-configuration-file"></a>

### 完整設定檔

以下是包含 filesystem 和 Context7 伺服器的完整 `mcp-config.json`：

> 💡 **注意：** GitHub MCP 為內建功能，不需要加入設定檔。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

將此儲存為 `~/.copilot/mcp-config.json` 以全域存取，或儲存為 `.vscode/mcp.json` 以進行專案特定設定。

---

# 使用 MCP 伺服器

現在你已設定好 MCP 伺服器，讓我們看看它們能做什麼。

<img src="images/using-mcp-servers.png" alt="使用 MCP 伺服器 - 輻射狀圖示，顯示 Developer CLI 連接到 GitHub、Filesystem、Context7 和 Custom/Web Fetch 伺服器" width="800" />

---

## 伺服器使用範例

**選擇一個你感興趣的伺服器來探索，或按順序逐一操作。**

| 我想嘗試… | 跳至 |
|----------|------|
| GitHub 儲存庫、issue 和 PR | [GitHub 伺服器](#github-server-built-in) |
| 瀏覽專案檔案 | [Filesystem 伺服器使用方式](#filesystem-server-usage) |
| 查詢函式庫文件 | [Context7 伺服器使用方式](#context7-server-usage) |
| 自訂伺服器、Microsoft Learn MCP 和 web_fetch 使用方式 | [進階功能使用方式](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub 伺服器（內建）</strong> - 存取儲存庫、issue、PR 等</summary>
<a id="github-server-built-in"></a>

### GitHub 伺服器（內建）

GitHub MCP 伺服器為**內建功能**。如果你已登入 Copilot（這是初始設定時完成的），它已經可以正常運作了。不需要任何設定！

> 💡 **無法運作？** 執行 `/login` 重新向 GitHub 驗證身份。

<details>
<summary><strong>在 Dev Container 中的驗證</strong></summary>

- **GitHub Codespaces**（推薦）：驗證是自動的。`gh` CLI 會繼承你的 Codespace token。不需要任何操作。
- **本地 dev container（Docker）**：在容器啟動後執行 `gh auth login`，然後重新啟動 Copilot。

**驗證疑難排解：**
```bash
# 確認你已通過驗證
gh auth status

# 如果沒有，請登入
gh auth login

# 確認 GitHub MCP 已連線
copilot
> /mcp show
```

</details>

| 功能 | 範例 |
|------|------|
| **儲存庫資訊** | 查看提交、分支、貢獻者 |
| **Issues** | 列出、建立、搜尋 issue 和留言 |
| **Pull requests** | 查看 PR、diff、建立 PR、確認狀態 |
| **程式碼搜尋** | 跨儲存庫搜尋程式碼 |
| **Actions** | 查詢工作流程執行狀態 |

```bash
copilot

# 查看此儲存庫的最近活動
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# 探索儲存庫結構
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# 跨儲存庫搜尋程式碼模式
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **在你自己的 fork 上工作？** 如果你 fork 了這個課程儲存庫，你也可以嘗試建立 issue 和 pull request 等寫入操作。我們將在下方的練習中實作這些操作。

> ⚠️ **看不到結果？** GitHub MCP 對儲存庫的遠端（在 github.com 上）進行操作，而不僅僅是本地檔案。請確保你的儲存庫有遠端：執行 `git remote -v` 確認。

</details>

<details>
<summary><strong>Filesystem 伺服器</strong> - 瀏覽和分析專案檔案</summary>
<a id="filesystem-server-usage"></a>

### Filesystem 伺服器

設定完成後，filesystem MCP 提供 Copilot 可以自動使用的工具：

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7 伺服器</strong> - 查詢函式庫文件</summary>
<a id="context7-server-usage"></a>

### Context7 伺服器

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot now knows the official pytest patterns
# and can apply them to samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>進階功能</strong> - 自訂伺服器和 web_fetch 使用方式</summary>
<a id="beyond-the-basics-usage"></a>

### 進階功能

**自訂 MCP 伺服器**：如果你已依照[自訂 MCP 伺服器指南](mcp-custom-server-zh_tw.md)建立了書籍查詢伺服器，你可以直接查詢你的書籍集合：

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**：如果你安裝了 [Microsoft Learn MCP 伺服器](#microsoft-learn-mcp-server)，你可以直接查詢官方 Microsoft 文件：

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**：使用內建的 `web_fetch` 工具從任何 URL 抓取內容：

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## 多伺服器工作流程

這些工作流程展示了為什麼開發者說「我再也不想在沒有它的情況下工作了。」每個範例都在單一 session 中結合多個 MCP 伺服器。

<img src="images/issue-to-pr-workflow.png" alt="使用 MCP 的 Issue 轉 PR 工作流程 - 顯示從取得 GitHub issue 到建立 pull request 的完整流程" width="800"/>

*完整的 MCP 工作流程：GitHub MCP 擷取儲存庫資料、Filesystem MCP 尋找程式碼、Context7 MCP 提供最佳實踐，Copilot 負責分析*

以下每個範例都是獨立的。**選擇一個你感興趣的，或全部閱讀。**

| 我想看… | 跳至 |
|---------|------|
| 多個伺服器協同工作 | [多伺服器探索](#multi-server-exploration) |
| 在單一 session 中從 issue 到 PR | [Issue-to-PR 工作流程](#issue-to-pr-workflow) |
| 快速專案健康檢查 | [健康儀表板](#health-dashboard) |

<details>
<summary><strong>多伺服器探索</strong> - 在單一 session 中結合 filesystem、GitHub 和 Context7</summary>
<a id="multi-server-exploration"></a>

#### 使用多個 MCP 伺服器探索書籍應用程式

```bash
copilot

# 步驟 1：使用 filesystem MCP 探索書籍應用程式
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# 步驟 2：使用 GitHub MCP 查看最近的變更
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# 步驟 3：使用 Context7 MCP 取得最佳實踐
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# 步驟 4：綜合出建議
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 看看 MCP 工作流程的實際效果！</summary>

![MCP 工作流程示範](images/mcp-workflow-demo.gif)

*示範輸出結果僅供參考。你的模型、工具和回應可能與此處顯示的有所不同。*

</details>

**結果**：程式碼探索 → 歷史記錄審查 → 最佳實踐查詢 → 改進計畫。**全部在單一終端機 session 中，同時使用三個 MCP 伺服器完成。**

</details>

<details>
<summary><strong>Issue-to-PR 工作流程</strong> - 不離開終端機，從 GitHub issue 到 pull request</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue-to-PR 工作流程（在你自己的儲存庫上）

這個工作流程在你擁有寫入權限的自己的 fork 或儲存庫上效果最佳：

> 💡 **現在無法嘗試也沒關係。** 如果你在唯讀的 clone 上，你將在作業中練習這個流程。現在只需閱讀以了解整個流程即可。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**零複製貼上。零情境切換。單一終端機 session。**

</details>

<details>
<summary><strong>健康儀表板</strong> - 使用多個伺服器快速進行專案健康檢查</summary>
<a id="health-dashboard"></a>

#### 書籍應用程式健康儀表板

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**結果**：在幾秒內彙整多個資料來源。手動處理的話，需要執行 grep、計算行數、查看 git log 和瀏覽測試檔案，輕鬆要花 15 分鐘以上。

</details>

---

# 練習

<img src="../images/practice.png" alt="溫馨的辦公桌設定，顯示程式碼的螢幕、檯燈、咖啡杯和耳機，為實作練習做好準備" width="800"/>

**🎉 你現在掌握了基本知識！** 你了解了 MCP，看過如何設定伺服器，並看過實際工作流程。現在是你自己嘗試的時候了。

---

## ▶️ 自行嘗試

現在換你了！完成這些練習，使用書籍應用程式專案練習 MCP 伺服器。

### 練習 1：確認你的 MCP 狀態

先查看哪些 MCP 伺服器可用：

```bash
copilot

> /mcp show
```

你應該看到 GitHub 伺服器列為已啟用。如果沒有，執行 `/login` 進行驗證。

---

### 練習 2：使用 Filesystem MCP 探索書籍應用程式

如果你已設定 filesystem 伺服器，用它來探索書籍應用程式：

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**預期結果**：Copilot 列出 `book_app.py`、`books.py` 和 `utils.py` 及其函式。

> 💡 **尚未設定 filesystem MCP？** 從上方的[完整設定](#complete-configuration-file)章節建立設定檔，然後重新啟動 Copilot。

---

### 練習 3：使用 GitHub MCP 查詢儲存庫歷史記錄

使用內建的 GitHub MCP 探索這個課程儲存庫：

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**預期結果**：Copilot 顯示來自 GitHub 遠端的最近提交訊息和分支名稱。

> ⚠️ **在 Codespace 中？** 這會自動運作，驗證已被繼承。如果你在本地 clone 上，請確認 `gh auth status` 顯示你已登入。

---

### 練習 4：結合多個 MCP 伺服器

現在在單一 session 中結合 filesystem 和 GitHub MCP：

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**預期結果**：Copilot 讀取 JSON 檔案（filesystem MCP），列出 5 本書，包括「The Hobbit」、「1984」、「Dune」、「To Kill a Mockingbird」和「Mysterious Book」，然後查詢 GitHub 的提交歷史記錄。

**自我檢測**：當你能夠解釋為什麼「查看我的儲存庫提交歷史記錄」比手動執行 `git log` 並將輸出貼到提示中更好時，你就掌握了 MCP。

---

## 📝 作業

### 主要挑戰：書籍應用程式 MCP 探索

在書籍應用程式專案上練習結合使用 MCP 伺服器。在單一 Copilot session 中完成以下步驟：

1. **確認 MCP 正常運作**：執行 `/mcp show` 並確認至少 GitHub 伺服器已啟用
2. **設定 filesystem MCP**（如果尚未完成）：使用 filesystem 伺服器設定建立 `~/.copilot/mcp-config.json`
3. **探索程式碼**：請 Copilot 使用 filesystem 伺服器：
   - 列出 `samples/book-app-project/books.py` 中的所有函式
   - 確認 `samples/book-app-project/utils.py` 中哪些函式缺少型別提示
   - 讀取 `samples/book-app-project/data.json` 並找出任何資料品質問題（提示：看最後一個條目）
4. **查看儲存庫活動**：請 Copilot 使用 GitHub MCP：
   - 列出觸及 `samples/book-app-project/` 中檔案的最近提交
   - 確認是否有任何未解決的 issue 或 pull request
5. **結合伺服器**：在單一提示中，請 Copilot：
   - 讀取 `samples/book-app-project/tests/test_books.py` 的測試檔案
   - 將已測試的函式與 `books.py` 中的所有函式進行比較
   - 摘要缺少的測試覆蓋率

**成功標準**：你能夠在單一 Copilot session 中無縫結合 filesystem 和 GitHub MCP 資料，並能解釋每個 MCP 伺服器對回應的貢獻。

<details>
<summary>💡 提示（點擊展開）</summary>

**步驟 1：確認 MCP**
```bash
copilot
> /mcp show
# 應顯示 "github" 為已啟用
# 如果沒有，執行：/login
```

**步驟 2：建立設定檔**

使用上方[完整設定](#complete-configuration-file)章節中的 JSON，儲存為 `~/.copilot/mcp-config.json`。

**步驟 3：需要查找的資料品質問題**

`data.json` 中的最後一本書是：
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
空的作者和年份為 0。這就是資料品質問題！

**步驟 5：測試覆蓋率比較**

`test_books.py` 中的測試涵蓋：`add_book`、`mark_as_read`、`remove_book`、`get_unread_books` 和 `find_book_by_title`。像 `load_books`、`save_books` 和 `list_books` 這樣的函式沒有直接測試。`book_app.py` 中的 CLI 函式和 `utils.py` 中的輔助函式根本沒有測試。

**如果 MCP 無法運作：** 編輯設定檔後重新啟動 Copilot。

</details>

### 進階挑戰：建立自訂 MCP 伺服器

準備好深入探索了嗎？按照[自訂 MCP 伺服器指南](mcp-custom-server-zh_tw.md)在 Python 中建立你自己的 MCP 伺服器，連接到任何 API。

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 發生情況 | 解決方法 |
|------|---------|---------|
| 不知道 GitHub MCP 是內建的 | 嘗試手動安裝/設定它 | GitHub MCP 預設已包含。直接嘗試：「List the recent commits in this repo」 |
| 在錯誤的位置尋找設定 | 找不到或無法編輯 MCP 設定 | 使用者層級設定在 `~/.copilot/mcp-config.json`，專案層級在 `.vscode/mcp.json` |
| 設定檔中的 JSON 無效 | MCP 伺服器無法載入 | 使用 `/mcp show` 確認設定；驗證 JSON 語法 |
| 忘記對 MCP 伺服器進行驗證 | 「驗證失敗」錯誤 | 部分 MCP 需要單獨驗證。確認每個伺服器的要求 |

### 疑難排解

**「找不到 MCP 伺服器」** - 確認：
1. npm 套件存在：`npm view @modelcontextprotocol/server-github`
2. 你的設定是有效的 JSON
3. 伺服器名稱與你的設定相符

使用 `/mcp show` 查看目前設定。

**「GitHub 驗證失敗」** - 內建的 GitHub MCP 使用你的 `/login` 憑證。請嘗試：

```bash
copilot
> /login
```

這將重新向 GitHub 驗證你的身份。如果問題持續，請確認你的 GitHub 帳戶對你正在存取的儲存庫有必要的權限。

**「MCP 伺服器啟動失敗」** - 確認伺服器日誌：
```bash
# 手動執行伺服器指令查看錯誤
npx -y @modelcontextprotocol/server-github
```

**MCP 工具不可用** - 確認伺服器已啟用：
```bash
copilot

> /mcp show
# 確認伺服器是否已列出並啟用
```

如果伺服器被停用，請參閱下方的[其他 `/mcp` 指令](#-additional-mcp-commands)了解如何重新啟用它。

</details>

---

<details>
<summary>📚 <strong>其他 <code>/mcp</code> 指令</strong>（點擊展開）</summary>
<a id="-additional-mcp-commands"></a>

除了 `/mcp show` 之外，還有幾個其他指令用於管理你的 MCP 伺服器：

| 指令 | 功能 |
|------|------|
| `/mcp show` | 顯示所有已設定的 MCP 伺服器及其狀態 |
| `/mcp add` | 互動式新增新伺服器的設定 |
| `/mcp edit <server-name>` | 編輯現有的伺服器設定 |
| `/mcp enable <server-name>` | 啟用已停用的伺服器 |
| `/mcp disable <server-name>` | 暫時停用伺服器 |
| `/mcp delete <server-name>` | 永久移除伺服器 |
| `/mcp auth <server-name>` | 重新向使用 OAuth 的 MCP 伺服器驗證（例如，切換帳戶後） |

在這個課程的大多數情況下，`/mcp show` 就是你所需要的。其他指令在你管理更多伺服器時會變得有用。

</details>

---

# 總結

## 🔑 關鍵要點

1. **MCP** 將 Copilot 連接到外部服務（GitHub、檔案系統、文件）
2. **GitHub MCP 為內建功能** - 不需要設定，只需 `/login`
3. **Filesystem 和 Context7** 透過 `~/.copilot/mcp-config.json` 設定
4. **多伺服器工作流程** 在單一 session 中結合來自多個來源的資料
5. **使用 `/mcp show` 確認伺服器狀態**（管理伺服器的其他指令也可使用）
6. **自訂伺服器** 讓你連接任何 API（選用，在附錄指南中涵蓋）

> 📋 **快速參考**：請參閱 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference)，取得完整的指令和快捷鍵清單。

---

## ➡️ 下一步

你現在擁有了所有建構模組：模式、情境、工作流程、agent、skill 和 MCP。是時候把它們全部整合在一起了。

在**[第 07 章：整合所有技能](../07-putting-it-together/README-zh_tw.md)**中，你將學習：

- 在統一的工作流程中結合 agent、skill 和 MCP
- 從想法到合併 PR 的完整功能開發
- 使用 hook 進行自動化
- 團隊環境的最佳實踐

---

**[← 返回第 05 章](../05-skills/README-zh_tw.md)** | **[繼續第 07 章 →](../07-putting-it-together/README-zh_tw.md)**
