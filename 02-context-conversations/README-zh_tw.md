![Chapter 02: Context and Conversations](images/chapter-header.png)

> **如果 AI 能看到你整個程式碼庫，而不只是一次一個檔案，會怎麼樣？**

在本章中，你將解鎖 GitHub Copilot CLI 的真正力量：上下文。你將學習使用 `@` 語法來引用檔案和目錄，讓 Copilot CLI 深入理解你的程式碼庫。你將發現如何在工作階段之間保持對話、幾天後準確地從離開的地方繼續，並看到跨檔案分析如何能捕捉到單一檔案審查完全遺漏的 bug。

## 🎯 學習目標

完成本章後，你將能夠：

- 使用 `@` 語法引用檔案、目錄和圖片
- 使用 `--resume` 和 `--continue` 恢復之前的工作階段
- 理解[上下文視窗](../GLOSSARY-zh_tw.md#context-window)的運作方式
- 撰寫有效的多輪對話
- 管理多專案工作流程的目錄權限

> ⏱️ **預估時間**：約 50 分鐘（20 分鐘閱讀 + 30 分鐘實際操作）

---

## 🧩 真實世界類比：與同事合作

<img src="images/colleague-context-analogy.png" alt="Context Makes the Difference - Without vs With Context" width="800"/>

*就像你的同事一樣，Copilot CLI 不是讀心術師。提供更多資訊有助於人類和 Copilot 提供有針對性的支援！*

想像向同事解釋一個 bug：

> **沒有上下文**：「book app 壞掉了。」

> **有上下文**：「看看 `books.py`，特別是 `find_book_by_title` 函式。它沒有做大小寫不敏感的比對。」

要向 Copilot CLI 提供上下文，請使用 *`@` 語法*將 Copilot CLI 指向特定檔案。

---

# 必學：基本上下文

<img src="images/essential-basic-context.png" alt="Glowing code blocks connected by light trails representing how context flows through Copilot CLI conversations" width="800"/>

本節涵蓋有效使用上下文所需的一切。先掌握這些基礎。

---

## @ 語法

`@` 符號在你的提示中引用檔案和目錄。這是你告訴 Copilot CLI「看這個檔案」的方式。

> 💡 **注意**：本課程中的所有範例都使用此倉庫中包含的 `samples/` 資料夾，因此你可以直接嘗試每個指令。

### 立即試試（無需設定）

你可以用電腦上的任何檔案試試這個：

```bash
copilot

# 指向你有的任何檔案
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **手邊沒有專案？** 建立一個快速測試檔案：
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本 @ 模式

| 模式 | 功能 | 使用範例 |
|------|------|----------|
| `@file.py` | 引用單一檔案 | `Review @samples/book-app-project/books.py` |
| `@folder/` | 引用目錄中的所有檔案 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 引用多個檔案 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 引用單一檔案

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 看它如何運作！</summary>

![File Context Demo](images/file-context-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

### 引用多個檔案

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### 引用整個目錄

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## 跨檔案智慧

這是上下文成為超能力的地方。單一檔案分析很有用。跨檔案分析則是革命性的。

<img src="images/cross-file-intelligence.png" alt="Cross-File Intelligence - comparing single-file vs cross-file analysis showing how analyzing files together reveals bugs, data flow, and patterns invisible in isolation" width="800"/>

### 示範：找出跨越多個檔案的 Bug

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **進階選項**：對於以安全為重點的跨檔案分析，試試 Python 安全範例：
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 看它如何運作！</summary>

![Multi-File Demo](images/multi-file-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

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

**為什麼這很重要**：單一檔案審查會錯過更大的圖景。只有跨檔案分析才能揭示：
- **重複程式碼**應該被整合
- **資料流模式**顯示元件如何互動
- **架構問題**影響可維護性

---

### 示範：60 秒內理解程式碼庫

<img src="images/codebase-understanding.png" alt="Split-screen comparison showing manual code review taking 1 hour versus AI-assisted analysis taking 10 seconds" width="800" />

剛加入一個專案？使用 Copilot CLI 快速了解它。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**你會得到的內容**：
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**結果**：把原本需要一小時閱讀程式碼的工作壓縮成 10 秒。你確切地知道該把重點放在哪裡。

---

## 實際範例

### 範例 1：帶上下文的程式碼審查

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI 現在有完整的檔案內容，可以提供具體的反饋：
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# 現在審查 book_app.py，但仍然知道 books.py 的上下文
```

### 範例 2：理解程式碼庫

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI 讀取 books.py 並理解 BookCollection 類別

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI 掃描目錄並摘要

> How does the app save and load books?

# Copilot CLI 可以追蹤它已看過的程式碼
```

<details>
<summary>🎬 看多輪對話如何運作！</summary>

![Multi-Turn Demo](images/multi-turn-demo.gif)

*示範輸出會有所不同。你的模型、工具和回應將與此處顯示的不同。*

</details>

### 範例 3：多檔案重構

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI 看到兩個檔案，可以建議如何合併重複的程式碼
```

---

## 工作階段管理

工作階段在你工作時自動儲存。你可以恢復之前的工作階段，從離開的地方繼續。

### 工作階段自動儲存

每次對話都會自動儲存。只需正常退出：

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... 做一些工作 ...]

