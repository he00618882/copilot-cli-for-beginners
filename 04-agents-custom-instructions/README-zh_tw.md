![Chapter 04: Agents and Custom Instructions](images/chapter-header.png)

> **如果你可以同時雇用一位 Python 程式碼審查員、測試專家和安全審查員……全都在同一個工具裡，那會怎樣？**

在第 03 章中，你已掌握了基本工作流程：程式碼審查、重構、除錯、測試生成與 git 整合。這些讓你在使用 GitHub Copilot CLI 時大幅提升效率。現在，讓我們更進一步。

到目前為止，你一直把 Copilot CLI 當作一個通用助手來使用。Agent 讓你能賦予它特定的角色，並內建相應標準，例如一個能強制執行 type hint 和 PEP 8 的程式碼審查員，或是一個撰寫 pytest 案例的測試輔助員。你將會看到，當相同的提示由具有針對性指令的 agent 來處理時，輸出結果會明顯更好。

## 🎯 學習目標

完成本章後，你將能夠：

- 使用內建 agent：Plan（`/plan`）、Code-review（`/review`），並了解自動 agent（Explore、Task）
- 使用 agent 檔案（`.agent.md`）建立專業化 agent
- 將 agent 用於特定領域的任務
- 使用 `/agent` 和 `--agent` 切換 agent
- 為專案特定標準撰寫自訂指令檔案

> ⏱️ **預估時間**：約 55 分鐘（20 分鐘閱讀 + 35 分鐘實作）

---

## 🧩 現實世界比喻：雇用專家

當你的房子需要協助時，你不會打電話給一個「通用幫手」，而是會找專家：

| 問題 | 專家 | 原因 |
|------|------|------|
| 水管漏水 | 水管工 | 了解水管規範，擁有專業工具 |
| 電路重新佈線 | 電工 | 理解安全要求，符合規範 |
| 換屋頂 | 屋頂工 | 了解材料、當地氣候因素 |

Agent 的運作方式相同。與其使用通用 AI，不如使用專注於特定任務並了解正確流程的 agent。設定一次指令，之後每當你需要那個專業時就能重複使用：程式碼審查、測試、安全性、文件撰寫。

<img src="images/hiring-specialists-analogy.png" alt="Hiring Specialists Analogy - Just as you call specialized tradespeople for house repairs, AI agents are specialized for specific tasks like code review, testing, security, and documentation" width="800" />

---

# 使用 Agent

立即開始使用內建與自訂 agent。

---

## *第一次接觸 Agent？* 從這裡開始！
從未使用或建立過 agent？以下是本課程入門所需的全部知識。

1. **立即嘗試一個*內建* agent：**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   這會呼叫 Plan agent，為你建立一個逐步的實作計畫。

2. **查看我們的自訂 agent 範例：** 定義 agent 指令非常簡單，請查看我們提供的 [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) 檔案，了解其模式。

3. **理解核心概念：** Agent 就像諮詢專家而非通才。「frontend agent」會自動專注於無障礙功能和元件模式，你不需要反覆提醒，因為這些已在 agent 的指令中指定。


## 內建 Agent

**你在第 03 章的開發工作流程中已經使用過一些內建 agent 了！**
<br>`/plan` 和 `/review` 其實就是內建 agent。現在你了解了背後的運作原理。以下是完整清單：

| Agent | 呼叫方式 | 功能說明 |
|-------|---------|---------|
| **Plan** | `/plan` 或 `Shift+Tab`（循環切換模式） | 在撰寫程式碼前建立逐步實作計畫 |
| **Code-review** | `/review` | 審查已暫存/未暫存的變更，提供集中且可操作的回饋 |
| **Init** | `/init` | 產生專案設定檔（指令檔、agent 檔） |
| **Explore** | *自動觸發* | 當你要求 Copilot 探索或分析程式碼庫時內部使用 |
| **Task** | *自動觸發* | 執行測試、建置、lint 檢查和安裝相依套件等指令 |

<br>

