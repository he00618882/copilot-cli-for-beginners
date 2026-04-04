![Chapter 01: First Steps](images/chapter-header.png)

> **看 AI 即時找出程式錯誤、解釋令人困惑的程式碼，並產生可執行的腳本。接著學習三種使用 GitHub Copilot CLI 的方式。**

本章是魔法開始的地方！你將親身體驗為什麼開發者形容 GitHub Copilot CLI 就像「隨時待命的資深工程師」。你將看到 AI 在幾秒內找出安全漏洞、用平易近人的英文解釋複雜程式碼，並即時產生可執行的腳本。接著你將掌握三種互動模式（Interactive、Plan 和 Programmatic），讓你知道面對任何任務時該選用哪一種。

> ⚠️ **前置條件**：請確認你已完成 **[Chapter 00: Quick Start](../00-quick-start/README-zh_tw.md)**。在執行下列示範前，你必須先安裝並通過認證 GitHub Copilot CLI。

## 🎯 學習目標

完成本章後，你將能夠：

- 透過實作示範體驗 GitHub Copilot CLI 帶來的生產力提升
- 針對任何任務選擇正確的模式（Interactive、Plan 或 Programmatic）
- 使用 slash 指令控制你的工作階段

> ⏱️ **預估時間**：約 45 分鐘（閱讀 15 分鐘 + 實作 30 分鐘）

---

# 你的第一次 Copilot CLI 體驗

<img src="images/first-copilot-experience.png" alt="Developer sitting at a desk with code on the monitor and glowing particles representing AI assistance" width="800"/>

直接動手看看 Copilot CLI 能做什麼。

---

## 熟悉操作：你的第一批提示詞

在深入精彩示範之前，先從一些現在就可以嘗試的簡單提示詞開始。**不需要任何程式碼儲存庫**！只需開啟終端機並啟動 Copilot CLI：

```bash
copilot
```

試試這些適合初學者的提示詞：

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

不使用 Python 嗎？沒問題！直接用你選擇的語言提問就好。

注意感受它有多自然。就像跟同事聊天一樣提問。探索完畢後，輸入 `/exit` 離開工作階段。

**關鍵洞察**：GitHub Copilot CLI 是對話式的。你不需要特殊語法來入門。直接用平易近人的英文提問即可。

## 看它實際運作

現在讓我們看看為什麼開發者稱之為「隨時待命的資深工程師」。

> 📖 **閱讀範例說明**：以 `>` 開頭的行是你在互動式 Copilot CLI 工作階段內輸入的提示詞。沒有 `>` 前綴的行是你在終端機中執行的 shell 指令。

> 💡 **關於範例輸出**：本課程中所示的範例輸出僅供說明。由於 Copilot CLI 每次的回應都不同，你的結果在措辭、格式和細節上都會有所差異。請專注於回傳的*資訊類型*，而非確切的文字內容。

### 示範 1：幾秒內完成程式碼審查

本課程包含有意設置程式碼品質問題的範例檔案。如果你在本機環境工作，且尚未 clone 此儲存庫，請先執行下方的 `git clone` 指令，切換到 `copilot-cli-for-beginners` 資料夾，再執行 `copilot` 指令。

```bash
# 如果你在本機工作且尚未 clone，請先 clone 課程儲存庫
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# 啟動 Copilot
copilot
```

進入互動式 Copilot CLI 工作階段後，執行以下指令：

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 符號有什麼用途？** `@` 符號告訴 Copilot CLI 讀取一個檔案。你將在 Chapter 02 學到所有相關知識。現在只需照樣複製指令即可。

---

<details>
<summary>🎬 看它實際運作！</summary>

![Code Review Demo](images/code-review-demo.gif)

*示範輸出因情況而異。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

**重點收穫**：幾秒內完成專業程式碼審查。人工審查需要的時間……嗯……比這多得多！

---

### 示範 2：解釋令人困惑的程式碼

曾經盯著程式碼卻不知道它在做什麼嗎？在你的 Copilot CLI 工作階段中試試這個：

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 看它實際運作！</summary>

![Explain Code Demo](images/explain-code-demo.gif)

*示範輸出因情況而異。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

**發生了什麼**：（你的輸出會有所不同）Copilot CLI 讀取檔案，理解程式碼，並用平易近人的英文加以解釋。

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**重點收穫**：複雜的程式碼以耐心導師的方式加以解釋。