> /exit
```

### 恢復最近的工作階段

```bash
# 從離開的地方繼續
copilot --continue
```

### 恢復特定工作階段

```bash
# 從工作階段列表中互動選擇
copilot --resume

# 或透過 ID 恢復特定工作階段
copilot --resume abc123
```

> 💡 **如何找到工作階段 ID？** 你不需要記住它們。不帶 ID 執行 `copilot --resume` 會顯示你之前工作階段的互動列表，包含其名稱、ID 和最後活躍時間。只需選擇你想要的那個即可。
>
> **多個終端機怎麼辦？** 每個終端機視窗都是有自己上下文的獨立工作階段。如果你在三個終端機中開啟了 Copilot CLI，那就是三個獨立的工作階段。從任何終端機執行 `--resume` 都可以瀏覽所有工作階段。`--continue` 旗標會抓取最近關閉的工作階段，無論它在哪個終端機中。
>
> **可以不重新啟動就切換工作階段嗎？** 可以。在活躍的工作階段中使用 `/resume` 斜線指令：
> ```
> > /resume
> # 顯示可切換的工作階段列表
> ```

### 整理你的工作階段

給工作階段有意義的名稱，以便日後找到它們：

```bash
copilot

> /rename book-app-review
# 工作階段已重新命名，方便識別
```

### 檢查和管理上下文

當你新增檔案和對話時，Copilot CLI 的[上下文視窗](../GLOSSARY-zh_tw.md#context-window)會逐漸填滿。有幾個指令可以幫助你保持控制：

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 放棄目前工作階段（不儲存歷史記錄）並開始新的對話

> /new
# 結束目前工作階段（儲存到歷史記錄以供搜尋/恢復）並開始新的對話

> /rewind
# 開啟時間軸選擇器，讓你回滾到對話中的早期時間點
```

> 💡 **何時使用 `/clear` 或 `/new`**：如果你一直在審查 books.py 並想切換到討論 utils.py，先執行 /new（或如果你不需要工作階段歷史記錄則使用 /clear）。否則，舊主題的過時上下文可能會混淆新主題的回應。

> 💡 **犯了錯誤或想嘗試不同的方法？** 使用 `/rewind`（或按兩次 Esc）開啟**時間軸選擇器**，讓你回滾到對話中的任何早期時間點，而不僅僅是最近的一個。當你走錯了方向並想退回而不是完全重新開始時，這很有用。

---

### 從離開的地方繼續

<img src="images/session-persistence-timeline.png" alt="Timeline showing how GitHub Copilot CLI sessions persist across days - start on Monday, resume on Wednesday with full context restored" width="800"/>

*工作階段在你退出時自動儲存。幾天後恢復，所有上下文都已恢復：檔案、問題和進度全都被記住。*

想像這個跨越多天的工作流程：

```bash
# 星期一：開始 book app 審查
copilot

> /rename book-app-review
> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# 處理修正...

> /exit
```

