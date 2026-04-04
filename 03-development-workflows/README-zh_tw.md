![Chapter 03: Development Workflows](images/chapter-header.png)

> **如果 AI 能找到你甚至不知道要問的 bug，會怎麼樣？**

在本章中，GitHub Copilot CLI 成為你的日常主要工具。你將在你每天已經依賴的工作流程中使用它：測試、重構、調試和 Git。

## 🎯 學習目標

完成本章後，你將能夠：

- 使用 Copilot CLI 執行全面的程式碼審查
- 安全地重構舊有程式碼
- 在 AI 協助下調試問題
- 自動生成測試
- 將 Copilot CLI 整合到你的 git 工作流程

> ⏱️ **預估時間**：約 60 分鐘（15 分鐘閱讀 + 45 分鐘實際操作）

---

## 🧩 真實世界類比：木工的工作流程

木匠不只是知道如何使用工具，他們對不同的工作有*工作流程*：

<img src="images/carpenter-workflow-steps.png" alt="Craftsman workshop showing three workflow lanes: Building Furniture (Measure, Cut, Assemble, Finish), Fixing Damage (Assess, Remove, Repair, Match), and Quality Check (Inspect, Test Joints, Check Alignment)" width="800"/>

同樣地，開發者對不同任務有工作流程。GitHub Copilot CLI 增強了這些工作流程中的每一個，讓你在日常程式設計任務中更有效率。

---

# 五種工作流程

<img src="images/five-workflows.png" alt="Five glowing neon icons representing code review, testing, debugging, refactoring, and git integration workflows" width="800"/>

下面的每個工作流程都是獨立的。選擇符合你當前需求的，或全部依序完成。

---

## 選擇你自己的冒險

本章涵蓋開發者通常使用的五種工作流程。**但是，你不需要一次全部閱讀！** 每個工作流程都包含在下面可折疊的段落中是獨立的。選擇符合你需求且最適合你當前專案的工作流程。你隨時可以回來探索其他的。

<img src="images/five-workflows-swimlane.png" alt="Five Development Workflows: Code Review, Refactoring, Debugging, Test Generation, and Git Integration shown as horizontal swimlanes" width="800"/>

