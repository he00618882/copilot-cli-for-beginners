![第 07 章：整合所有技能](images/chapter-header.png)

> **你學到的所有內容在這裡匯聚。在單一 session 中從想法到合併 PR。**

在本章中，你將把所學的一切整合成完整的工作流程。你將使用多 agent 協作建立功能、設定在提交前捕捉安全問題的 pre-commit hook、將 Copilot 整合到 CI/CD pipeline，並在單一終端機 session 中從功能想法到合併 PR。這就是 GitHub Copilot CLI 成為真正力量倍增器的地方。

> 💡 **注意**：本章展示如何結合你所學的一切。**你不需要 agent、skill 或 MCP 才能提高生產力（雖然它們非常有幫助）。** 核心工作流程 — 描述、計畫、實作、測試、審查、發布 — 只需要第 00-03 章的內建功能即可運作。

## 🎯 學習目標

完成本章後，你將能夠：

- 在統一的工作流程中結合 agent、skill 和 MCP（Model Context Protocol）
- 使用多工具方法建立完整的功能
- 設定基本的 hook 自動化
- 應用專業開發的最佳實踐

> ⏱️ **預估時間**：約 75 分鐘（閱讀 15 分鐘 + 實作 60 分鐘）

---

## 🧩 實際類比：管弦樂團

<img src="images/orchestra-analogy.png" alt="管弦樂團類比 - 統一工作流程" width="800"/>

交響樂團有許多部分：
- **弦樂**提供基礎（就像你的核心工作流程）
- **銅管**增添力量（就像具有專業知識的 agent）
- **木管**增添色彩（就像擴展能力的 skill）
- **打擊樂**保持節奏（就像連接外部系統的 MCP）

單獨來看，每個部分聽起來都有所侷限。合在一起，指揮得當，它們創造出壯麗的作品。

**這就是本章所教授的！**<br>
*就像指揮管弦樂團一樣，你統籌 agent、skill 和 MCP 形成統一的工作流程*

讓我們從一個修改程式碼、產生測試、審查，並建立 PR 的場景開始，全部在單一 session 中完成。

---

## 在單一 Session 中從想法到合併 PR