```bash
# 星期三：從離開的地方精確恢復
copilot --continue

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**讓這個強大的原因**：幾天後，Copilot CLI 還記得：
- 你正在處理的確切檔案
- 編號的問題列表
- 你已經解決的哪些問題
- 你對話的上下文

無需重新解釋。無需重新讀取檔案。只需繼續工作。

---

**🎉 你現在掌握了基礎！** `@` 語法、工作階段管理（`--continue`/`--resume`/`/rename`）和上下文指令（`/context`/`/clear`）足以讓你高效工作。以下的所有內容都是選擇性的。準備好後再回來看。

---

# 選擇性：深入探索

<img src="images/optional-going-deeper.png" alt="Abstract crystal cave in blue and purple tones representing deeper exploration of context concepts" width="800"/>

這些主題建立在上面的基礎之上。**選擇你感興趣的，或直接跳到[練習](#practice)。**

| 我想了解... | 跳至 |
|---|---|
| 萬用字元模式和進階工作階段指令 | [其他 @ 模式和工作階段指令](#additional-patterns) |
| 在多個提示中建立上下文 | [上下文感知對話](#context-aware-conversations) |
| Token 限制和 `/compact` | [理解上下文視窗](#understanding-context-windows) |
| 如何選擇要引用的正確檔案 | [選擇引用內容](#choosing-what-to-reference) |
| 分析截圖和設計稿 | [使用圖片](#working-with-images) |

<details>
<summary><strong>其他 @ 模式和工作階段指令</strong></summary>
<a id="additional-patterns"></a>

### 其他 @ 模式

對於進階使用者，Copilot CLI 支援萬用字元模式和圖片引用：

| 模式 | 功能 |
|------|------|
| `@folder/*.py` | 資料夾中的所有 .py 檔案 |
| `@**/test_*.py` | 遞迴萬用字元：在任何地方尋找所有測試檔案 |
| `@image.png` | 用於 UI 審查的圖片檔案 |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### 查看工作階段資訊

```bash
copilot

> /session
# 顯示目前工作階段詳情和工作區摘要

> /usage
# 顯示工作階段指標和統計資料
```

### 分享你的工作階段

```bash
copilot

> /share file ./my-session.md
# 將工作階段匯出為 markdown 檔案

> /share gist
# 建立含有工作階段的 GitHub gist

> /share html
# 將工作階段匯出為獨立的互動式 HTML 檔案
# 適合與隊友分享精美的工作階段報告或儲存以供參考
```

</details>

<details>
<summary><strong>上下文感知對話</strong></summary>
<a id="context-aware-conversations"></a>

### 上下文感知對話

魔法發生在你進行相互建立的多輪對話時。

#### 範例：逐步改善

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[顯示帶有型別提示的版本]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[新增驗證和適當的例外處理]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[生成完整的測試]
```

注意每個提示是如何建立在之前工作的基礎上的。這就是上下文的力量。

</details>

<details>
<summary><strong>理解上下文視窗</strong></summary>
<a id="understanding-context-windows"></a>

### 理解上下文視窗

你已經從基礎部分了解了 `/context` 和 `/clear`。以下是上下文視窗如何運作的更深入說明。

每個 AI 都有一個「上下文視窗」，這是它一次能考慮的文字量。

<img src="images/context-window-visualization.png" alt="Context Window Visualization" width="800"/>

*上下文視窗就像一張桌子：一次只能放這麼多東西。檔案、對話歷史和系統提示都佔用空間。*

#### 達到限制時會發生什麼

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# 隨著你新增更多檔案和對話，這個數字會增長

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 警告：接近上下文限制

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` 指令

當你的上下文快滿但不想失去對話時，`/compact` 會摘要你的歷史記錄以釋放 token：

```bash
copilot

