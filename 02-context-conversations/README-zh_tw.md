![Chapter 02: Context and Conversations](images/chapter-header.png)

> **如果 AI 能看到你的整個程式碼庫，而不只是一次一個檔案，會怎樣？**

在本章中，你將解鎖 GitHub Copilot CLI 的真正力量：脈絡（context）。你將學習使用 `@` 語法來參照檔案和目錄，讓 Copilot CLI 深入理解你的程式碼庫。你將發現如何跨工作階段維持對話、幾天後從離開的地方精確地繼續，並看到跨檔案分析如何捕捉到單一檔案審查完全遺漏的錯誤。

## 🎯 學習目標

完成本章後，你將能夠：

- 使用 `@` 語法參照檔案、目錄和圖片
- 使用 `--resume` 和 `--continue` 恢復先前的工作階段
- 了解[脈絡視窗](../GLOSSARY.md#context-window)的運作方式
- 撰寫有效的多輪對話
- 管理多專案工作流程的目錄權限

> ⏱️ **預估時間**：約 50 分鐘（閱讀 20 分鐘 + 實作 30 分鐘）

---

## 🧩 真實世界類比：與同事協作

<img src="images/colleague-context-analogy.png" alt="Context Makes the Difference - Without vs With Context" width="800"/>

*就像你的同事一樣，Copilot CLI 不會讀心術。提供更多資訊有助於人類和 Copilot 提供針對性的協助！*

想像向同事解釋一個錯誤：

> **沒有脈絡**：「book app 壞了。」

> **有脈絡**：「看一下 `books.py`，特別是 `find_book_by_title` 函式。它沒有做大小寫不敏感的比對。」

要向 Copilot CLI 提供脈絡，請使用 *`@` 語法*將 Copilot CLI 指向特定檔案。

---

# 基本：基礎脈絡

<img src="images/essential-basic-context.png" alt="Glowing code blocks connected by light trails representing how context flows through Copilot CLI conversations" width="800"/>

本節涵蓋有效使用脈絡所需的一切。先掌握這些基礎。

---

## @ 語法

`@` 符號在你的提示詞中參照檔案和目錄。這是你告訴 Copilot CLI「看這個檔案」的方式。

> 💡 **注意**：本課程中所有範例都使用儲存庫中包含的 `samples/` 資料夾，所以你可以直接嘗試每一個指令。

### 現在就試試（無需任何設定）

你可以用電腦上的任何檔案嘗試：

```bash
copilot

# 指向你有的任何檔案
> Explain what @package.json does
# 中文 Prompt：解釋 @package.json 在做什麼
> Summarize @README.md
# 中文 Prompt：摘要 @README.md 的內容
> What's in @.gitignore and why?
# 中文 Prompt：@.gitignore 裡有什麼，為什麼？
```

> 💡 **手邊沒有專案？** 建立一個快速測試檔案：
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本 @ 模式

| 模式 | 功能 | 使用範例 |
|------|------|---------|
| `@file.py` | 參照單一檔案 | `Review @samples/book-app-project/books.py` |
| `@folder/` | 參照目錄中的所有檔案 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 參照多個檔案 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 參照單一檔案

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
# 中文 Prompt：解釋 @samples/book-app-project/utils.py 在做什麼
```

---

<details>
<summary>🎬 看它實際運作！</summary>

![File Context Demo](images/file-context-demo.gif)

*示範輸出因情況而異。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

### 參照多個檔案

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
# 中文 Prompt：比較 @samples/book-app-project/book_app.py 和 @samples/book-app-project/books.py 的一致性
```

### 參照整個目錄

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
# 中文 Prompt：review @samples/book-app-project/ 中所有檔案的 error handling
```

---

## 跨檔案智慧

這就是脈絡成為超能力的地方。單一檔案分析很有用。跨檔案分析則能帶來革命性變化。

<img src="images/cross-file-intelligence.png" alt="Cross-File Intelligence - comparing single-file vs cross-file analysis showing how analyzing files together reveals bugs, data flow, and patterns invisible in isolation" width="800"/>

### 示範：找出跨多個檔案的錯誤

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
# 中文 Prompt：這些檔案如何協同工作？資料流是什麼？
```

> 💡 **進階選項**：若要進行以安全為重點的跨檔案分析，試試 Python 安全範例：
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 看它實際運作！</summary>

![Multi-File Demo](images/multi-file-demo.gif)

*示範輸出因情況而異。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

**Copilot CLI 發現的內容**：

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**為什麼這很重要**：單一檔案審查會錯過更大的整體圖像。只有跨檔案分析才能揭示：
- 應該整合的**重複程式碼**
- 顯示元件如何互動的**資料流模式**
- 影響可維護性的**架構問題**

---

### 示範：60 秒內了解一個程式碼庫

<img src="images/codebase-understanding.png" alt="Split-screen comparison showing manual code review taking 1 hour versus AI-assisted analysis taking 10 seconds" width="800" />

剛加入一個專案嗎？使用 Copilot CLI 快速了解它。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
# 中文 Prompt：用一段話說明這個 app 做什麼，以及它最大的 code quality 問題是什麼？
```

**你得到的結果**：
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**結果**：原本需要一個小時閱讀程式碼的工作，壓縮到 10 秒內完成。你確切知道該把精力放在哪裡。

---

## 實際範例

### 範例 1：帶脈絡的程式碼審查

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs
# 中文 Prompt：review @samples/book-app-project/books.py 這個檔案是否有潛在的 bug

# Copilot CLI 現在擁有完整的檔案內容，可以給出具體反饋：
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?
# 中文 Prompt：那 @samples/book-app-project/book_app.py 呢？

# 現在審查 book_app.py，但仍然了解 books.py 的脈絡
```

### 範例 2：了解一個程式碼庫

```bash
copilot

> @samples/book-app-project/books.py What does this module do?
# 中文 Prompt：@samples/book-app-project/books.py 這個模組在做什麼？

# Copilot CLI 讀取 books.py 並理解 BookCollection 類別

> @samples/book-app-project/ Give me an overview of the code structure
# 中文 Prompt：給我 @samples/book-app-project/ 的程式碼結構概覽

# Copilot CLI 掃描目錄並進行摘要

> How does the app save and load books?
# 中文 Prompt：這個 app 如何儲存和載入書籍資料？

# Copilot CLI 可以追蹤它已看過的程式碼
```

<details>
<summary>🎬 看多輪對話實際運作！</summary>

![Multi-Turn Demo](images/multi-turn-demo.gif)

*示範輸出因情況而異。你的模型、工具和回應將與此處顯示的不同。*

</details>

### 範例 3：多檔案重構

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.
# 中文 Prompt：我看到有重複的顯示函式：show_books() 和 print_books()。幫我把它們合併。

# Copilot CLI 看到兩個檔案，可以建議如何合併重複的程式碼
```

---

## 工作階段管理

工作階段在你工作時會自動儲存。你可以恢復先前的工作階段，從離開的地方繼續。

### 工作階段自動儲存

每次對話都會自動儲存。正常退出即可：

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules
# 中文 Prompt：讓我們改善 @samples/book-app-project/ 中所有模組的 error handling

[... 進行一些工作 ...]

> /exit
```

### 恢復最近的工作階段

```bash
# 從離開的地方繼續
copilot --continue
```

### 恢復特定工作階段

```bash
# 從互動式列表中選擇工作階段
copilot --resume

# 或透過 ID 恢復特定工作階段
copilot --resume abc123
```

> 💡 **如何找到工作階段 ID？** 你不需要記住它們。執行 `copilot --resume`（不帶 ID）會顯示你先前工作階段的互動式列表，包含名稱、ID 和最後活躍時間。只需選擇你想要的即可。
>
> **多個終端機視窗怎麼辦？** 每個終端機視窗都是自己的工作階段，有自己的脈絡。如果你在三個終端機中開啟 Copilot CLI，那就是三個獨立的工作階段。從任何終端機執行 `--resume` 都可以瀏覽所有工作階段。`--continue` 旗標會抓取最近關閉的工作階段，無論它在哪個終端機中。
>
> **可以不重啟就切換工作階段嗎？** 可以。在活躍工作階段中使用 `/resume` slash 指令：
> ```
> > /resume
> # 顯示可切換到的工作階段列表
> ```

### 整理你的工作階段

給工作階段有意義的名稱，方便日後尋找：

```bash
copilot

> /rename book-app-review
# 工作階段已重新命名，方便識別
```

### 檢查和管理脈絡

隨著你新增檔案和對話，Copilot CLI 的[脈絡視窗](../GLOSSARY.md#context-window)會逐漸填滿。有幾個指令可以幫助你掌控：

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 放棄當前工作階段（不儲存歷史記錄）並開始新的對話

> /new
# 結束當前工作階段（儲存到歷史記錄以供搜尋/恢復）並開始新的對話

> /rewind
# 開啟時間軸選擇器，讓你回滾到對話中較早的時間點
```

> 💡 **何時使用 `/clear` 或 `/new`**：如果你一直在審查 books.py 並想切換到討論 utils.py，請先執行 /new（如果不需要工作階段歷史記錄則使用 /clear）。否則，舊話題的過時脈絡可能會讓新話題的回應產生混亂。

> 💡 **犯了錯誤或想嘗試不同方式？** 使用 `/rewind`（或按兩下 Esc）開啟**時間軸選擇器**，讓你回滾到對話中任何較早的時間點，不僅僅是最近的一個。當你走了彎路並想回頭，但又不想完全重新開始時，這非常有用。

---

### 從離開的地方繼續

<img src="images/session-persistence-timeline.png" alt="Timeline showing how GitHub Copilot CLI sessions persist across days - start on Monday, resume on Wednesday with full context restored" width="800"/>

*工作階段在你退出時自動儲存。幾天後恢復，完整脈絡仍在：檔案、問題和進度全都被記住了。*

想像這個跨多天的工作流程：

```bash
# 週一：開始 book app 審查
copilot

> /rename book-app-review
> @samples/book-app-project/books.py
> Review and number all code quality issues
# 中文 Prompt：review 並為所有 code quality 問題編號

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# 中文 Prompt：fix 問題 #1（重複的函式）
# 進行修復...

> /exit
```

```bash
# 週三：從離開的地方繼續
copilot --continue

> What issues remain unfixed from our book app review?
# 中文 Prompt：我們的 book app review 還有哪些問題尚未 fix？

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
# 中文 Prompt：接下來處理問題 #2
```

**讓這個功能強大的原因**：幾天後，Copilot CLI 仍然記得：
- 你正在處理的確切檔案
- 問題的編號列表
- 你已經解決了哪些問題
- 你的對話脈絡

不需要重新解釋。不需要重新閱讀檔案。直接繼續工作。

---

**🎉 你現在已經掌握基礎知識了！** `@` 語法、工作階段管理（`--continue`/`--resume`/`/rename`）和脈絡指令（`/context`/`/clear`）已足以讓你高效工作。以下內容都是選用的。準備好時再回來看。

---

# 選用：深入探索

<img src="images/optional-going-deeper.png" alt="Abstract crystal cave in blue and purple tones representing deeper exploration of context concepts" width="800"/>

這些主題建立在上方基礎知識之上。**選擇你感興趣的，或直接跳到[練習](#practice)。**

| 我想學習... | 跳到 |
|---|---|
| 萬用字元模式和進階工作階段指令 | [其他 @ 模式與工作階段指令](#additional-patterns) |
| 在多個提示詞中建立脈絡 | [脈絡感知對話](#context-aware-conversations) |
| Token 限制和 `/compact` | [了解脈絡視窗](#understanding-context-windows) |
| 如何選擇要參照的正確檔案 | [選擇參照的內容](#choosing-what-to-reference) |
| 分析螢幕截圖和原型設計稿 | [使用圖片](#working-with-images) |

<details>
<summary><strong>其他 @ 模式與工作階段指令</strong></summary>
<a id="additional-patterns"></a>

### 其他 @ 模式

對於進階使用者，Copilot CLI 支援萬用字元模式和圖片參照：

| 模式 | 功能 |
|------|------|
| `@folder/*.py` | 資料夾中的所有 .py 檔案 |
| `@**/test_*.py` | 遞迴萬用字元：尋找任何地方的所有測試檔案 |
| `@image.png` | 用於 UI 審查的圖片檔案 |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
# 中文 Prompt：找出 @samples/book-app-project/**/*.py 中所有的 TODO 註解
```

### 檢視工作階段資訊

```bash
copilot

> /session
# 顯示當前工作階段詳情和工作區摘要

> /usage
# 顯示工作階段指標和統計資料
```

### 分享你的工作階段

```bash
copilot

> /share file ./my-session.md
# 將工作階段匯出為 markdown 檔案

> /share gist
# 建立包含工作階段的 GitHub gist

> /share html
# 將工作階段匯出為獨立的互動式 HTML 檔案
# 適合與團隊成員分享精美的工作階段報告或儲存以供參考
```

</details>

<details>
<summary><strong>脈絡感知對話</strong></summary>
<a id="context-aware-conversations"></a>

### 脈絡感知對話

當你進行相互建立的多輪對話時，魔法就發生了。

#### 範例：漸進式增強

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class
# 中文 Prompt：review @samples/book-app-project/books.py 中的 BookCollection 類別

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods
# 中文 Prompt：為所有方法加上 type hints

Copilot CLI: "Here's the class with complete type hints..."
[Shows typed version]

> Now improve error handling
# 中文 Prompt：現在改善 error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[Adds validation and proper exceptions]

> Generate tests for this final version
# 中文 Prompt：為這個最終版本產生 test

Copilot CLI: "Based on the class with types and error handling..."
[Generates comprehensive tests]
```

注意每個提示詞如何建立在前一個工作的基礎上。這就是脈絡的力量。

</details>

<details>
<summary><strong>了解脈絡視窗</strong></summary>
<a id="understanding-context-windows"></a>

### 了解脈絡視窗

你已從基礎知識中了解 `/context` 和 `/clear`。以下是脈絡視窗運作方式的更深層說明。

每個 AI 都有一個「脈絡視窗」，即它一次可以考慮的文字量。

<img src="images/context-window-visualization.png" alt="Context Window Visualization" width="800"/>

*脈絡視窗就像一張桌子：一次只能容納這麼多東西。檔案、對話歷史記錄和系統提示詞都佔用空間。*

#### 達到限制時會發生什麼

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# 隨著你新增更多檔案和對話，這個數字會增長

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 警告：接近脈絡限制

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` 指令

當你的脈絡快滿但不想失去對話時，`/compact` 會摘要你的歷史記錄以釋放 token：

```bash
copilot

> /compact
# 摘要對話歷史記錄，釋放脈絡空間
# 保留你的關鍵發現和決策
```

#### 脈絡效率提示

| 情況 | 操作 | 原因 |
|------|------|------|
| 開始新話題 | `/clear` | 移除不相關的脈絡 |
| 走了彎路 | `/rewind` | 回滾到任何較早的時間點 |
| 對話很長 | `/compact` | 摘要歷史記錄，釋放 token |
| 需要特定檔案 | 用 `@file.py` 而非 `@folder/` | 只載入你需要的 |
| 達到限制 | `/new` 或 `/clear` | 全新脈絡 |
| 多個話題 | 每個話題使用 `/rename` | 方便恢復正確的工作階段 |

#### 大型程式碼庫的最佳實踐

1. **要具體**：用 `@samples/book-app-project/books.py` 而非 `@samples/book-app-project/`
2. **在話題之間清除脈絡**：切換焦點時使用 `/new` 或 `/clear`
3. **使用 `/compact`**：摘要對話以釋放脈絡
4. **使用多個工作階段**：每個功能或話題一個工作階段

</details>

<details>
<summary><strong>選擇參照的內容</strong></summary>
<a id="choosing-what-to-reference"></a>

### 選擇參照的內容

在脈絡方面，並非所有檔案都是平等的。以下是如何明智地選擇：

#### 檔案大小考量

| 檔案大小 | 大約 [Token](../GLOSSARY.md#token) 數 | 策略 |
|---------|--------------------------------------|------|
| 小型（< 100 行） | 約 500-1,500 tokens | 自由參照 |
| 中型（100-500 行） | 約 1,500-7,500 tokens | 參照特定檔案 |
| 大型（500+ 行） | 7,500+ tokens | 有選擇性地使用特定檔案 |
| 非常大型（1000+ 行） | 15,000+ tokens | 考慮分割或針對特定區段 |

**具體範例：**
- book app 的 4 個 Python 檔案合計約 2,000-3,000 tokens
- 典型的 Python 模組（200 行）約 3,000 tokens
- Flask API 檔案（400 行）約 6,000 tokens
- 你的 package.json 約 200-500 tokens
- 簡短的提示詞 + 回應約 500-1,500 tokens

> 💡 **程式碼的快速估算：** 將程式碼行數乘以約 15 以得到大約的 token 數。請注意這只是估算。

#### 應包含與排除的內容

**高價值**（包含這些）：
- 入口點（`book_app.py`、`main.py`、`app.py`）
- 你詢問的特定檔案
- 目標檔案直接匯入的檔案
- 設定檔（`requirements.txt`、`pyproject.toml`）
- 資料模型或 dataclass

**較低價值**（考慮排除）：
- 產生的檔案（編譯輸出、打包資產）
- Node modules 或 vendor 目錄
- 大型資料檔案或 fixture
- 與你的問題無關的檔案

#### 具體程度的光譜

```
較不具體 ────────────────────────► 更具體
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ 掃描所有內容                           └─ 只取你需要的
        （使用更多脈絡）                           （保留脈絡）
```

**何時使用廣泛參照**（`@samples/book-app-project/`）：
- 初始程式碼庫探索
- 在多個檔案中尋找模式
- 架構審查

**何時使用具體參照**（`@samples/book-app-project/books.py`）：
- 除錯特定問題
- 審查特定檔案的程式碼
- 詢問單一函式

#### 實際範例：分階段載入脈絡

```bash
copilot

# 步驟 1：從結構開始
> @package.json What frameworks does this project use?
# 中文 Prompt：@package.json 這個專案使用了哪些框架？

# 步驟 2：根據答案縮小範圍
> @samples/book-app-project/ Show me the project structure
# 中文 Prompt：顯示 @samples/book-app-project/ 的專案結構

# 步驟 3：專注於重要的部分
> @samples/book-app-project/books.py Review the BookCollection class
# 中文 Prompt：review @samples/book-app-project/books.py 中的 BookCollection 類別

# 步驟 4：只在需要時新增相關檔案
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
# 中文 Prompt：CLI 如何使用 @samples/book-app-project/book_app.py 和 @samples/book-app-project/books.py 中的 BookCollection？
```

這種分階段方式讓脈絡保持專注和高效。

</details>

<details>
<summary><strong>使用圖片</strong></summary>
<a id="working-with-images"></a>

### 使用圖片

你可以使用 `@` 語法在對話中包含圖片，或直接**從剪貼簿貼上**（Cmd+V / Ctrl+V）。Copilot CLI 可以分析螢幕截圖、原型設計稿和圖表，以協助 UI 除錯、設計實作和錯誤分析。

```bash
copilot

> @images/screenshot.png What is happening in this image?
# 中文 Prompt：@images/screenshot.png 這張圖片裡發生了什麼事？

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
# 中文 Prompt：根據 @images/mockup.png 寫出符合這個設計的 HTML 和 CSS，放在新檔案 index.html 中，CSS 放在 styles.css。
```

> 📖 **深入了解**：查看[其他脈絡功能](../appendices/additional-context.md#working-with-images)了解支援的格式、實際使用案例和結合圖片與程式碼的技巧。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

是時候應用你的脈絡和工作階段管理技能了。

---

## ▶️ 親自嘗試

### 完整專案審查

本課程包含你可以直接審查的範例檔案。啟動 copilot 並執行下方顯示的提示詞：

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project
# 中文 Prompt：給我 @samples/book-app-project/ 的 code quality review

# Copilot CLI 將識別出問題，例如：
# - 重複的顯示函式
# - 缺少輸入驗證
# - 不一致的錯誤處理
```

> 💡 **想用自己的檔案試試看？** 建立一個小型 Python 專案（`mkdir -p my-project/src`），新增一些 .py 檔案，然後使用 `@my-project/src/` 來審查它們。如果你需要，可以請 copilot 為你建立範例程式碼！

### 工作階段工作流程

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles
# 中文 Prompt：讓我們為 @samples/book-app-project/books.py 加入空白標題的輸入驗證

[Copilot CLI 建議驗證方式]

> Implement that fix
# 中文 Prompt：實作那個 fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
# 中文 Prompt：現在整合 @samples/book-app-project/ 中重複的顯示函式
> /exit

# 稍後——從離開的地方繼續
copilot --continue

> Generate tests for the changes we made
# 中文 Prompt：為我們所做的變更產生 test
```

---

完成示範後，試試這些變化：

1. **跨檔案挑戰**：分析 book_app.py 和 books.py 如何協同工作：
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   # 中文 Prompt：這些檔案之間的關係是什麼？有沒有 code smells？
   ```

2. **工作階段挑戰**：開始一個工作階段，用 `/rename my-first-session` 命名它，做一些工作，用 `/exit` 退出，然後執行 `copilot --continue`。它記得你在做什麼嗎？

3. **脈絡挑戰**：在工作階段中執行 `/context`。你使用了多少 token？試試 `/compact` 然後再檢查一次。（參見「深入探索」中的[了解脈絡視窗](#understanding-context-windows)以了解更多關於 `/compact` 的內容。）

**自我檢核**：當你能解釋為什麼 `@folder/` 比逐一開啟每個檔案更強大時，你就理解了脈絡。

---

## 📝 作業

### 主要挑戰：追蹤資料流

實作範例專注於程式碼品質審查和輸入驗證。現在在不同的任務上練習相同的脈絡技能——追蹤資料如何在應用程式中流動：

1. 啟動互動式工作階段：`copilot`
2. 同時參照 `books.py` 和 `book_app.py`：
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. 引入資料檔案以獲取額外脈絡：
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. 請求跨檔案改善：
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. 重新命名工作階段：`/rename data-flow-analysis`
6. 用 `/exit` 退出，然後用 `copilot --continue` 恢復，並詢問關於資料流的後續問題

**成功標準**：你能夠跨多個檔案追蹤資料，恢復已命名的工作階段，並獲得跨檔案建議。

<details>
<summary>💡 提示（點擊展開）</summary>

**開始方式：**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
# 中文 Prompt：追蹤一本書從使用者輸入到儲存在 data.json 的完整流程
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
# 中文 Prompt：如果 @samples/book-app-project/data.json 這個檔案遺失或損毀會發生什麼？
> /rename data-flow-analysis
> /exit
```

然後用 `copilot --continue` 恢復

**實用指令：**
- `@file.py` - 參照單一檔案
- `@folder/` - 參照資料夾中的所有檔案（注意尾部的 `/`）
- `/context` - 檢查你使用了多少脈絡
- `/rename <name>` - 命名你的工作階段以方便恢復

</details>

### 進階挑戰：脈絡限制

1. 使用 `@samples/book-app-project/` 一次參照所有 book app 檔案
2. 詢問關於不同檔案的幾個詳細問題（`books.py`、`utils.py`、`book_app.py`、`data.json`）
3. 執行 `/context` 查看使用情況。它填滿的速度有多快？
4. 練習使用 `/compact` 回收空間，然後繼續對話
5. 嘗試使用更具體的檔案參照（例如，用 `@samples/book-app-project/books.py` 而非整個資料夾），看看這如何影響脈絡使用量

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 發生的情況 | 修正方式 |
|------|-----------|---------|
| 忘記在檔案名稱前加 `@` | Copilot CLI 將「books.py」視為純文字 | 使用 `@samples/book-app-project/books.py` 來參照檔案 |
| 期望工作階段自動持久化 | 全新啟動 `copilot` 會失去所有先前的脈絡 | 使用 `--continue`（最後一個工作階段）或 `--resume`（選擇工作階段） |
| 參照當前目錄之外的檔案 | 「Permission denied」或「File not found」錯誤 | 使用 `/add-dir /path/to/directory` 授予存取權限 |
| 切換話題時不使用 `/clear` | 舊脈絡讓新話題的回應產生混亂 | 開始不同任務前執行 `/clear` |

### 疑難排解

**「File not found」錯誤** - 確保你在正確的目錄：

```bash
pwd  # 檢查當前目錄
ls   # 列出檔案

# 然後啟動 copilot 並使用相對路徑
copilot

> Review @samples/book-app-project/books.py
# 中文 Prompt：review @samples/book-app-project/books.py
```

**「Permission denied」** - 將目錄新增到允許清單：

```bash
copilot --add-dir /path/to/directory

# 或在工作階段中：
> /add-dir /path/to/directory
```

**脈絡填滿太快**：
- 使用更具體的檔案參照
- 在不同話題之間使用 `/clear`
- 將工作分散到多個工作階段

</details>

---

# 摘要

## 🔑 重點收穫

1. **`@` 語法**讓 Copilot CLI 了解關於檔案、目錄和圖片的脈絡
2. **多輪對話**隨著脈絡積累而相互建立
3. **工作階段自動儲存**：使用 `--continue` 或 `--resume` 從離開的地方繼續
4. **脈絡視窗**有限制：使用 `/clear`、`/compact`、`/context`、`/new` 和 `/rewind` 管理它們
5. **權限旗標**（`--add-dir`、`--allow-all`）控制多目錄存取。明智使用！
6. **圖片參照**（`@screenshot.png`）幫助視覺化地除錯 UI 問題

> 📚 **官方文件**：[使用 Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli)提供關於脈絡、工作階段和使用檔案的完整參考。

> 📋 **快速參考**：查看 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference)取得完整的指令和快捷鍵列表。

---

## ➡️ 下一步

現在你可以為 Copilot CLI 提供脈絡了，讓我們將它應用在真實的開發任務上。你剛學到的脈絡技術（檔案參照、跨檔案分析和工作階段管理）是下一章強大工作流程的基礎。

在 **[Chapter 03: Development Workflows](../03-development-workflows/README-zh_tw.md)** 中，你將學習：

- 程式碼審查工作流程
- 重構模式
- 除錯輔助
- 測試產生
- Git 整合

---

**[← 返回 Chapter 01](../01-setup-and-first-steps/README-zh_tw.md)** | **[繼續到 Chapter 03 →](../03-development-workflows/README-zh_tw.md)**