**內建 agent 實際運作** - 呼叫 Plan、Code-review、Explore 和 Task 的範例

```bash
copilot

# Invoke the Plan agent to create an implementation plan
> /plan Add input validation for book year in the book app
# 中文 Prompt：/plan 為 book app 的書籍年份新增 input validation

# Invoke the Code-review agent on your changes
> /review

# Explore and Task agents are invoked automatically when relevant:
> Run the test suite        # Uses Task agent
# 中文 Prompt：執行測試套件

> Explore how book data is loaded    # Uses Explore agent
# 中文 Prompt：探索書籍資料是如何載入的
```

Task Agent 在幕後運作，負責管理和追蹤進行中的事項，並以清晰整潔的格式回報結果：

| 結果 | 你會看到 |
|------|---------|
| ✅ **成功** | 簡短摘要（例如「所有 247 個測試通過」、「建置成功」） |
| ❌ **失敗** | 完整輸出，包含堆疊追蹤、編譯器錯誤和詳細日誌 |


> 📚 **官方文件**：[GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# 將 Agent 加入 Copilot CLI

你可以輕鬆定義自己的 agent，讓它成為工作流程的一部分！定義一次，隨時使用！

<img src="images/using-agents.png" alt="Four colorful AI robots standing together, each with different tools representing specialized agent capabilities" width="800"/>

## 🗂️ 新增你的 agent

Agent 檔案是副檔名為 `.agent.md` 的 markdown 檔案。它們包含兩個部分：YAML frontmatter（元資料）和 markdown 指令。

> 💡 **不熟悉 YAML frontmatter？** 它是檔案頂部的一小段設定區塊，由 `---` 標記包圍。YAML 就是 `key: value` 的鍵值對。其餘部分則是普通的 markdown。

以下是一個最簡 agent：

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **必填與選填**：`description` 欄位是必填的。其他欄位如 `name`、`tools` 和 `model` 則是選填的。

## Agent 檔案放置位置

| 位置 | 範圍 | 最適用於 |
|------|------|---------|
| `.github/agents/` | 專案特定 | 遵循專案規範的團隊共用 agent |
| `~/.copilot/agents/` | 全域（所有專案） | 你在各處都會用到的個人 agent |

**本專案在 [.github/agents/](../.github/agents/) 資料夾中包含範例 agent 檔案**。你可以自行撰寫，或自訂已提供的那些。

<details>
<summary>📂 查看本課程中的範例 agent</summary>

| 檔案 | 說明 |
|------|------|
| `hello-world.agent.md` | 最簡範例，從這裡開始 |
| `python-reviewer.agent.md` | Python 程式碼品質審查員 |
| `pytest-helper.agent.md` | Pytest 測試專家 |

```bash
# Or copy one to your personal agents folder (available in every project)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

更多社群 agent，請參見 [github/awesome-copilot](https://github.com/github/awesome-copilot)

</details>


## 🚀 兩種使用自訂 agent 的方式

### 互動模式
在互動模式中，使用 `/agent` 列出 agent 並選擇要使用的 agent，
然後繼續你的對話。

```bash
copilot
> /agent
```

若要切換至不同的 agent，或回到預設模式，再次使用 `/agent` 指令即可。

### 程式化模式

直接以指定的 agent 啟動新工作階段。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
# 中文 Prompt：Review @samples/book-app-project/books.py
```

> 💡 **切換 agent**：你可以隨時使用 `/agent` 或 `--agent` 切換至不同的 agent。若要回到標準的 Copilot CLI 體驗，使用 `/agent` 並選擇**無 agent**。

---

# 深入探索 Agent

<img src="images/creating-custom-agents.png" alt="Robot being assembled on a workbench surrounded by components and tools representing custom agent creation" width="800"/>

> 💡 **本節為選讀內容。** 內建 agent（`/plan`、`/review`）已足夠應付大多數工作流程。當你需要在工作中持續套用特定領域的專業知識時，再建立自訂 agent。

以下每個主題都是獨立的。**選擇你感興趣的部分閱讀，不需要一次全部讀完。**

| 我想要... | 跳至 |
|---|---|
| 了解 agent 為何優於通用提示 | [Specialist vs Generic](#specialist-vs-generic-see-the-difference) |
| 在某個功能上結合多個 agent | [Working with Multiple Agents](#working-with-multiple-agents) |
| 組織、命名與分享 agent | [Organizing & Sharing Agents](#organizing--sharing-agents) |
| 設定專案的常駐上下文 | [Configuring Your Project for Copilot](#configuring-your-project-for-copilot) |
| 查閱 YAML 屬性和工具 | [Agent File Reference](#agent-file-reference) |

選擇下方的情境以展開。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>Specialist vs Generic: See the Difference</strong> - 為何 agent 能產出比通用提示更好的結果</summary>

## Specialist vs Generic: See the Difference

這正是 agent 展現價值的地方。看看這個差異：

### 不使用 Agent（通用 Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
# 中文 Prompt：在書籍應用程式中新增一個依年份範圍搜尋書籍的函式
```

**通用輸出**：
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基本可用。但缺少很多東西。

---

### 使用 Python Reviewer Agent

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
# 中文 Prompt：在書籍應用程式中新增一個依年份範圍搜尋書籍的函式
```

**專業輸出**：
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewer agent 自動包含的內容**：
- ✅ 所有參數和回傳值都有 type hint
- ✅ 包含 Args/Returns/Raises 的完整 docstring
- ✅ 具備適當錯誤處理的輸入驗證
- ✅ 使用 list comprehension 提升效能
- ✅ 邊界情況處理（缺失/無效的年份值）
- ✅ 符合 PEP 8 的格式
- ✅ 防禦性程式設計實踐

**差異所在**：相同的提示，輸出結果大幅改善。Agent 帶來了你原本可能忘記要求的專業知識。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>Working with Multiple Agents</strong> - 結合專家、中途切換、agent 作為工具</summary>

## Working with Multiple Agents

真正的強大之處在於多個專家共同協作完成一個功能。

### 範例：建立一個簡單功能

```bash
copilot

> I want to add a "search by year range" feature to the book app
# 中文 Prompt：我想在書籍應用程式中新增「依年份範圍搜尋」功能

# Use python-reviewer for design
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?
# 中文 Prompt：@samples/book-app-project/books.py 設計一個 find_by_year_range 方法，什麼是最佳做法？

# Switch to pytest-helper for test design
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
# 中文 Prompt：@samples/book-app-project/tests/test_books.py 為 find_by_year_range 方法設計 test cases
> What edge cases should we cover?
# 中文 Prompt：我們應該涵蓋哪些 edge cases？

# Synthesize both designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
# 中文 Prompt：建立一個包含方法實作和完整 tests 的實作計畫
```

**核心洞見**：你是指揮專家的架構師。他們處理細節，你掌握大局。

<details>
<summary>🎬 看實際示範！</summary>

![Python Reviewer Demo](images/python-reviewer-demo.gif)

*示範輸出會有所不同——你的模型、工具和回應結果將與此處所示有所差異。*

</details>

### Agent 作為工具

當 agent 設定完成後，Copilot 在處理複雜任務時也可以將它們作為工具來呼叫。如果你要求實作一個全端功能，Copilot 可能會自動將各個部分委派給適當的專業 agent。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>Organizing & Sharing Agents</strong> - 命名、檔案放置、指令檔案與團隊共享</summary>

## Organizing & Sharing Agents

### 為你的 Agent 命名

建立 agent 檔案時，名稱很重要。這是你在 `/agent` 或 `--agent` 之後輸入的內容，也是你的隊友在 agent 清單中看到的名稱。

| ✅ 好的名稱 | ❌ 避免使用 |
|------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名慣例：**
- 使用小寫加連字號：`my-agent-name.agent.md`
- 包含領域名稱：`frontend`、`backend`、`devops`、`security`
- 必要時更具體：`react-typescript` 而非只是 `frontend`

---

### 與團隊共享

將 agent 檔案放置在 `.github/agents/` 中，它們就受到版本控制。推送到你的 repo，每位團隊成員就會自動取得這些 agent。但 agent 只是 Copilot 從你的專案讀取的其中一種檔案類型。Copilot 還支援**指令檔案**，這些檔案會自動套用於每個工作階段，不需要任何人執行 `/agent`。

你可以這樣理解：agent 是你按需呼叫的專家，而指令檔案則是始終生效的團隊規則。

### 檔案放置位置

你已經知道兩個主要位置（見上方的 [Where to put agent files](#where-to-put-agent-files)）。使用此決策樹來選擇：

<img src="images/agent-file-placement-decision-tree.png" alt="Decision tree for where to put agent files: experimenting → current folder, team use → .github/agents/, everywhere → ~/.copilot/agents/" width="800"/>

**從簡單開始：** 在你的專案資料夾中建立一個 `*.agent.md` 檔案。滿意後再移至永久位置。

除了 agent 檔案之外，Copilot 也會自動讀取**專案層級的指令檔案**，不需要 `/agent`。請參閱下方的 [Configuring Your Project for Copilot](#configuring-your-project-for-copilot)，了解 `AGENTS.md`、`.instructions.md` 和 `/init`。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Configuring Your Project for Copilot</strong> - AGENTS.md、指令檔案與 /init 設定</summary>

## Configuring Your Project for Copilot

Agent 是你按需呼叫的專家。**專案設定檔**則不同：Copilot 會在每個工作階段自動讀取它們，以了解你的專案慣例、技術堆疊和規則。不需要任何人執行 `/agent`；所有在 repo 中工作的人都會自動套用這些上下文。

### 使用 /init 快速設定

最快的入門方式是讓 Copilot 為你產生設定檔：

```bash
copilot
> /init
```

Copilot 會掃描你的專案並建立量身訂製的指令檔案。你可以在之後編輯它們。

### 指令檔案格式

| 檔案 | 範圍 | 備註 |
|------|------|------|
| `AGENTS.md` | 專案根目錄或巢狀目錄 | **跨平台標準** - 適用於 Copilot 和其他 AI 助手 |
| `.github/copilot-instructions.md` | 專案 | GitHub Copilot 專用 |
| `.github/instructions/*.instructions.md` | 專案 | 細粒度的主題特定指令 |
| `CLAUDE.md`、`GEMINI.md` | 專案根目錄 | 為相容性而支援 |

> 🎯 **剛開始入門？** 使用 `AGENTS.md` 作為專案指令。你可以之後視需要探索其他格式。

### AGENTS.md

`AGENTS.md` 是推薦的格式。它是一個[開放標準](https://agents.md/)，可在 Copilot 和其他 AI 程式碼工具中使用。將它放在你的 repository 根目錄，Copilot 就會自動讀取。本專案自身的 [AGENTS.md](../AGENTS.md) 就是一個實際運作的範例。

典型的 `AGENTS.md` 描述你的專案上下文、程式碼風格、安全需求和測試標準。使用 `/init` 產生一個，或參考我們範例檔案的模式自行撰寫。

### 自訂指令檔案（.instructions.md）

對於想要更細粒度控制的團隊，可以將指令拆分成主題特定的檔案。每個檔案涵蓋一個關注點並自動套用：

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **注意**：指令檔案適用於任何語言。這個範例使用 Python 是為了配合我們的課程專案，但你可以為 TypeScript、Go、Rust 或團隊使用的任何技術建立類似的檔案。

**尋找社群指令檔案**：瀏覽 [github/awesome-copilot](https://github.com/github/awesome-copilot) 查找涵蓋 .NET、Angular、Azure、Python、Docker 以及更多技術的現成指令檔案。

### 停用自訂指令

如果你需要 Copilot 忽略所有專案特定設定（在除錯或比較行為時很有用）：

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>Agent File Reference</strong> - YAML 屬性、工具別名與完整範例</summary>

## Agent File Reference

### 更完整的範例

你已經看過上方的[最簡 agent 格式](#-add-your-agents)。以下是一個使用 `tools` 屬性的更完整 agent。建立 `~/.copilot/agents/python-reviewer.agent.md`：

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### YAML 屬性

| 屬性 | 必填 | 說明 |
|------|------|------|
| `name` | 否 | 顯示名稱（預設為檔案名稱） |
| `description` | **是** | Agent 的功能說明 - 幫助 Copilot 了解何時建議使用它 |
| `tools` | 否 | 允許的工具清單（省略 = 所有工具可用）。請見下方工具別名。 |
| `target` | 否 | 限制僅用於 `vscode` 或 `github-copilot` |

### 工具別名

在 `tools` 清單中使用這些名稱：
- `read` - 讀取檔案內容
- `edit` - 編輯檔案
- `search` - 搜尋檔案（grep/glob）
- `execute` - 執行 shell 指令（亦可用：`shell`、`Bash`）
- `agent` - 呼叫其他自訂 agent

> 📖 **官方文件**：[Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **僅限 VS Code**：`model` 屬性（用於選擇 AI 模型）在 VS Code 中有效，但在 GitHub Copilot CLI 中不支援。你可以在跨平台 agent 檔案中安全地包含它，GitHub Copilot CLI 會忽略它。

### 更多 Agent 範本

> 💡 **初學者注意**：以下範例是範本。**請將特定技術替換為你的專案所使用的技術。** 重要的是 agent 的*結構*，而非提及的特定技術。

本專案在 [.github/agents/](../.github/agents/) 資料夾中包含實際運作的範例：
- [hello-world.agent.md](../.github/agents/hello-world.agent.md) - 最簡範例，從這裡開始
- [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) - Python 程式碼品質審查員
- [pytest-helper.agent.md](../.github/agents/pytest-helper.agent.md) - Pytest 測試專家

社群 agent 請參見 [github/awesome-copilot](https://github.com/github/awesome-copilot)。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

建立你自己的 agent 並觀察它們實際運作。

---

## ▶️ 自己動手試試看

```bash

# Create the agents directory (if it doesn't exist)
mkdir -p .github/agents

# Create a code reviewer agent
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# Create a documentation agent
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Now use them
copilot --agent reviewer
> Review @samples/book-app-project/books.py
# 中文 Prompt：Review @samples/book-app-project/books.py

# Or switch agents
copilot
> /agent
# Select "documentor"
> Document @samples/book-app-project/books.py
# 中文 Prompt：為 @samples/book-app-project/books.py 撰寫文件
```

---

## 📝 作業

### 主要挑戰：建立一個專業 Agent 團隊

上方的實作範例建立了 `reviewer` 和 `documentor` agent。現在練習為不同任務建立和使用 agent——改善書籍應用程式中的資料驗證：

1. 建立 3 個 agent 檔案（`.agent.md`），每個 agent 一個，針對書籍應用程式量身訂製，放置在 `.github/agents/`
2. 你的 agent：
   - **data-validator**：檢查 `data.json` 中缺失或格式錯誤的資料（空的作者、year=0、缺少欄位）
   - **error-handler**：審查 Python 程式碼中不一致的錯誤處理方式並建議統一的方法
   - **doc-writer**：產生或更新 docstring 和 README 內容
3. 在書籍應用程式上使用每個 agent：
   - `data-validator` → 稽核 `@samples/book-app-project/data.json`
   - `error-handler` → 審查 `@samples/book-app-project/books.py` 和 `@samples/book-app-project/utils.py`
   - `doc-writer` → 為 `@samples/book-app-project/books.py` 新增 docstring
4. 協作：使用 `error-handler` 找出錯誤處理的不足之處，再用 `doc-writer` 記錄改善後的方法

**成功標準**：你有 3 個能產出一致、高品質輸出的正常運作 agent，並且可以用 `/agent` 在它們之間切換。

<details>
<summary>💡 提示（點擊展開）</summary>

**起始範本**：在 `.github/agents/` 中為每個 agent 建立一個檔案：

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**測試你的 agent：**

> 💡 **注意：** 你的本機 repo 副本中應該已有 `samples/book-app-project/data.json`。如果缺失，請從原始 repo 下載：
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Select "data-validator" from the list
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
# 中文 Prompt：@samples/book-app-project/data.json 檢查作者欄位為空或年份無效的書籍
```

**提示：** YAML frontmatter 中的 `description` 欄位是 agent 正常運作的必要條件。

</details>

### 加分挑戰：指令資源庫

你已經建立了按需呼叫的 agent。現在嘗試另一面：**指令檔案**，讓 Copilot 在每個工作階段自動讀取，不需要 `/agent`。

在 `.github/instructions/` 資料夾中建立至少 3 個指令檔案：
- `python-style.instructions.md`：強制執行 PEP 8 和 type hint 慣例
- `test-standards.instructions.md`：強制執行測試檔案中的 pytest 慣例
- `data-quality.instructions.md`：驗證 JSON 資料條目

在書籍應用程式的程式碼上測試每個指令檔案。

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 會發生什麼 | 修正方式 |
|------|----------|---------|
| Agent frontmatter 中缺少 `description` | Agent 無法載入或無法被發現 | 務必在 YAML frontmatter 中包含 `description:` |
| Agent 檔案位置錯誤 | 嘗試使用時找不到 agent | 放置在 `~/.copilot/agents/`（個人）或 `.github/agents/`（專案） |
| 使用 `.md` 而非 `.agent.md` | 檔案可能無法被識別為 agent | 將檔案命名為 `python-reviewer.agent.md` 這樣的格式 |
| Agent 提示過長 | 可能超過 30,000 字元限制 | 保持 agent 定義精簡；使用 skill 來放置詳細指令 |

### 疑難排解

**找不到 agent** - 確認 agent 檔案存在於以下其中一個位置：
- `~/.copilot/agents/`
- `.github/agents/`

列出可用的 agent：

```bash
copilot
> /agent
# Shows all available agents
```

**Agent 未遵循指令** - 在提示中更明確說明，並在 agent 定義中增加更多細節：
- 包含版本號的特定框架/函式庫
- 團隊慣例
- 範例程式碼模式

**自訂指令未載入** - 在你的專案中執行 `/init` 以設定專案特定的指令：

```bash
copilot
> /init
```

或檢查它們是否被停用：
```bash
# Don't use --no-custom-instructions if you want them loaded
copilot  # This loads custom instructions by default
```

</details>

---

# 總結

## 🔑 重點整理

1. **內建 agent**：`/plan` 和 `/review` 直接呼叫；Explore 和 Task 自動運作
2. **自訂 agent** 是在 `.agent.md` 檔案中定義的專家
3. **好的 agent** 有清晰的專業知識、標準和輸出格式
4. **多 agent 協作** 透過結合專業知識解決複雜問題
5. **指令檔案**（`.instructions.md`）將團隊標準編碼以自動套用
6. **一致的輸出** 來自定義明確的 agent 指令

> 📋 **快速參考**：請參閱 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) 取得完整的指令和快捷鍵清單。

---

## ➡️ 接下來

Agent 改變了 *Copilot 如何處理並對你的程式碼採取針對性行動*。接下來，你將學習 **skill**——改變的是它*遵循哪些步驟*。想知道 agent 和 skill 有何不同？第 05 章將正面回答這個問題。

在 **[第 05 章：Skills System](../05-skills/README-zh_tw.md)** 中，你將學到：

- Skill 如何從你的提示自動觸發（不需要 slash 指令）
- 安裝社群 skill
- 使用 SKILL.md 檔案建立自訂 skill
- Agent、skill 和 MCP 的差異
- 何時使用各個工具

---

**[← 返回第 03 章](../03-development-workflows/README-zh_tw.md)** | **[繼續至第 05 章 →](../05-skills/README-zh_tw.md)**