> /compact
# 摘要對話歷史，釋放上下文空間
# 保留你的主要發現和決定
```

#### 上下文效率技巧

| 情況 | 操作 | 原因 |
|------|------|------|
| 開始新主題 | `/clear` | 移除不相關的上下文 |
| 走錯了方向 | `/rewind` | 回滾到任何早期時間點 |
| 長時間對話 | `/compact` | 摘要歷史記錄，釋放 token |
| 需要特定檔案 | 使用 `@file.py` 而非 `@folder/` | 只載入需要的內容 |
| 達到限制 | `/new` 或 `/clear` | 重新開始上下文 |
| 多個主題 | 每個主題使用 `/rename` | 方便恢復正確的工作階段 |

#### 大型程式碼庫的最佳實踐

1. **具體明確**：使用 `@samples/book-app-project/books.py` 而不是 `@samples/book-app-project/`
2. **在主題之間清除上下文**：切換焦點時使用 `/new` 或 `/clear`
3. **使用 `/compact`**：摘要對話以釋放上下文
4. **使用多個工作階段**：每個功能或主題一個工作階段

</details>

<details>
<summary><strong>選擇引用內容</strong></summary>
<a id="choosing-what-to-reference"></a>

### 選擇引用內容

在上下文方面，並非所有檔案都是平等的。以下是如何明智地選擇：

#### 檔案大小考量

| 檔案大小 | 大約 [Token](../GLOSSARY-zh_tw.md#token) 數 | 策略 |
|---------|--------------------------------------|------|
| 小型（< 100 行） | 約 500-1,500 個 token | 可以自由引用 |
| 中型（100-500 行） | 約 1,500-7,500 個 token | 引用特定檔案 |
| 大型（500+ 行） | 7,500+ 個 token | 選擇性引用，使用特定檔案 |
| 非常大型（1000+ 行） | 15,000+ 個 token | 考慮分割或針對特定段落 |

**具體範例：**
- book app 的 4 個 Python 檔案合計 ≈ 2,000-3,000 個 token
- 典型的 Python 模組（200 行） ≈ 3,000 個 token
- Flask API 檔案（400 行） ≈ 6,000 個 token
- 你的 package.json ≈ 200-500 個 token
- 短提示 + 回應 ≈ 500-1,500 個 token

> 💡 **程式碼的快速估算**：將程式碼行數乘以約 15 即可得到大約的 token 數。請記住這只是估算。

#### 包含與排除的內容

**高價值**（包含這些）：
- 進入點（`book_app.py`、`main.py`、`app.py`）
- 你正在詢問的特定檔案
- 目標檔案直接匯入的檔案
- 設定檔（`requirements.txt`、`pyproject.toml`）
- 資料模型或 dataclass

**低價值**（考慮排除）：
- 生成的檔案（編譯輸出、打包資產）
- Node modules 或 vendor 目錄
- 大型資料檔案或 fixture
- 與你的問題無關的檔案

#### 具體程度的光譜

```
較不具體 ────────────────────────► 更具體
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ 掃描所有內容                          └─ 只需要的內容
        （使用更多上下文）                        （保留上下文）
```

**何時廣泛引用**（`@samples/book-app-project/`）：
- 初始程式碼庫探索
- 在多個檔案中尋找模式
- 架構審查

**何時具體引用**（`@samples/book-app-project/books.py`）：
- 調試特定問題
- 特定檔案的程式碼審查
- 詢問單一函式

#### 實際範例：分階段載入上下文

```bash
copilot

# 第一步：從結構開始
> @package.json What frameworks does this project use?

# 第二步：根據答案縮小範圍
> @samples/book-app-project/ Show me the project structure

# 第三步：聚焦在重要的內容
> @samples/book-app-project/books.py Review the BookCollection class

# 第四步：只在需要時新增相關檔案
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

這種分階段方法保持上下文的聚焦和效率。

</details>

<details>
<summary><strong>使用圖片</strong></summary>
<a id="working-with-images"></a>

### 使用圖片

