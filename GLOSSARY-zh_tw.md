# Glossary（術語表）

本課程中使用的技術術語快速參考。現在不需要把這些全部記住——有需要時隨時回來查閱即可。

---

## A

### Agent

具備特定領域專業知識的 AI 角色（例如：前端、資安）。以 `.agent.md` 檔案定義，並包含 YAML frontmatter，至少需要有 `description` 欄位。

### API

Application Programming Interface（應用程式介面）。讓程式之間互相溝通的方式。

---

## C

### CI/CD

Continuous Integration/Continuous Deployment（持續整合／持續部署）。自動化的測試與部署流程。

### CLI

Command Line Interface（命令列介面）。以文字方式與軟體互動的工具（就像這個工具！）。

### Context Window

AI 一次能夠處理的文字量。就像一張只能放一定量東西的桌子。當你加入檔案、對話紀錄和系統提示時，這些都會佔用此視窗的空間。

### Context Manager

Python 使用 `with` 陳述式的結構，可自動處理初始化與清理工作（例如開啟和關閉檔案）。範例：`with open("file.txt") as f:` 可確保即使發生錯誤，檔案也會被關閉。

### Conventional Commit

遵循標準化格式的提交訊息：`type(scope): description`。常見的類型包括 `feat`（新功能）、`fix`（修正 bug）、`docs`（文件）、`refactor` 和 `test`。範例：`feat(auth): add password reset flow`。

### Dataclass

Python 的裝飾器（`@dataclass`），可為主要用於儲存資料的類別自動產生 `__init__`、`__repr__` 等方法。在書籍應用程式中，用於定義 `Book` 類別，包含 `title`、`author`、`year`、`read` 等欄位。

---

## F

### Frontmatter

位於 Markdown 檔案頂端、以 `---` 分隔符包圍的中繼資料。用於 agent 和 skill 檔案中，以 YAML 格式定義 `description`、`name` 等屬性。

---

## G

### Glob Pattern

使用萬用字元來比對檔案路徑的模式（例如：`*.py` 比對所有 Python 檔案，`*.js` 比對所有 JavaScript 檔案）。

---

## J

### JWT

JSON Web Token。在系統之間安全傳遞身份驗證資訊的方式。

---

## M

### MCP

Model Context Protocol。將 AI 助理連接至外部資料來源的標準協定。

---

## N

### npx

Node.js 的工具，可在不全域安裝套件的情況下直接執行 npm 套件。用於 MCP 伺服器設定中啟動伺服器（例如：`npx @modelcontextprotocol/server-filesystem`）。

---

## O

### OWASP

Open Web Application Security Project（開放網路應用程式安全計畫）。一個發布資安最佳實踐的組織，並維護「OWASP Top 10」列表，涵蓋最關鍵的網頁應用程式安全風險。

---

## P

### PEP 8

Python Enhancement Proposal 8。Python 程式碼的官方風格指南，涵蓋命名慣例（函式使用 snake_case、類別使用 PascalCase）、縮排（4 個空格）及程式碼排版。遵循 PEP 8 可讓 Python 程式碼保持一致性與可讀性。

### Pre-commit Hook

在每次 `git commit` 之前自動執行的腳本。可用於在程式碼提交前執行 Copilot 資安審查或程式碼品質檢查。

### pytest

廣受歡迎的 Python 測試框架，以其簡單的語法、強大的 fixtures 和豐富的外掛生態系著稱。本課程全程使用 pytest 測試書籍應用程式。執行方式：`python -m pytest tests/`。

### Programmatic Mode

使用 `-p` 旗標執行 Copilot，以單一指令方式執行而不需互動介面。

---

## R

### Rate Limiting

在特定時間內對 API 請求次數的限制。若超過方案的使用配額，Copilot 可能會暫時限制回應。

---

## S

### Session

與 Copilot 的對話，能保留上下文並可於稍後繼續。

### Skill

包含指令的資料夾，當內容與你的提示相關時，Copilot 會自動載入。以 `SKILL.md` 檔案定義，並包含 YAML frontmatter。

### Slash Command

以 `/` 開頭、用於控制 Copilot 的指令（例如：`/help`、`/clear`、`/model`）。

---

## T

### Token

AI 模型處理的文字單位。大約等於 4 個字元或 0.75 個英文單字。用於衡量輸入（你的提示與上下文）和輸出（AI 的回應）。

### Type Hints

Python 的標注語法，用於表明函式參數和回傳值的預期型別（例如：`def add_book(title: str, year: int) -> Book:`）。雖然不在執行時強制型別，但有助於提升程式碼可讀性、IDE 支援，以及使用 mypy 等靜態分析工具。

---

## W

### WCAG

Web Content Accessibility Guidelines（網頁內容無障礙指引）。W3C 發布的標準，用於使網頁內容對身心障礙人士更易於使用。WCAG 2.1 AA 是常見的合規目標。

---

## Y

### YAML

YAML Ain't Markup Language。一種人類可讀的資料格式，用於設定檔。在本課程中，YAML 出現在 agent 和 skill 的 frontmatter（即 `.agent.md` 和 `SKILL.md` 檔案頂端以 `---` 分隔的區塊）中。