| 我想要... | 跳至 |
|---|---|
| 在合併前審查程式碼 | [工作流程 1：程式碼審查](#workflow-1-code-review) |
| 清理凌亂或舊有的程式碼 | [工作流程 2：重構](#workflow-2-refactoring) |
| 追蹤和修復 bug | [工作流程 3：調試](#workflow-3-debugging) |
| 為我的程式碼生成測試 | [工作流程 4：測試生成](#workflow-4-test-generation) |
| 撰寫更好的 commit 和 PR | [工作流程 5：Git 整合](#workflow-5-git-integration) |
| 在編寫程式碼前研究 | [快速提示：在規劃或編寫程式碼前先研究](#quick-tip-research-before-you-plan-or-code) |
| 端到端查看完整的 bug 修復工作流程 | [整合在一起](#putting-it-all-together-bug-fix-workflow) |

**選擇下面的工作流程展開它**，看看 GitHub Copilot CLI 如何在該領域增強你的開發流程。

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>工作流程 1：程式碼審查</strong> - 審查檔案、使用 /review agent、建立嚴重性清單</summary>

<img src="images/code-review-swimlane-single.png" alt="Code review workflow: review, identify issues, prioritize, generate checklist." width="800"/>

### 基本審查

此範例使用 `@` 符號引用檔案，讓 Copilot CLI 直接存取其內容進行審查。

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 看它如何運作！</summary>

![Code Review Demo](images/code-review-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

### 輸入驗證審查

要求 Copilot CLI 將審查重點放在特定問題上（此處為輸入驗證），在提示中列出你關心的類別。

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### 跨檔案專案審查

用 `@` 引用整個目錄，讓 Copilot CLI 一次掃描專案中的每個檔案。

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### 互動式程式碼審查

使用多輪對話深入探討。從廣泛的審查開始，然後在不重新啟動的情況下提問後續問題。

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI 提供詳細審查

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI 顯示空字串、特殊字元等潛在問題

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI 生成按優先順序排列的行動項目
```

### 審查清單範本

要求 Copilot CLI 以特定格式組織輸出（此處為按嚴重性分類的 markdown 清單，你可以貼到 issue 中）。

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### 理解 Git 變更（使用 /review 的重要事項）

在使用 `/review` 指令之前，你需要了解 git 中的兩種變更類型：

| 變更類型 | 含義 | 如何查看 |
|---------|------|----------|
| **已暫存的變更** | 你已用 `git add` 標記為下一次 commit 的檔案 | `git diff --staged` |
| **未暫存的變更** | 你已修改但尚未新增的檔案 | `git diff` |

```bash
# 快速參考
git status           # 顯示已暫存和未暫存的變更
git add file.py      # 暫存檔案以備 commit
git diff             # 顯示未暫存的變更
git diff --staged    # 顯示已暫存的變更
```

### 使用 /review 指令

`/review` 指令調用內建的**程式碼審查 agent**，它針對分析已暫存和未暫存的變更進行了最佳化，提供高信噪比的輸出。使用斜線指令觸發專門的內建 agent，而不是撰寫自由格式的提示。

```bash
copilot

> /review
# 對已暫存/未暫存的變更調用程式碼審查 agent
# 提供聚焦、可行的反饋

> /review Check for security issues in authentication
# 以特定重點領域執行審查
```

> 💡 **提示**：當你有待處理的變更時，程式碼審查 agent 效果最好。用 `git add` 暫存你的檔案以進行更聚焦的審查。

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>工作流程 2：重構</strong> - 重組程式碼、分離關切點、改善錯誤處理</summary>

<img src="images/refactoring-swimlane-single.png" alt="Refactoring workflow: assess code, plan changes, implement, verify behavior." width="800"/>

### 簡單重構

> **先試試這個：** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

從直接的改善開始。在 book app 上試試這些。每個提示使用 `@` 檔案引用配合特定的重構說明，讓 Copilot CLI 確切知道要改什麼。

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **重構新手？** 在處理複雜的轉換之前，先從簡單的請求開始，如新增型別提示或改善變數名稱。

---

<details>
<summary>🎬 看它如何運作！</summary>

![Refactor Demo](images/refactor-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

### 分離關切點

在單一提示中用 `@` 引用多個檔案，讓 Copilot CLI 可以在它們之間移動程式碼作為重構的一部分。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### 改善錯誤處理

提供兩個相關檔案並描述橫切的關切點，讓 Copilot CLI 可以建議跨兩個檔案一致的修正方案。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### 新增文件

使用詳細的項目符號清單指定每個 docstring 應該包含的確切內容。

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### 帶測試的安全重構

在多輪對話中鏈接兩個相關請求。先生成測試，然後以這些測試作為安全網進行重構。

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# 先獲取測試

> Now refactor the BookCollection class to use a context manager for file operations

# 自信地重構 - 測試驗證行為已被保留
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>工作流程 3：調試</strong> - 追蹤 bug、安全審計、跨檔案追蹤問題</summary>

<img src="images/debugging-swimlane-single.png" alt="Debugging workflow: understand error, locate root cause, fix, test." width="800"/>

### 簡單調試

> **先試試這個：** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

從描述問題開始。以下是你可以在有 bug 的 book app 上嘗試的常見調試模式。每個提示將 `@` 檔案引用與清晰的症狀描述配對，讓 Copilot CLI 可以找到並診斷 bug。

```bash
copilot

# 模式：「預期 X 但得到 Y」
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# 模式：「意外的行為」
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# 模式：「錯誤的結果」
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **調試技巧**：描述*症狀*（你看到的）和*期望*（應該發生什麼）。Copilot CLI 會處理其餘的部分。

---

<details>
<summary>🎬 看它如何運作！</summary>

![Fix Bug Demo](images/fix-bug-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

### 「Bug 偵探」- AI 找到相關的 Bug

這是上下文感知調試大放異彩的地方。在有 bug 的 book app 上試試這個場景。透過 `@` 提供整個檔案，只描述用戶報告的症狀。Copilot CLI 將追蹤根本原因，可能還會發現附近的其他 bug。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI 會做什麼**：
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**為什麼這很重要**：Copilot CLI 讀取整個檔案、理解你的 bug 報告的上下文，並給你一個有清晰解釋的具體修正方案。

> 💡 **額外收穫**：因為 Copilot CLI 分析整個檔案，它常常發現你沒有詢問的*其他*問題。例如，在修復作者搜尋時，Copilot CLI 可能也注意到 `find_book_by_title` 中的大小寫敏感 bug！

### 真實世界安全側記

雖然調試自己的程式碼很重要，但理解生產應用中的安全漏洞至關重要。試試這個範例：將 Copilot CLI 指向一個不熟悉的檔案，要求它審計安全問題。

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

這個檔案示範了你在生產應用中會遇到的真實世界安全模式。

> 💡 **你會遇到的常見安全術語：**
> - **SQL Injection（SQL 注入）**：當用戶輸入直接放入資料庫查詢時，允許攻擊者執行惡意指令
> - **Parameterized queries（參數化查詢）**：安全的替代方案——佔位符（`?`）將用戶資料與 SQL 指令分開
> - **Race condition（競爭條件）**：當兩個操作同時發生並相互干擾時
> - **XSS (Cross-Site Scripting)（跨站腳本攻擊）**：攻擊者將惡意腳本注入網頁

---

### 理解錯誤

將堆疊追蹤直接貼入提示中，同時帶上 `@` 檔案引用，讓 Copilot CLI 可以將錯誤映射到源碼。

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### 帶測試案例的調試

描述確切的輸入和觀察到的輸出，為 Copilot CLI 提供一個具體的、可重現的測試案例來推理。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### 在程式碼中追蹤問題

引用多個檔案並要求 Copilot CLI 跨越它們追蹤資料流，以找出問題的起源。

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### 理解資料問題

將資料檔案與讀取它的程式碼一起包含，讓 Copilot CLI 在建議錯誤處理改善時理解完整的圖景。

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>工作流程 4：測試生成</strong> - 自動生成全面的測試和邊緣案例</summary>

<img src="images/test-gen-swimlane-single.png" alt="Test Generation workflow: analyze function, generate tests, include edge cases, run." width="800"/>

> **先試試這個：** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### 「測試爆炸」- 2 個測試 vs 15+ 個測試

手動撰寫測試時，開發者通常會建立 2-3 個基本測試：
- 測試有效輸入
- 測試無效輸入
- 測試一個邊緣案例

看看當你要求 Copilot CLI 生成全面的測試時會發生什麼！這個提示使用帶有 `@` 檔案引用的結構化項目符號清單，引導 Copilot CLI 進行徹底的測試覆蓋：

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 看它如何運作！</summary>

![Test Generation Demo](images/test-gen-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

**你會得到**：15+ 個全面的測試，包括：

```python
class TestBookCollection:
    # 正常路徑
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # 查找操作
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # 邊緣案例
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # 資料持久化
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # 特殊字元
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**結果**：30 秒內，你得到了原本需要一小時思考和撰寫的邊緣案例測試。

---

### 單元測試

針對單一函式並列舉你想要測試的輸入類別，讓 Copilot CLI 生成聚焦、徹底的單元測試。

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### 執行測試

向 Copilot CLI 提出關於你工具鏈的普通英文問題。它可以為你生成正確的 shell 指令。

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI 回應：
# cd samples/book-app-project && python -m pytest tests/
# 或詳細輸出：python -m pytest tests/ -v
# 查看 print 語句：python -m pytest tests/ -s
```

### 針對特定場景測試

列出你想要覆蓋的進階或棘手場景，讓 Copilot CLI 超越正常路徑。

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 在現有檔案中新增測試

要求*額外*針對單一函式的測試，讓 Copilot CLI 生成補充你已有的測試案例。

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>工作流程 5：Git 整合</strong> - Commit 訊息、PR 描述、/pr、/delegate 和 /diff</summary>

<img src="images/git-integration-swimlane-single.png" alt="Git Integration workflow: stage changes, generate message, commit, create PR." width="800"/>

> 💡 **此工作流程假設你具備基本的 git 知識**（暫存、commit、分支）。如果 git 對你是新的，先試試其他四種工作流程。

### 生成 Commit 訊息

> **先試試這個：** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — 暫存一些變更，然後執行這個看 Copilot CLI 撰寫你的 commit 訊息。

此範例使用帶有 shell 指令替換的 `-p` 內聯提示旗標，將 `git diff` 輸出直接傳入 Copilot CLI 以生成一次性的 commit 訊息。`$(...)` 語法執行括號內的指令並將其輸出插入外部指令中。

```bash

# 查看變更了什麼
git diff --staged

# 使用[慣例 Commit](../GLOSSARY-zh_tw.md#conventional-commit) 格式生成 commit 訊息
# （結構化訊息如「feat(books): add search」或「fix(data): handle empty input」）
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# 輸出：「feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors」
```

---

<details>
<summary>🎬 看它如何運作！</summary>

![Git Integration Demo](images/git-integration-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

### 解釋變更

將 `git show` 的輸出傳入 `-p` 提示，以獲取最後一次 commit 的白話文摘要。

```bash
# 這個 commit 改變了什麼？
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR 描述

結合 `git log` 輸出與結構化提示範本，自動生成完整的 pull request 描述。

```bash
# 從分支變更生成 PR 描述
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### 在互動模式中使用 /pr 操作當前分支

如果你在 Copilot CLI 的互動模式中使用分支，可以使用 `/pr` 指令操作 pull request。使用 `/pr` 查看 PR、建立新 PR、修復現有 PR，或讓 Copilot CLI 根據分支狀態自動決定。

```bash
copilot

> /pr [view|create|fix|auto]
```

### 推送前審查

在 `-p` 提示中使用 `git diff main..HEAD`，對所有分支變更進行快速的推送前健全性檢查。

```bash
# 推送前的最後確認
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### 使用 /delegate 執行背景任務

`/delegate` 指令將工作移交給 GitHub Copilot cloud agent。使用 `/delegate` 斜線指令（或 `&` 快捷方式）將明確定義的任務卸載給背景 agent。

```bash
copilot

> /delegate Add input validation to the login form

# 或使用 & 前綴快捷方式：
> & Fix the typo in the README header

# Copilot CLI：
# 1. 將你的變更 commit 到新分支
# 2. 開啟草稿 pull request
# 3. 在 GitHub 上背景工作
# 4. 完成後請求你審查
```

這對於你想在專注於其他工作時完成的明確定義任務很有用。

### 使用 /diff 審查工作階段變更

`/diff` 指令顯示你當前工作階段中所做的所有變更。在 commit 之前，使用這個斜線指令查看 Copilot CLI 修改了什麼的視覺差異。

```bash
copilot

# 做了一些變更之後...
> /diff

# 顯示此工作階段中修改的所有檔案的視覺差異
# 在 commit 之前審查的好方法
```

</details>

---

## 快速提示：在規劃或編寫程式碼前先研究

當你需要調查一個函式庫、了解最佳實踐或探索不熟悉的主題時，在撰寫任何程式碼之前，使用 `/research` 執行深度研究調查：

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot 搜索 GitHub 倉庫和網路來源，然後回傳一個帶有參考資料的摘要。當你即將開始一個新功能並想要先做出明智的決定時，這很有用。你可以使用 `/share` 分享結果。

> 💡 **提示**：`/research` 在 `/plan` *之前*很有效。先研究方法，再規劃實作。

---

## 整合在一起：Bug 修復工作流程

以下是修復已報告 bug 的完整工作流程：

```bash

# 1. 了解 bug 報告
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. 調試問題（在同一工作階段中繼續）
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. 為修正生成測試
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# 4. 生成 commit 訊息
copilot -p "Generate commit message for: $(git diff --staged)"

# 輸出：「fix(books): support partial author name search」
```

### Bug 修復工作流程摘要

| 步驟 | 操作 | Copilot 指令 |
|------|------|--------------|
| 1 | 了解 bug | `> [描述 bug] @relevant-file.py Analyze the likely cause` |
| 2 | 獲得詳細分析 | `> Show me the function and explain the issue` |
| 3 | 實作修正 | `> Fix the [specific issue]` |
| 4 | 生成測試 | `> Generate tests for [specific scenarios]` |
| 5 | Commit | `copilot -p "Generate commit message for: $(git diff --staged)"` |

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

現在輪到你運用這些工作流程了。

---

## ▶️ 自己試試看

完成示範後，試試這些變體：

1. **Bug 偵探挑戰**：請 Copilot CLI 調試 `samples/book-app-buggy/books_buggy.py` 中的 `mark_as_read` 函式。它解釋了為什麼該函式標記了所有書籍為已讀而不只是一本嗎？

2. **測試挑戰**：為 book app 中的 `add_book` 函式生成測試。計算 Copilot CLI 包含了多少你不會想到的邊緣案例。

3. **Commit 訊息挑戰**：對 book app 檔案做任何小改動，暫存它（`git add .`），然後執行：
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   這個訊息比你快速寫的更好嗎？

**自我檢查**：當你能解釋為什麼「debug this bug」比「find bugs」更強大時（上下文很重要！），你就理解了開發工作流程。

---

## 📝 作業

### 主要挑戰：重構、測試和發布

實際操作範例專注於 `find_book_by_title` 和程式碼審查。現在在 `book-app-project` 中的不同函式上練習相同的工作流程技能：

1. **審查**：請 Copilot CLI 審查 `books.py` 中的 `remove_book()` 函式的邊緣案例和潛在問題：
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **重構**：請 Copilot CLI 改善 `remove_book()` 以處理邊緣案例，如大小寫不敏感的比對，以及在找不到書籍時返回有用的反饋
3. **測試**：專門為改善後的 `remove_book()` 函式生成 pytest 測試，涵蓋：
   - 移除存在的書籍
   - 大小寫不敏感的標題比對
   - 不存在的書籍返回適當的反饋
   - 從空集合中移除
4. **審查**：暫存你的變更並執行 `/review` 檢查任何剩餘問題
5. **Commit**：生成慣例 commit 訊息：
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 提示（點擊展開）</summary>

**每個步驟的範例提示：**

```bash
copilot

# 步驟 1：審查
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# 步驟 2：重構
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# 步驟 3：測試
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# 步驟 4：審查
> /review

# 步驟 5：Commit
> Generate a conventional commit message for this refactor
```

**提示：** 改善 `remove_book()` 後，試著問 Copilot CLI：「Are there any other functions in this file that could benefit from the same improvements?」它可能會建議對 `find_book_by_title()` 或 `find_by_author()` 進行類似的改動。

</details>

### 額外挑戰：使用 Copilot CLI 建立應用程式

> 💡 **注意**：這個 GitHub Skills 練習使用 **Node.js** 而非 Python。你將練習的 GitHub Copilot CLI 技術——建立 issue、生成程式碼和從終端機協作——適用於任何語言。

這個練習展示了開發者如何使用 GitHub Copilot CLI 建立 issue、生成程式碼，並在建立 Node.js 計算機應用程式的同時從終端機協作。你將安裝 CLI、使用範本和 agent，並練習迭代式、由指令行驅動的開發。

##### <img src="../images/github-skills-logo.png" width="28" align="center" /> [開始「使用 Copilot CLI 建立應用程式」Skills 練習](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 會發生什麼 | 修正方法 |
|------|------------|----------|
| 使用模糊的提示如「Review this code」 | 遺漏特定問題的通用反饋 | 具體說明：「Review for SQL injection, XSS, and auth issues」 |
| 不使用 `/review` 進行程式碼審查 | 錯過最佳化的程式碼審查 agent | 使用針對高信噪比輸出調整的 `/review` |
| 在沒有上下文的情況下要求「find bugs」 | Copilot CLI 不知道你遇到了什麼 bug | 描述症狀：「Users report X happens when Y」 |
| 生成測試時不指定框架 | 測試可能使用錯誤的語法或斷言函式庫 | 指定：「Generate tests using Jest」或「using pytest」 |

### 疑難排解

**審查似乎不完整** - 對要查找的內容更加具體：

```bash
copilot

# 不要這樣：
> Review @samples/book-app-project/book_app.py

# 試試這樣：
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**測試不匹配我的框架** - 指定框架：

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**重構改變了行為** - 要求 Copilot CLI 保留行為：

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# 摘要

## 🔑 重點收穫

<img src="images/specialized-workflows.png" alt="Specialized Workflows for Every Task: Code Review, Refactoring, Debugging, Testing, and Git Integration" width="800"/>

1. **程式碼審查**透過具體的提示變得全面
2. **重構**在先生成測試時更安全
3. **調試**受益於向 Copilot CLI 同時展示錯誤和程式碼
4. **測試生成**應該包含邊緣案例和錯誤場景
5. **Git 整合**自動化 commit 訊息和 PR 描述

> 📋 **快速參考**：參閱 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference) 獲取完整的指令和快捷鍵列表。

---

## ✅ 檢查點：你已掌握基礎知識

**恭喜！** 你現在擁有使用 GitHub Copilot CLI 提高生產力所需的所有核心技能：

| 技能 | 章節 | 你現在可以... |
|------|------|--------------|
| 基本指令 | Ch 01 | 使用互動模式、計畫模式、程式化模式（-p）和斜線指令 |
| 上下文 | Ch 02 | 用 `@` 引用檔案、管理工作階段、理解上下文視窗 |
| 工作流程 | Ch 03 | 審查程式碼、重構、調試、生成測試、整合 git |

Chapter 04-06 涵蓋了增加更多能力的額外功能，值得學習。

---

## 🛠️ 建立你的個人工作流程

使用 GitHub Copilot CLI 沒有唯一「正確」的方式。以下是一些你在發展自己的模式時的提示：

> 📚 **官方文件**：[Copilot CLI 最佳實踐](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices) 提供來自 GitHub 的推薦工作流程和提示。

- **從 `/plan` 開始**處理任何非瑣碎的事情。在執行前完善計畫——好的計畫帶來更好的結果。
- **儲存效果好的提示。** 當 Copilot CLI 出錯時，記錄哪裡出了問題。隨著時間推移，這成為你的個人手冊。
- **自由實驗。** 一些開發者偏好長而詳細的提示。其他人偏好帶有後續問題的短提示。嘗試不同的方法，注意什麼感覺自然。

> 💡 **即將推出**：在 Chapter 04 和 05 中，你將學習如何將你的最佳實踐編碼為 Copilot CLI 自動載入的自訂說明和 skill。

---

## ➡️ 接下來是什麼

其餘章節涵蓋延伸 Copilot CLI 功能的額外特性：

| 章節 | 涵蓋內容 | 何時需要 |
|------|----------|----------|
| Ch 04: Agents | 建立專門的 AI 人物角色 | 當你想要領域專家（前端、安全）時 |
| Ch 05: Skills | 為任務自動載入說明 | 當你反覆使用相同的提示時 |
| Ch 06: MCP | 連接外部服務 | 當你需要來自 GitHub、資料庫的即時資料時 |

**建議**：試用核心工作流程一週，然後在你有具體需求時再回來看 Chapter 04-06。

---

## 繼續到額外主題

在 **[Chapter 04: Agents and Custom Instructions](../04-agents-custom-instructions/README-zh_tw.md)** 中，你將學習：

- 使用內建 agent（`/plan`、`/review`）
- 使用 `.agent.md` 檔案建立專門的 agent（前端專家、安全審計員）
- 多 agent 協作模式
- 用於專案標準的自訂說明檔案

---

**[← 返回 Chapter 02](../02-context-conversations/README-zh_tw.md)** | **[繼續到 Chapter 04 →](../04-agents-custom-instructions/README-zh_tw.md)**