你可以使用 `@` 語法在對話中包含圖片，或直接**從剪貼板貼上**（Cmd+V / Ctrl+V）。Copilot CLI 可以分析截圖、設計稿和圖表，以協助進行 UI 調試、設計實作和錯誤分析。

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **了解更多**：請參閱[其他上下文功能](../appendices/additional-context.md#working-with-images)了解支援的格式、實際使用案例和結合圖片與程式碼的技巧。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

是時候運用你的上下文和工作階段管理技能了。

---

## ▶️ 自己試試看

### 完整專案審查

課程包含你可以直接審查的範例檔案。啟動 copilot 並執行下面顯示的提示：

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI 將識別以下問題：
# - 重複的顯示函式
# - 缺少輸入驗證
# - 不一致的錯誤處理
```

> 💡 **想用你自己的檔案試試？** 建立一個小 Python 專案（`mkdir -p my-project/src`），新增一些 .py 檔案，然後使用 `@my-project/src/` 審查它們。如果你想要，可以請 copilot 為你建立範例程式碼！

### 工作階段工作流程

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI 建議驗證方法]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 之後 - 從離開的地方恢復
copilot --continue

> Generate tests for the changes we made
```

---

完成示範後，試試這些變體：

1. **跨檔案挑戰**：分析 book_app.py 和 books.py 如何協同工作：
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **工作階段挑戰**：開始一個工作階段，用 `/rename my-first-session` 命名它，做一些事情，用 `/exit` 退出，然後執行 `copilot --continue`。它還記得你在做什麼嗎？

3. **上下文挑戰**：在工作階段中間執行 `/context`。你使用了多少 token？試試 `/compact` 然後再次檢查。（參閱深入探索中的[理解上下文視窗](#understanding-context-windows)了解更多關於 `/compact` 的資訊。）

**自我檢查**：當你能解釋為什麼 `@folder/` 比逐個開啟每個檔案更強大時，你就理解了上下文。

---

## 📝 作業

### 主要挑戰：追蹤資料流

實際操作範例專注於程式碼品質審查和輸入驗證。現在在不同的任務上練習相同的上下文技能，追蹤資料如何在 app 中流動：

1. 開始互動式工作階段：`copilot`
2. 同時引用 `books.py` 和 `book_app.py`：
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. 引入資料檔案以獲取額外上下文：
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. 要求跨檔案改善：
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. 重新命名工作階段：`/rename data-flow-analysis`
6. 用 `/exit` 退出，然後用 `copilot --continue` 恢復，並詢問關於資料流的後續問題

**成功標準**：你可以跨多個檔案追蹤資料、恢復命名的工作階段，並獲得跨檔案的建議。

<details>
<summary>💡 提示（點擊展開）</summary>

**開始：**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

然後用以下指令恢復：`copilot --continue`

**實用指令：**
- `@file.py` - 引用單一檔案
- `@folder/` - 引用資料夾中的所有檔案（注意結尾的 `/`）
- `/context` - 檢查你使用了多少上下文
- `/rename <name>` - 為你的工作階段命名以方便恢復

</details>

### 額外挑戰：上下文限制

1. 用 `@samples/book-app-project/` 一次引用所有 book app 檔案
2. 詢問關於不同檔案的幾個詳細問題（`books.py`、`utils.py`、`book_app.py`、`data.json`）
3. 執行 `/context` 查看使用量。它填滿的速度有多快？
4. 練習使用 `/compact` 回收空間，然後繼續對話
5. 嘗試更具體的檔案引用（例如 `@samples/book-app-project/books.py` 而不是整個資料夾），看看它如何影響上下文使用量

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 會發生什麼 | 修正方法 |
|------|------------|----------|
| 在檔案名稱前忘記 `@` | Copilot CLI 將「books.py」視為純文字 | 使用 `@samples/book-app-project/books.py` 引用檔案 |
| 期望工作階段自動持久存在 | 重新啟動 `copilot` 會丟失所有之前的上下文 | 使用 `--continue`（最後一個工作階段）或 `--resume`（選擇工作階段） |
| 引用目前目錄以外的檔案 | 「Permission denied」或「File not found」錯誤 | 使用 `/add-dir /path/to/directory` 授予存取權限 |
| 切換主題時不使用 `/clear` | 舊上下文混淆新主題的回應 | 在開始不同任務前執行 `/clear` |

### 疑難排解

**「File not found」錯誤** - 確保你在正確的目錄中：

```bash
pwd  # 檢查目前目錄
ls   # 列出檔案

# 然後啟動 copilot 並使用相對路徑
copilot

> Review @samples/book-app-project/books.py
```

**「Permission denied」** - 將目錄新增到你的允許列表：

```bash
copilot --add-dir /path/to/directory

# 或在工作階段中：
> /add-dir /path/to/directory
```

**上下文填滿太快**：
- 對檔案引用更加具體
- 在不同主題之間使用 `/clear`
- 將工作分散到多個工作階段

</details>

---

# 摘要

## 🔑 重點收穫

1. **`@` 語法**為 Copilot CLI 提供關於檔案、目錄和圖片的上下文
2. **多輪對話**隨著上下文累積而相互建立
3. **工作階段自動儲存**：使用 `--continue` 或 `--resume` 從離開的地方繼續
4. **上下文視窗**有限制：使用 `/clear`、`/compact`、`/context`、`/new` 和 `/rewind` 管理它們
5. **權限旗標**（`--add-dir`、`--allow-all`）控制多目錄存取。明智地使用它們！
6. **圖片引用**（`@screenshot.png`）幫助視覺化調試 UI 問題

> 📚 **官方文件**：[使用 Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) 提供關於上下文、工作階段和使用檔案的完整參考。

> 📋 **快速參考**：參閱 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference) 獲取完整的指令和快捷鍵列表。

---

## ➡️ 接下來是什麼

現在你可以給 Copilot CLI 上下文了，讓我們把它用在真實的開發任務上。你剛剛學到的上下文技術（檔案引用、跨檔案分析和工作階段管理）是下一章強大工作流程的基礎。

在 **[Chapter 03: Development Workflows](../03-development-workflows/README-zh_tw.md)** 中，你將學習：

- 程式碼審查工作流程
- 重構模式
- 調試協助
- 測試生成
- Git 整合

---

**[← 返回 Chapter 01](../01-setup-and-first-steps/README-zh_tw.md)** | **[繼續到 Chapter 03 →](../03-development-workflows/README-zh_tw.md)**