---

### 示範 3：產生可執行的程式碼

需要一個原本要花 15 分鐘搜尋的函式嗎？繼續在同一個工作階段中：

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 看它實際運作！</summary>

![Generate Code Demo](images/generate-code-demo.gif)

*示範輸出因情況而異。你的模型、工具和回應將與此處顯示的不同。*

</details>

---

**發生了什麼**：幾秒內產生一個完整、可執行的函式，讓你直接複製貼上執行。

探索完畢後，退出工作階段：

```
> /exit
```

**重點收穫**：即時獲得成果，而且全程都在同一個連續工作階段中。

---

# 模式與指令

<img src="images/modes-and-commands.png" alt="Futuristic control panel with glowing screens, dials, and equalizers representing Copilot CLI modes and commands" width="800"/>

你剛剛看到了 Copilot CLI 能做什麼。現在讓我們了解*如何*有效地使用這些功能。關鍵在於知道面對不同情況應使用三種互動模式中的哪一種。

> 💡 **注意**：Copilot CLI 還有一個 **Autopilot** 模式，可以在不等待你輸入的情況下完成任務。它功能強大，但需要授予完整權限，並且會自動使用付費請求。本課程專注於以下三種模式。當你熟悉基礎知識後，我們會引導你了解 Autopilot。

---

## 🧩 真實世界類比：外出用餐

把使用 GitHub Copilot CLI 想像成外出用餐。從規劃行程到點餐，不同情況需要不同的方式：

| 模式 | 用餐類比 | 使用時機 |
|------|---------|---------|
| **Plan** | 去餐廳的 GPS 路線 | 複雜任務——規劃路線、確認停靠點、同意計畫後再出發 |
| **Interactive** | 與服務生對話 | 探索與迭代——提問、客製化、即時獲得反饋 |
| **Programmatic** | 得來速點餐 | 快速、明確的任務——待在你的環境中，快速獲得結果 |

就像外出用餐一樣，你會自然地學會什麼時候哪種方式最合適。

<img src="images/ordering-food-analogy.png" alt="Three Ways to Use GitHub Copilot CLI - Plan Mode (GPS route to restaurant), Interactive Mode (talking to waiter), Programmatic Mode (drive-through)" width="800"/>

*根據任務選擇模式：Plan 用於先規劃、Interactive 用於來回協作、Programmatic 用於快速一次性結果*

### 我應該從哪個模式開始？

**從 Interactive 模式開始。**
- 你可以實驗並追問後續問題
- 脈絡在對話中自然積累
- 錯誤很容易用 `/clear` 修正

熟悉後，再嘗試：
- **Programmatic 模式**（`copilot -p "<your prompt>"`）用於快速一次性問題
- **Plan 模式**（`/plan`）當你需要在撰寫程式碼前更詳細地規劃時

---

## 三種模式

### 模式 1：Interactive 模式（從這裡開始）

<img src="images/interactive-mode.png" alt="Interactive Mode - Like talking to a waiter who can answer questions and adjust the order" width="250"/>

**最適合**：探索、迭代、多輪對話。就像與能回答問題、接受反饋並即時調整訂單的服務生交談。

啟動互動式工作階段：

```bash
copilot
```

如你到目前為止所見，你會看到一個可以自然輸入的提示符號。若要取得可用指令的說明，只需輸入：

```
> /help
```

**關鍵洞察**：Interactive 模式保持脈絡。每則訊息都建立在前一則訊息之上，就像真實對話一樣。

#### Interactive 模式範例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

注意每個提示詞如何建立在前一個答案的基礎上。你在進行對話，而不是每次從頭開始。

---

### 模式 2：Plan 模式

<img src="images/plan-mode.png" alt="Plan Mode - Like planning a route before a trip using GPS" width="250"/>

**最適合**：你想在執行前先審查方式的複雜任務。類似於旅行前使用 GPS 規劃路線。

Plan 模式幫助你在撰寫任何程式碼前建立逐步計畫。使用 `/plan` 指令或按 **Shift+Tab** 切換到 Plan 模式：

> 💡 **提示**：**Shift+Tab** 在模式間切換：Interactive → Plan → Autopilot。在互動式工作階段中隨時按下，即可切換模式而不需輸入指令。

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