與其在編輯器、終端機、測試執行器和 GitHub UI 之間切換而每次都失去情境，你可以在單一終端機 session 中結合所有工具。我們將在下方的[整合模式](#the-integration-pattern-for-power-users)章節中分解這個模式。

```bash
# 以互動模式啟動 Copilot
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?
# 中文 Prompt：我需要在 book app 新增一個「list unread」指令，只顯示 read 為 False 的書籍。哪些檔案需要變更？

# Copilot creates high-level plan...

# 切換到 PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?
# 中文 Prompt：為 @samples/book-app-project/books.py 設計一個 get_unread_books 方法，最佳做法是什麼？

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# 切換到 PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.
# 中文 Prompt：為 @samples/book-app-project/tests/test_books.py 設計篩選未讀書籍的 test cases

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# 實作
> Add a get_unread_books method to BookCollection in books.py
# 中文 Prompt：在 books.py 的 BookCollection 中新增 get_unread_books 方法
> Add a "list unread" command option in book_app.py
# 中文 Prompt：在 book_app.py 中新增「list unread」指令選項
> Update the help text in the show_help function
# 中文 Prompt：更新 show_help 函式中的說明文字

# 測試
> Generate comprehensive tests for the new feature
# 中文 Prompt：為新功能產生完整的測試

# Multiple tests are generated similar to the following:
# - Happy path (3 tests) — filters correctly, excludes read, includes unread
# - Edge cases (4 tests) — empty collection, all read, none read, single book
# - Parametrized (5 cases) — varying read/unread ratios via @pytest.mark.parametrize
# - Integration (4 tests) — interplay with mark_as_read, remove_book, add_book, and data integrity

# 審查變更
> /review

# 如果審查通過，使用 /pr 對目前分支的 pull request 進行操作
> /pr [view|create|fix|auto]

# 或者，如果你想讓 Copilot 從終端機起草 PR，可以自然地詢問
> Create a pull request titled "Feature: Add list unread books command"
# 中文 Prompt：建立一個標題為「Feature: Add list unread books command」的 pull request
```

**傳統方式**：在編輯器、終端機、測試執行器、文件和 GitHub UI 之間切換。每次切換都造成情境喪失和摩擦。

**關鍵洞察**：你像建築師一樣指導專家。他們處理細節，你掌握整體視野。

> 💡 **進一步提升**：對於像這樣的大型多步驟計畫，嘗試 `/fleet` 讓 Copilot 並行執行獨立的子任務。詳情請參閱[官方文件](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)。

---

# 額外工作流程

<img src="images/combined-workflows.png" alt="人們組裝帶有齒輪的彩色大型拼圖，代表 agent、skill 和 MCP 如何結合成統一的工作流程" width="800"/>

對於完成了第 04-06 章的進階使用者，這些工作流程展示了 agent、skill 和 MCP 如何倍增你的效率。

## 整合模式

以下是結合所有工具的思維模型：

<img src="images/integration-pattern.png" alt="整合模式 - 4 個階段的工作流程：蒐集情境（MCP）、分析和計畫（Agents）、執行（Skills + 手動）、完成（MCP）" width="800"/>

---

## 工作流程 1：Bug 調查和修復

使用完整工具整合的真實世界 bug 修復：

```bash
copilot

# 階段 1：從 GitHub 了解 bug（MCP 提供此功能）
> Get the details of issue #1
# 中文 Prompt：取得 issue #1 的詳情

# 了解："find_by_author doesn't work with partial names"

# 階段 2：研究最佳實踐（使用網路和 GitHub 來源進行深度研究）
> /research Best practices for Python case-insensitive string matching

# 階段 3：找到相關程式碼
> @samples/book-app-project/books.py Show me the find_by_author method
# 中文 Prompt：顯示 @samples/book-app-project/books.py 中的 find_by_author 方法

# 階段 4：取得專家分析
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching
# 中文 Prompt：分析這個方法在部分名稱匹配方面的問題

# Agent identifies: Method uses exact equality instead of substring matching

# 階段 5：依照 agent 的指導修復
> Implement the fix using lowercase comparison and 'in' operator
# 中文 Prompt：使用小寫比較和 'in' 運算子實作 fix

# 階段 6：產生測試
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches
# 中文 Prompt：為 find_by_author 的部分匹配功能產生 pytest 測試，包含以下 test cases：部分名稱、大小寫變化、無結果

# 階段 7：提交和 PR
> Generate a commit message for this fix
# 中文 Prompt：為這個 fix 產生 commit message

> Create a pull request linking to issue #1
# 中文 Prompt：建立一個連結到 issue #1 的 pull request
```

---

## 工作流程 2：程式碼審查自動化（選用）

> 💡 **此章節是選用的。** Pre-commit hook 對團隊很有用，但不是提高生產力的必要條件。如果你剛剛開始，可以跳過這部分。
>
> ⚠️ **效能注意事項**：此 hook 對每個暫存的檔案呼叫 `copilot -p`，每個檔案需要幾秒鐘。對於大型提交，考慮只限制到關鍵檔案，或改用 `/review` 手動執行審查。

**git hook** 是 Git 在特定時間點自動執行的腳本，例如，在提交之前。你可以用它來對你的程式碼執行自動化檢查。以下是如何在你的提交上設定自動化 Copilot 審查：

```bash
# 建立 pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    # --allow-all auto-approves file reads/writes so the hook can run unattended.
    # Only use this in automated scripts. In interactive sessions, let Copilot ask for permission.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)
    # 中文 Prompt：快速 security review @$file — 僅回報 critical 問題

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOS 使用者**：`timeout` 指令在 macOS 上不是預設包含的。使用 `brew install coreutils` 安裝，或將 `timeout 60` 替換為不帶超時保護的簡單呼叫。

> 📚 **官方文件**：[使用 hook](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) 和 [Hook 設定參考](https://docs.github.com/copilot/reference/hooks-configuration)，取得完整的 hook API。
>
> 💡 **內建替代方案**：Copilot CLI 也有內建的 hook 系統（`copilot hooks`），可以在 pre-commit 等事件上自動執行。上方的手動 git hook 讓你有完全的控制，而內建系統更易於設定。請參閱上方的文件決定哪種方式適合你的工作流程。

現在每次提交都會進行快速的安全性審查：

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# 輸出：
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## 工作流程 3：入門新程式碼庫

加入新專案時，結合情境、agent 和 MCP 快速上手：

```bash
# 以互動模式啟動 Copilot
copilot

# 階段 1：使用情境掌握全貌
> @samples/book-app-project/ Explain the high-level architecture of this codebase
# 中文 Prompt：解釋 @samples/book-app-project/ 這個程式碼庫的高層架構

# 階段 2：了解特定流程
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"
# 中文 Prompt：引導我了解 @samples/book-app-project/book_app.py 中當使用者執行「python book_app.py add」時發生了什麼

# 階段 3：使用 agent 取得專家分析
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?
# 中文 Prompt：@samples/book-app-project/books.py 有任何設計問題、缺少 error handling，或你會建議的改進嗎？

# 階段 4：找到可以處理的事項（MCP 提供 GitHub 存取）
> List open issues labeled "good first issue"
# 中文 Prompt：列出標記為「good first issue」的未解決 issue

# 階段 5：開始貢獻
> Pick the simplest open issue and outline a plan to fix it
# 中文 Prompt：選出最簡單的未解決 issue，並擬定 fix 計畫
```

這個工作流程將 `@` 情境、agent 和 MCP 結合到單一的入門 session 中，正是本章前面提到的整合模式。

---

# 最佳實踐與自動化

讓你的工作流程更有效率的模式和習慣。

---

## 最佳實踐

### 1. 分析前先蒐集情境

在請求分析之前，一定要先蒐集情境：

```bash
# 好的做法
> Get the details of issue #42
# 中文 Prompt：取得 issue #42 的詳情
> /agent
# Select python-reviewer
> Analyze this issue
# 中文 Prompt：分析這個 issue

# 效果較差的做法
> /agent
# Select python-reviewer
> Fix login bug
# 中文 Prompt：fix login bug
# Agent 沒有 issue 情境
```

### 2. 了解差異：Agent、Skill 和自訂指令

每個工具都有其最佳使用場景：

```bash
# Agent：你明確啟動的專業角色
> /agent
# Select python-reviewer
> Review this authentication code for security issues
# 中文 Prompt：Review 這段驗證程式碼的 security 問題

# Skill：當你的提示符合 skill 描述時自動啟動的模組化能力
# （你必須先建立它們 — 參見第 05 章）
> Generate comprehensive tests for this code
# 中文 Prompt：為這段程式碼產生完整的測試
# 如果你有已設定的測試 skill，它會自動啟動

# 自訂指令（.github/copilot-instructions.md）：永遠啟用的
# 指導，無需切換或觸發就適用於每個 session
```

> 💡 **關鍵重點**：Agent 和 skill 都可以分析和產生程式碼。真正的差異在於**它們如何啟動** — agent 是明確的（`/agent`），skill 是自動的（提示匹配），自訂指令始終啟用。

### 3. 保持 Session 的專注性

使用 `/rename` 為你的 session 標記（方便在歷史記錄中找到）和 `/exit` 乾淨地結束：

```bash
# 好的做法：每個 session 專注於一個功能
> /rename list-unread-feature
# 處理 list unread
> /exit

copilot
> /rename export-csv-feature
# 處理 CSV 匯出
> /exit

# 效果較差的做法：在一個漫長的 session 中處理所有事情
```

### 4. 使用 Copilot 讓工作流程可重複使用

與其只是在 wiki 中記錄工作流程，不如直接在儲存庫中編碼，讓 Copilot 可以使用它們：

- **自訂指令**（`.github/copilot-instructions.md`）：始終啟用的編碼標準、架構規則和建置/測試/部署步驟指引。每個 session 都會自動遵循它們。
- **提示檔案**（`.github/prompts/`）：你的團隊可以分享的可重複使用參數化提示 — 就像程式碼審查、元件產生或 PR 描述的範本。
- **自訂 agent**（`.github/agents/`）：編碼專業角色（例如，安全性審查員或文件撰寫員），團隊中的任何人都可以使用 `/agent` 啟動。
- **自訂 skill**（`.github/skills/`）：封裝在相關時自動啟動的逐步工作流程指令。

> 💡 **成效**：新團隊成員可以免費獲得你的工作流程 — 它們內建在儲存庫中，而不是鎖在某人的腦海裡。

---

## 進階：生產環境模式

這些模式是選用的，但對專業環境很有價值。

### PR 描述產生器

```bash
# 產生完整的 PR 描述
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
# 中文 Prompt：為以下內容產生 PR 描述：分支：$BRANCH，提交記錄：$COMMITS，包含：摘要、變更內容、測試完成情況、是否需要截圖
```

### CI/CD 整合

對於擁有現有 CI/CD pipeline 的團隊，你可以使用 GitHub Actions 在每個 pull request 上自動化 Copilot 審查。這包括自動發布審查評論和篩選關鍵問題。

> 📖 **深入了解**：請參閱 [CI/CD 整合](../appendices/ci-cd-integration-zh_tw.md)，取得完整的 GitHub Actions 工作流程、設定選項和疑難排解提示。

---

# 練習

<img src="../images/practice.png" alt="溫馨的辦公桌設定，顯示程式碼的螢幕、檯燈、咖啡杯和耳機，為實作練習做好準備" width="800"/>

將完整的工作流程付諸實踐。

---

## ▶️ 自行嘗試

完成示範後，嘗試這些變化：

1. **端對端挑戰**：選擇一個小功能（例如，「列出未讀書籍」或「匯出為 CSV」）。使用完整工作流程：
   - 使用 `/plan` 規劃
   - 使用 agent（python-reviewer、pytest-helper）設計
   - 實作
   - 產生測試
   - 建立 PR

2. **自動化挑戰**：設定程式碼審查自動化工作流程中的 pre-commit hook。進行一個故意包含檔案路徑漏洞的提交。它會被阻擋嗎？

3. **你的生產工作流程**：為你常做的任務設計你自己的工作流程。以清單形式記下來。哪些部分可以用 skill、agent 或 hook 自動化？

**自我檢測**：當你能向同事解釋 agent、skill 和 MCP 如何協作以及何時使用各項時，你就完成了課程。

---

## 📝 作業

### 主要挑戰：端對端功能

實作範例詳細說明了建立「列出未讀書籍」功能的過程。現在在不同的功能上練習完整工作流程：**依年份範圍搜尋書籍**：

1. 啟動 Copilot 並蒐集情境：`@samples/book-app-project/books.py`
2. 使用 `/plan Add a "search by year" command that lets users find books published between two years` 規劃
3. 在 `BookCollection` 中實作 `find_by_year_range(start_year, end_year)` 方法
4. 在 `book_app.py` 中新增 `handle_search_year()` 函式，提示使用者輸入開始和結束年份
5. 產生測試：`@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. 使用 `/review` 審查
7. 更新 README：`@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. 產生提交訊息

進行過程中記錄你的工作流程。

**成功標準**：你已使用 Copilot CLI 完成從想法到提交的功能，包括規劃、實作、測試、文件和審查。

> 💡 **進階挑戰**：如果你已從第 04 章設定了 agent，嘗試建立和使用自訂 agent。例如，用於實作審查的 error-handler agent 和用於 README 更新的 doc-writer agent。

<details>
<summary>💡 提示（點擊展開）</summary>

**依照本章開頭的[「從想法到合併 PR」](#idea-to-merged-pr-in-one-session)範例的模式進行。** 關鍵步驟是：

1. 使用 `@samples/book-app-project/books.py` 蒐集情境
2. 使用 `/plan Add a "search by year" command` 規劃
3. 實作方法和指令處理器
4. 使用邊緣案例產生測試（無效輸入、空結果、反向範圍）
5. 使用 `/review` 審查
6. 使用 `@samples/book-app-project/README.md` 更新 README
7. 使用 `-p` 產生提交訊息

**需要考慮的邊緣案例：**
- 如果使用者輸入「2000」和「1990」（反向範圍）怎麼辦？
- 如果沒有書籍符合範圍怎麼辦？
- 如果使用者輸入非數字輸入怎麼辦？

**關鍵是練習完整工作流程**：想法 → 情境 → 計畫 → 實作 → 測試 → 文件 → 提交。

</details>

---

<details>
<summary>🔧 <strong>常見錯誤</strong>（點擊展開）</summary>

| 錯誤 | 發生情況 | 解決方法 |
|------|---------|---------|
| 直接跳到實作 | 錯過設計問題，後來修復成本很高 | 先使用 `/plan` 思考方法 |
| 在多個工具能幫助時只使用一個 | 結果較慢，較不全面 | 結合：分析用 Agent → 執行用 Skill → 整合用 MCP |
| 提交前不審查 | 安全問題或 bug 漏網 | 始終執行 `/review` 或使用 [pre-commit hook](#workflow-2-code-review-automation-optional) |
| 忘記與團隊分享工作流程 | 每個人都重新發明輪子 | 在共享的 agent、skill 和指令中記錄模式 |

</details>

---

# 總結

## 🔑 關鍵要點

1. **整合 > 孤立**：結合工具以獲得最大影響
2. **情境優先**：在分析之前始終蒐集所需情境
3. **Agent 分析，Skill 執行**：使用正確的工具完成工作
4. **自動化重複工作**：Hook 和腳本倍增你的效率
5. **記錄工作流程**：可共享的模式使整個團隊受益

> 📋 **快速參考**：請參閱 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference)，取得完整的指令和快捷鍵清單。

---

## 🎓 課程完成！

恭喜你！你已學習：

| 章節 | 學到的內容 |
|------|-----------|
| 00 | Copilot CLI 安裝和快速開始 |
| 01 | 三種互動模式 |
| 02 | 使用 @ 語法管理情境 |
| 03 | 開發工作流程 |
| 04 | 專業 agent |
| 05 | 可擴展的 skill |
| 06 | 使用 MCP 進行外部連線 |
| 07 | 統一的生產環境工作流程 |

你現在已具備在開發工作流程中將 GitHub Copilot CLI 作為真正力量倍增器的能力。

## ➡️ 下一步

你的學習不會止步於此：

1. **每天練習**：將 Copilot CLI 用於真實工作
2. **建立自訂工具**：為你的特定需求建立 agent 和 skill
3. **分享知識**：幫助你的團隊採用這些工作流程
4. **保持更新**：關注 GitHub Copilot 的新功能更新

### 參考資源

- [GitHub Copilot CLI 文件](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP 伺服器登錄](https://github.com/modelcontextprotocol/servers)
- [社群 Skill](https://github.com/topics/copilot-skill)

---

**做得好！現在去建立一些了不起的東西吧。**

**[← 返回第 06 章](../06-mcp-servers/README-zh_tw.md)** | **[返回課程首頁 →](../README-zh_tw.md)**