**Plan 模式輸出：**（你的輸出可能不同）

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**關鍵洞察**：Plan 模式讓你在撰寫任何程式碼前審查並修改方式。計畫完成後，你甚至可以告訴 Copilot CLI 將其儲存到檔案以供日後參考。例如，「Save this plan to `mark_as_read_plan.md`」會建立一個包含計畫詳情的 markdown 檔案。

> 💡 **想要更複雜的東西？** 試試：`/plan Add search and filter capabilities to the book app`。Plan 模式可以從簡單功能擴展到完整應用程式。

> 📚 **Autopilot 模式**：你可能注意到 Shift+Tab 會循環到第三個模式，稱為 **Autopilot**。在 autopilot 模式中，Copilot 會在不等待你逐步輸入的情況下完成整個計畫——就像把任務交給同事並說「完成後告訴我」。典型的工作流程是 plan → accept → autopilot，這意味著你需要先善於撰寫計畫。先熟悉 Interactive 和 Plan 模式，準備好後再查看[官方文件](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)。

---

### 模式 3：Programmatic 模式

<img src="images/programmatic-mode.png" alt="Programmatic Mode - Like using a drive-through for a quick order" width="250"/>

**最適合**：自動化、腳本、CI/CD、單次指令。就像使用得來速快速點餐，不需要與服務生交談。

使用 `-p` 旗標執行不需要互動的一次性指令：

```bash
# 產生程式碼
copilot -p "Write a function that checks if a number is even or odd"

# 快速取得說明
copilot -p "How do I read a JSON file in Python?"
```

**關鍵洞察**：Programmatic 模式給你一個快速答案然後退出。不需對話，只需輸入 → 輸出。

<details>
<summary>📚 <strong>進一步探索：在腳本中使用 Programmatic 模式</strong>（點擊展開）</summary>

熟悉後，你可以在 shell 腳本中使用 `-p`：

```bash
#!/bin/bash

# 自動產生 commit 訊息
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# 審查一個檔案
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **關於 `--allow-all`**：此旗標跳過所有權限提示，讓 Copilot CLI 在不詢問的情況下讀取檔案、執行指令並存取 URL。這對 programmatic 模式（`-p`）是必要的，因為沒有互動式工作階段可以批准操作。僅在你自己撰寫的提示詞和你信任的目錄中使用 `--allow-all`。切勿在不受信任的輸入或敏感目錄中使用。

</details>

---

## 基本 Slash 指令

這些指令在 interactive 模式中使用。**先從這六個開始**——它們涵蓋了 90% 的日常使用：

| 指令 | 功能 | 使用時機 |
|------|------|---------|
| `/clear` | 清除對話並重新開始 | 切換話題時 |
| `/help` | 顯示所有可用指令 | 忘記指令時 |
| `/model` | 顯示或切換 AI 模型 | 想更換 AI 模型時 |
| `/plan` | 在撰寫程式碼前規劃工作 | 處理較複雜的功能時 |
| `/research` | 使用 GitHub 和網路來源進行深度研究 | 需要在撰寫程式碼前調查某個主題時 |
| `/exit` | 結束工作階段 | 完成後 |

入門就這些！隨著你越來越熟練，可以探索更多指令。

> 📚 **官方文件**：[CLI 指令參考](https://docs.github.com/copilot/reference/cli-command-reference)提供完整的指令和旗標列表。

<details>
<summary>📚 <strong>其他指令</strong>（點擊展開）</summary>

> 💡 上方的基本指令已涵蓋你日常使用的大部分需求。此參考資料供你準備好探索更多時使用。

### Agent 環境

| 指令 | 功能 |
|------|------|
| `/agent` | 瀏覽並從可用的 agent 中選擇 |
| `/init` | 為你的儲存庫初始化 Copilot 指示 |
| `/mcp` | 管理 MCP 伺服器設定 |
| `/skills` | 管理用於增強功能的 skill |

> 💡 Agent 在 [Chapter 04](../04-agents-custom-instructions/README-zh_tw.md) 中介紹，skill 在 [Chapter 05](../05-skills/README-zh_tw.md) 中介紹，MCP 伺服器在 [Chapter 06](../06-mcp-servers/README-zh_tw.md) 中介紹。

### 模型與子 agent

| 指令 | 功能 |
|------|------|
| `/delegate` | 將任務移交給 GitHub Copilot 雲端 agent |
| `/fleet` | 將複雜任務分割成平行子任務以加快完成速度 |
| `/model` | 顯示或切換 AI 模型 |
| `/tasks` | 檢視背景子 agent 和已分離的 shell 工作階段 |

### 程式碼

| 指令 | 功能 |
|------|------|
| `/diff` | 審查當前目錄中的變更 |
| `/pr` | 對當前分支的 pull request 進行操作 |
| `/research` | 使用 GitHub 和網路來源執行深度研究調查 |
| `/review` | 執行程式碼審查 agent 來分析變更 |
| `/terminal-setup` | 啟用多行輸入支援（shift+enter 和 ctrl+enter） |

### 權限

| 指令 | 功能 |
|------|------|
| `/add-dir <directory>` | 將目錄新增到允許清單 |
| `/allow-all [on|off|show]` | 自動批准所有權限提示；使用 `on` 啟用、`off` 停用、`show` 查看當前狀態 |
| `/cwd`, `/cd [directory]` | 檢視或變更工作目錄 |
| `/list-dirs` | 顯示所有允許的目錄 |

> ⚠️ **請謹慎使用**：`/allow-all` 跳過確認提示。對於受信任的專案很方便，但對不受信任的程式碼要小心。

### 工作階段

| 指令 | 功能 |
|------|------|
| `/clear` | 放棄當前工作階段（不儲存歷史記錄）並開始新的對話 |
| `/compact` | 摘要對話以減少脈絡使用量 |
| `/context` | 顯示脈絡視窗的 token 使用量和視覺化 |
| `/new` | 結束當前工作階段（儲存到歷史記錄以供搜尋/恢復）並開始新的對話 |
| `/resume` | 切換到不同的工作階段（可選擇性地指定工作階段 ID） |
| `/rename` | 重新命名當前工作階段（省略名稱則自動產生） |
| `/rewind` | 開啟時間軸選擇器，回滾到對話中任何較早的時間點 |
| `/usage` | 顯示工作階段使用指標和統計資料 |
| `/session` | 顯示工作階段資訊和工作區摘要 |
| `/share` | 將工作階段匯出為 markdown 檔案、GitHub gist 或獨立 HTML 檔案 |

### 說明與回饋

| 指令 | 功能 |
|------|------|
| `/changelog` | 顯示 CLI 版本的更新日誌 |
| `/feedback` | 向 GitHub 提交回饋 |
| `/help` | 顯示所有可用指令 |
| `/theme` | 檢視或設定終端機主題 |

### 快速 Shell 指令

在不透過 AI 的情況下，直接執行 shell 指令，在前面加上 `!`：

```bash
copilot

> !git status
# 直接執行 git status，略過 AI

> !python -m pytest tests/
# 直接執行 pytest
```

### 切換模型

Copilot CLI 支援來自 OpenAI、Anthropic、Google 等的多種 AI 模型。你可用的模型取決於你的訂閱等級和地區。使用 `/model` 查看選項並在它們之間切換：

```bash
copilot
> /model

# 顯示可用模型並讓你選擇一個。選擇 Sonnet 4.5。
```

> 💡 **提示**：某些模型比其他模型消耗更多「付費請求」。標記為 **1x**（如 Claude Sonnet 4.5）的模型是很好的預設選擇。它們功能強大且高效。較高倍數的模型會更快耗用你的付費請求配額，因此請留到真正需要時再使用。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

是時候將你所學付諸實踐了。

---

## ▶️ 親自嘗試

### 互動式探索

啟動 Copilot 並使用後續提示詞來迭代改善 book app：

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 規劃功能

使用 `/plan` 讓 Copilot CLI 在撰寫任何程式碼前規劃實作：

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# 審查計畫
# 批准或修改
# 觀看它逐步實作
```

### 使用 Programmatic 模式自動化

`-p` 旗標讓你直接從終端機執行 Copilot CLI，而無需進入互動模式。從儲存庫根目錄將以下腳本複製貼上到你的終端機（不是在 Copilot 內部），以審查 book app 中的所有 Python 檔案。

```bash
# 審查 book app 中的所有 Python 檔案
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows)：**

```powershell
# 審查 book app 中的所有 Python 檔案
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

完成示範後，試試這些變化：

1. **互動挑戰**：啟動 `copilot` 並探索 book app。詢問 `@samples/book-app-project/books.py` 並連續請求改進 3 次。

2. **Plan 模式挑戰**：執行 `/plan Add rating and review features to the book app`。仔細閱讀計畫。它合理嗎？

3. **Programmatic 挑戰**：執行 `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`。第一次嘗試就成功了嗎？

---

## 📝 作業

### 主要挑戰：改善 Book App 工具程式

實作範例專注於審查和重構 `book_app.py`。現在在另一個檔案 `utils.py` 上練習相同的技能：

1. 啟動互動式工作階段：`copilot`
2. 請 Copilot CLI 摘要檔案：`@samples/book-app-project/utils.py What does each function in this file do?`
3. 請它新增輸入驗證：「Add validation to `get_user_choice()` so it handles empty input and non-numeric entries」
4. 請它改善錯誤處理：「What happens if `get_book_details()` receives an empty string for the title? Add guards for that.」
5. 請求 docstring：「Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values」
6. 觀察脈絡如何在提示詞之間傳遞。每次改善都建立在上一次的基礎上
7. 用 `/exit` 退出

**成功標準**：你應該透過多輪對話，得到一個改善後的 `utils.py`，包含輸入驗證、錯誤處理和 docstring。

<details>
<summary>💡 提示（點擊展開）</summary>

**可嘗試的範例提示詞：**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**常見問題：**
- 如果 Copilot CLI 提出澄清問題，直接自然地回答即可
- 脈絡會向前傳遞，所以每個提示詞都建立在前一個的基礎上
- 如果想重新開始，使用 `/clear`

</details>

### 進階挑戰：比較各種模式

範例中使用 `/plan` 進行搜尋功能，使用 `-p` 進行批次審查。現在在單一新任務上嘗試所有三種模式：將 `list_by_year()` 方法新增到 `BookCollection` 類別：

1. **Interactive**：`copilot` → 請它逐步設計並建立方法
2. **Plan**：`/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**：`copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**反思**：哪種模式感覺最自然？你什麼時候會使用哪種？

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 發生的情況 | 修正方式 |
|------|-----------|---------|
| 輸入 `exit` 而非 `/exit` | Copilot CLI 將「exit」視為提示詞而非指令 | Slash 指令一律以 `/` 開頭 |
| 使用 `-p` 進行多輪對話 | 每次 `-p` 呼叫都是獨立的，沒有之前呼叫的記憶 | 對建立在脈絡上的對話使用互動模式（`copilot`） |
| 忘記用引號包住含有 `$` 或 `!` 的提示詞 | Shell 在 Copilot CLI 看到之前就解譯了特殊字元 | 用引號包住提示詞：`copilot -p "What does $HOME mean?"` |

### 疑難排解

**「Model not available」** - 你的訂閱可能不包含所有模型。使用 `/model` 查看可用的模型。

**「Context too long」** - 你的對話已使用完整脈絡視窗。使用 `/clear` 重置，或開始新工作階段。

**「Rate limit exceeded」** - 等待幾分鐘後再試。考慮使用有延遲的 programmatic 模式進行批次操作。

</details>

---

# 摘要

## 🔑 重點收穫

1. **Interactive 模式**用於探索和迭代——脈絡向前傳遞。就像與記得你說過的話的人對話一樣。
2. **Plan 模式**通常用於較複雜的任務。在實作前先審查。
3. **Programmatic 模式**用於自動化。不需要互動。
4. **基本指令**（`/help`、`/clear`、`/plan`、`/research`、`/model`、`/exit`）涵蓋大部分日常使用。

> 📋 **快速參考**：查看 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference)取得完整的指令和快捷鍵列表。

---

## ➡️ 下一步

現在你已了解三種模式，讓我們學習如何為 Copilot CLI 提供關於程式碼的脈絡。

在 **[Chapter 02: Context and Conversations](../02-context-conversations/README-zh_tw.md)** 中，你將學習：

- 用於參照檔案和目錄的 `@` 語法
- 使用 `--resume` 和 `--continue` 管理工作階段
- 脈絡管理如何讓 Copilot CLI 真正強大

---

**[← 返回課程首頁](../README.md)** | **[繼續到 Chapter 02 →](../02-context-conversations/README-zh_tw.md)**
