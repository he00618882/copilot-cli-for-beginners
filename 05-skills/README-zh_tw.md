![Chapter 05: Skills System](images/chapter-header.png)

> **如果 Copilot 能自動套用你團隊的最佳實踐，而不需要你每次都重新說明，會如何？**

在本章中，你將學習 Agent Skills：當與你的任務相關時，Copilot 會自動載入的指令資料夾。Agents 改變的是 Copilot *如何*思考，而 skills 則教導 Copilot *完成任務的具體方式*。你將建立一個 Copilot 在你詢問安全性問題時自動套用的安全性稽核 skill，建立確保一致程式碼品質的團隊標準審查標準，並學習 skills 如何在 Copilot CLI、VS Code 和 GitHub Copilot cloud agent 之間運作。


## 🎯 學習目標

完成本章後，你將能夠：

- 了解 Agent Skills 的運作方式及使用時機
- 使用 SKILL.md 檔案建立自訂 skills
- 使用來自共享儲存庫的社群 skills
- 知道何時使用 skills vs agents vs MCP

> ⏱️ **預估時間**：約 55 分鐘（20 分鐘閱讀 + 35 分鐘實作）

---

## 🧩 現實世界類比：電動工具

通用電鑽很有用，但專用附件讓它更強大。
<img src="images/power-tools-analogy.png" alt="Power Tools - Skills Extend Copilot's Capabilities" width="800"/>


Skills 的運作方式相同。就像為不同工作更換鑽頭一樣，你可以為不同任務為 Copilot 添加 skills：

| Skill 附件 | 用途 |
|------------|---------|
| `commit` | 產生一致的 commit 訊息 |
| `security-audit` | 檢查 OWASP 漏洞 |
| `generate-tests` | 建立完整的 pytest 測試 |
| `code-checklist` | 套用團隊程式碼品質標準 |



*Skills 是擴展 Copilot 能力的專用附件*

---

# Skills 的運作方式

<img src="images/how-skills-work.png" alt="Glowing RPG-style skill icons connected by light trails on a starfield background representing Copilot skills" width="800"/>

了解 skills 是什麼、為什麼重要，以及它們與 agents 和 MCP 有何不同。

---

## *第一次接觸 Skills？* 從這裡開始！

1. **查看已有哪些 skills 可用：**
   ```bash
   copilot
   > /skills list
   ```
   這會顯示 Copilot 在你的專案和個人資料夾中能找到的所有 skills。

2. **查看一個真實的 skill 檔案：** 查看我們提供的 [code-checklist SKILL.md](../.github/skills/code-checklist/SKILL.md) 來了解模式。它只是 YAML frontmatter 加上 markdown 指令。

3. **理解核心概念：** Skills 是任務特定的指令，當你的提示詞符合 skill 的描述時，Copilot 會*自動*載入它們。你不需要啟動它們，只要自然地提問即可。


## 了解 Skills

Agent Skills 是包含指令、腳本和資源的資料夾，當**與你的任務相關時 Copilot 會自動載入**。Copilot 讀取你的提示詞，檢查是否有任何 skills 符合，並自動套用相關指令。

```bash
copilot

> Check books.py against our quality checklist
# 中文 Prompt：根據我們的 quality checklist 檢查 books.py
# Copilot detects this matches your "code-checklist" skill
# and automatically applies its Python quality checklist

> Generate tests for the BookCollection class
# 中文 Prompt：為 BookCollection class 產生 tests
# Copilot loads your "pytest-gen" skill
# and applies your preferred test structure

> What are the code quality issues in this file?
# 中文 Prompt：這個檔案有哪些 code quality 問題？
# Copilot loads your "code-checklist" skill
# and checks against your team's standards
```

> 💡 **關鍵洞見**：Skills 是根據你的提示詞與 skill 描述的匹配程度**自動觸發**的。只需自然地提問，Copilot 就會在幕後套用相關 skills。你也可以直接呼叫 skills，這在接下來會學到。

> 🧰 **即用範本**：查看 [.github/skills](../.github/skills/) 資料夾，其中有可以直接複製使用的簡易 skills。

### 直接使用斜線指令呼叫

雖然自動觸發是 skills 運作的主要方式，但你也可以使用 skill 名稱作為斜線指令**直接呼叫 skills**：

```bash
> /generate-tests Create tests for the user authentication module
# 中文 Prompt：/generate-tests 為使用者認證模組建立 test

> /code-checklist Check books.py for code quality issues
# 中文 Prompt：/code-checklist 檢查 books.py 的 code quality 問題

> /security-audit Check the API endpoints for vulnerabilities
# 中文 Prompt：/security-audit 檢查 API endpoints 的 security vulnerabilities
```

當你想確保使用特定 skill 時，這讓你擁有明確的控制權。

> 📝 **Skills vs Agents 呼叫方式**：不要混淆 skill 呼叫和 agent 呼叫：
> - **Skills**：`/skill-name <prompt>`，例如 `/code-checklist Check this file`
> - **Agents**：`/agent`（從清單選擇）或 `copilot --agent <name>`（命令列）
>
> 如果你同時有名稱相同的 skill 和 agent（例如 "code-reviewer"），輸入 `/code-reviewer` 會呼叫 **skill**，而非 agent。

### 我如何知道 Skill 被使用了？

你可以直接問 Copilot：

```bash
> What skills did you use for that response?
# 中文 Prompt：你在那次回應中使用了哪些 skills？

> What skills do you have available for security reviews?
# 中文 Prompt：你有哪些可用於 security reviews 的 skills？
```

### Skills vs Agents vs MCP

Skills 只是 GitHub Copilot 擴充性模型的其中一部分。以下是它們與 agents 和 MCP 伺服器的比較。

> *暫時不用擔心 MCP。我們將在[第 06 章](../06-mcp-servers/README-zh_tw.md)中介紹它。這裡列出是讓你看到 skills 在整體架構中的位置。*

<img src="images/skills-agents-mcp-comparison.png" alt="Comparison diagram showing the differences between Agents, Skills, and MCP Servers and how they combine into your workflow" width="800"/>

| 功能 | 做什麼 | 何時使用 |
|---------|--------------|-------------|
| **Agents** | 改變 AI 的思考方式 | 需要跨多個任務的專業知識 |
| **Skills** | 提供任務特定的指令 | 有詳細步驟的特定、可重複任務 |
| **MCP** | 連接外部服務 | 需要來自 API 的即時資料 |

使用 agents 處理廣泛的專業知識，skills 處理特定任務指令，MCP 處理外部資料。Agent 在對話中可以使用一個或多個 skills。例如，當你要求 agent 檢查你的程式碼時，它可能會自動套用 `security-audit` skill 和 `code-checklist` skill。

> 📚 **深入了解**：請參閱官方 [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) 文件，取得 skill 格式和最佳實踐的完整參考。

---

## 從手動提示詞到自動專業知識

在深入了解如何建立 skills 之前，讓我們先看看*為什麼*它們值得學習。一旦你看到一致性的提升，「如何做」就會更有意義。

### 使用 Skills 之前：不一致的審查

每次程式碼審查，你可能都會忘記一些事情：

```bash
copilot

> Review this code for issues
# 中文 Prompt：Review 這段程式碼的問題
# Generic review - might miss your team's specific concerns
```

或者你每次都要輸入很長的提示詞：

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
# 中文 Prompt：Review 這段程式碼，檢查 bare except clauses、缺少 type hints、mutable default arguments、file I/O 缺少 context managers、超過 50 行的函式、production code 中的 print 陳述句…
```

時間：**30+ 秒**輸入。一致性：**因記憶力而有所不同**。

### 使用 Skills 之後：自動最佳實踐

安裝 `code-checklist` skill 後，只需自然地提問：

```bash
copilot

> Check the book collection code for quality issues
# 中文 Prompt：檢查書籍集合程式碼的 quality 問題
```

**幕後發生的事情**：
1. Copilot 在你的提示詞中看到「code quality」和「issues」
2. 檢查 skill 描述，發現你的 `code-checklist` skill 符合
3. 自動載入你團隊的品質檢查清單
4. 無需你列出即可套用所有檢查

<img src="images/skill-auto-discovery-flow.png" alt="How Skills Auto-Trigger - 4-step flow showing how Copilot automatically matches your prompt to the right skill" width="800"/>

*只需自然地提問。Copilot 會將你的提示詞匹配到正確的 skill 並自動套用。*

**輸出**：
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**差異所在**：你的團隊標準每次都會自動套用，無需手動輸入。

---

<details>
<summary>🎬 觀看實際示範！</summary>

![Skill Trigger Demo](images/skill-trigger-demo.gif)

*示範輸出可能有所不同。你的模型、工具和回應與此處顯示的可能不同。*

</details>

---

## 規模化的一致性：團隊 PR 審查 Skill

想像你的團隊有一個 10 點 PR 檢查清單。沒有 skill 的話，每位開發人員都必須記住全部 10 點，而且總會有人忘記其中一點。有了 `pr-review` skill，整個團隊都能獲得一致的審查：

```bash
copilot

> Can you review this PR?
# 中文 Prompt：你可以 review 這個 PR 嗎？
```

Copilot 自動載入你團隊的 `pr-review` skill 並檢查所有 10 個項目：

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**強大之處**：每位團隊成員都自動套用相同的標準。新進員工不需要記住檢查清單，因為 skill 會處理這一切。

---

# 建立自訂 Skills

<img src="images/creating-managing-skills.png" alt="Human and robotic hands building a wall of glowing LEGO-like blocks representing skill creation and management" width="800"/>

從 SKILL.md 檔案建立你自己的 skills。

---

## Skill 存放位置

Skills 儲存在 `.github/skills/`（專案特定）或 `~/.copilot/skills/`（使用者層級）。

### Copilot 如何尋找 Skills

Copilot 會自動掃描以下位置以尋找 skills：

| 位置 | 範圍 |
|----------|-------|
| `.github/skills/` | 專案特定（透過 git 與團隊共用） |
| `~/.copilot/skills/` | 使用者特定（你的個人 skills） |

### Skill 結構

每個 skill 存放在自己的資料夾中，並有一個 `SKILL.md` 檔案。你可以選擇性地包含腳本、範例或其他資源：

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Required: Skill definition and instructions
    ├── examples/          # Optional: Example files Copilot can reference
    │   └── sample.py
    └── scripts/           # Optional: Scripts the skill can use
        └── validate.sh
```

> 💡 **提示**：目錄名稱應與 SKILL.md frontmatter 中的 `name` 一致（小寫加連字號）。

### SKILL.md 格式

Skills 使用帶有 YAML frontmatter 的簡易 markdown 格式：

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML 屬性：**

| 屬性 | 必要 | 說明 |
|----------|----------|-------------|
| `name` | **是** | 唯一識別碼（小寫，空格用連字號） |
| `description` | **是** | Skill 的功能及 Copilot 應在何時使用它 |
| `license` | 否 | 適用於此 skill 的授權條款 |

> 📖 **官方文件**：[About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### 建立你的第一個 Skill

讓我們建立一個檢查 OWASP Top 10 漏洞的安全性稽核 skill：

```bash
# Create skill directory
mkdir -p .github/skills/security-audit

# Create the SKILL.md file
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Test your skill (skills load automatically based on your prompt)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# 中文 Prompt：@samples/book-app-project/ 檢查這段程式碼的 security vulnerabilities
# Copilot detects "security vulnerabilities" matches your skill
# and automatically applies its OWASP checklist
```

**預期輸出**（你的結果可能有所不同）：

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## 撰寫好的 Skill 描述

SKILL.md 中的 `description` 欄位至關重要！這是 Copilot 決定是否載入你的 skill 的依據：

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **提示**：包含符合你自然提問方式的關鍵字。如果你說「security review」，就在描述中包含「security review」。

### 將 Skills 與 Agents 結合

Skills 和 agents 可以協同運作。Agent 提供專業知識，skill 提供具體指令：

```bash
# Start with a code-reviewer agent
copilot --agent code-reviewer

> Check the book app for quality issues
# 中文 Prompt：檢查書籍應用程式的 quality 問題
# code-reviewer agent's expertise combines
# with your code-checklist skill's checklist
```

---

# 管理與分享 Skills

探索已安裝的 skills、尋找社群 skills，以及分享你自己的 skills。

<img src="images/managing-sharing-skills.png" alt="Managing and Sharing Skills - showing the discover, use, create, and share cycle for CLI skills" width="800" />

---

## 使用 `/skills` 指令管理 Skills

使用 `/skills` 指令管理你已安裝的 skills：

| 指令 | 功能 |
|---------|--------------|
| `/skills list` | 顯示所有已安裝的 skills |
| `/skills info <name>` | 取得特定 skill 的詳細資訊 |
| `/skills add <name>` | 啟用一個 skill（從儲存庫或市集） |
| `/skills remove <name>` | 停用或解除安裝一個 skill |
| `/skills reload` | 編輯 SKILL.md 檔案後重新載入 skills |

> 💡 **記住**：你不需要為每個提示詞「啟動」skills。一旦安裝，當你的提示詞符合 skills 的描述時，它們就會**自動觸發**。這些指令用於管理哪些 skills 可用，而非用於使用它們。

### 範例：查看你的 Skills

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>觀看實際示範！</summary>

![List Skills Demo](images/list-skills-demo.gif)

*示範輸出可能有所不同。你的模型、工具和回應與此處顯示的可能不同。*

</details>

---

### 何時使用 `/skills reload`

建立或編輯 skill 的 SKILL.md 檔案後，執行 `/skills reload` 來套用變更，無需重新啟動 Copilot：

```bash
# Edit your skill file
# Then in Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **須知**：使用 `/compact` 壓縮對話記錄後，skills 仍然有效。壓縮後無需重新載入。

---

## 尋找與使用社群 Skills

### 使用 Plugins 安裝 Skills

> 💡 **什麼是 plugins？** Plugins 是可安裝的套件，能將 skills、agents 和 MCP 伺服器設定打包在一起。把它們想成 Copilot CLI 的「應用程式商店」擴充功能。

`/plugin` 指令讓你可以瀏覽和安裝這些套件：

```bash
copilot

> /plugin list
# Shows installed plugins

> /plugin marketplace
# Browse available plugins

> /plugin install <plugin-name>
# Install a plugin from the marketplace
```

Plugins 可以將多種功能打包在一起——一個 plugin 可能包含協同運作的相關 skills、agents 和 MCP 伺服器設定。

### 社群 Skill 儲存庫

預製 skills 也可從社群儲存庫取得：

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - 官方 GitHub Copilot 資源，包含 skills 文件和範例

### 手動安裝社群 Skill

如果你在 GitHub 儲存庫中找到了一個 skill，可以將其資料夾複製到你的 skills 目錄：

```bash
# Clone the awesome-copilot repository
git clone https://github.com/github/awesome-copilot.git /tmp/awesome-copilot

# Copy a specific skill to your project
cp -r /tmp/awesome-copilot/skills/code-checklist .github/skills/

# Or for personal use across all projects
cp -r /tmp/awesome-copilot/skills/code-checklist ~/.copilot/skills/
```

> ⚠️ **安裝前先審查**：在將 skill 的 `SKILL.md` 複製到你的專案之前，務必先閱讀它。Skills 控制 Copilot 的行為，惡意的 skill 可能會指示它執行有害指令或以意外方式修改程式碼。

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

透過建立和測試你自己的 skills 來應用所學。

---

## ▶️ 自己動手試試

### 建立更多 Skills

以下是兩個展示不同模式的 skills。按照上方「建立你的第一個 Skill」中相同的 `mkdir` + `cat` 工作流程進行，或將 skills 複製貼上到適當位置。更多範例可在 [.github/skills](../.github/skills) 中找到。

### pytest 測試產生 Skill

確保整個程式碼庫中 pytest 結構一致的 skill：

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### 團隊 PR 審查 Skill

在整個團隊中強制執行一致 PR 審查標準的 skill：

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### 更進一步

1. **Skill 建立挑戰**：建立一個執行 3 點檢查清單的 `quick-review` skill：
   - Bare except 子句
   - 缺少 type hints
   - 不清晰的變數名稱

   輸入以下提示詞測試它：「Do a quick review of books.py」

2. **Skill 比較**：計時自己手動撰寫詳細安全性審查提示詞所需的時間。然後只說「Check for security issues in this file」，讓你的 security-audit skill 自動載入。Skill 節省了多少時間？

3. **團隊 Skill 挑戰**：思考你團隊的程式碼審查檢查清單。你能將它編碼為 skill 嗎？寫下 skill 應該始終檢查的 3 件事。

**自我檢驗**：當你能解釋為什麼 `description` 欄位很重要（這是 Copilot 決定是否載入你的 skill 的依據）時，你就理解了 skills。

---

## 📝 作業

### 主要挑戰：建立書籍摘要 Skill

上面的範例建立了 `pytest-gen` 和 `pr-review` skills。現在練習建立一種完全不同類型的 skill：用於從資料產生格式化輸出的 skill。

1. 列出你目前的 skills：執行 Copilot 並輸入 `/skills list`。你也可以用 `ls .github/skills/` 查看專案 skills，或 `ls ~/.copilot/skills/` 查看個人 skills。
2. 在 `.github/skills/book-summary/SKILL.md` 建立一個 `book-summary` skill，用於產生書籍集合的格式化 markdown 摘要
3. 你的 skill 應該具備：
   - 清晰的名稱和描述（描述對於匹配至關重要！）
   - 具體的格式規則（例如包含標題、作者、年份、閱讀狀態的 markdown 表格）
   - 輸出慣例（例如用 ✅/❌ 表示閱讀狀態，按年份排序）
4. 測試 skill：`@samples/book-app-project/data.json Summarize the books in this collection`
5. 透過 `/skills list` 確認 skill 自動觸發
6. 嘗試用 `/book-summary Summarize the books in this collection` 直接呼叫它

**成功標準**：你有一個可運作的 `book-summary` skill，當你詢問書籍集合時 Copilot 會自動套用它。

<details>
<summary>💡 提示（點擊展開）</summary>

**起始範本**：建立 `.github/skills/book-summary/SKILL.md`：

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**測試它：**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# 中文 Prompt：@samples/book-app-project/data.json 摘要這個集合中的書籍
# The skill should auto-trigger based on the description match
```

**如果未觸發：** 嘗試 `/skills reload` 然後再次提問。

</details>

### 加分挑戰：Commit 訊息 Skill

1. 建立一個 `commit-message` skill，以一致的格式產生 conventional commit 訊息
2. 透過暫存一個變更並詢問「Generate a commit message for my staged changes」來測試它
3. 記錄你的 skill，並以 `copilot-skill` 主題在 GitHub 上分享它

---

<details>
<summary>🔧 <strong>常見錯誤與疑難排解</strong>（點擊展開）</summary>

### 常見錯誤

| 錯誤 | 發生的情況 | 修正方式 |
|---------|--------------|-----|
| 將檔案命名為 `SKILL.md` 以外的名稱 | Skill 無法被識別 | 檔案必須確切命名為 `SKILL.md` |
| `description` 欄位太模糊 | Skill 永遠不會自動載入 | Description 是主要的發現機制。使用具體的觸發關鍵字 |
| frontmatter 中缺少 `name` 或 `description` | Skill 載入失敗 | 在 YAML frontmatter 中新增這兩個欄位 |
| 資料夾位置錯誤 | 找不到 skill | 使用 `.github/skills/skill-name/`（專案）或 `~/.copilot/skills/skill-name/`（個人） |

### 疑難排解

**Skill 未被使用** - 如果 Copilot 在預期情況下未使用你的 skill：

1. **檢查描述**：它是否符合你的提問方式？
   ```markdown
   # Bad: Too vague
   description: Reviews code

   # Good: Includes trigger words
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **確認檔案位置**：
   ```bash
   # Project skills
   ls .github/skills/

   # User skills
   ls ~/.copilot/skills/
   ```

3. **檢查 SKILL.md 格式**：Frontmatter 是必要的：
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**Skill 未出現** - 確認資料夾結構：
```
.github/skills/
└── my-skill/           # Folder name
    └── SKILL.md        # Must be exactly SKILL.md (case-sensitive)
```

建立或編輯 skills 後執行 `/skills reload` 以確保套用變更。

**測試 skill 是否載入** - 直接詢問 Copilot：
```bash
> What skills do you have available for checking code quality?
# 中文 Prompt：你有哪些可用於檢查 code quality 的 skills？
# Copilot will describe relevant skills it found
```

**我如何知道我的 skill 實際上在運作？**

1. **檢查輸出格式**：如果你的 skill 指定了輸出格式（如 `[CRITICAL]` 標籤），請在回應中查找它
2. **直接詢問**：獲得回應後，問「Did you use any skills for that?」
3. **有無比較**：使用 `--no-custom-instructions` 嘗試相同的提示詞以查看差異：
   ```bash
   # With skills
   copilot --allow-all -p "Review @file.py for security issues"
   # 中文 Prompt：Review @file.py 的 security 問題

   # Without skills (baseline comparison)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   # 中文 Prompt：Review @file.py 的 security 問題
   ```
4. **檢查具體檢查項目**：如果你的 skill 包含具體的檢查（如「函數超過 50 行」），看看這些是否出現在輸出中

</details>

---

# 總結

## 🔑 重點摘要

1. **Skills 是自動的**：當你的提示詞符合 skill 的描述時，Copilot 就會載入它們
2. **直接呼叫**：你也可以使用 `/skill-name` 作為斜線指令直接呼叫 skills
3. **SKILL.md 格式**：YAML frontmatter（name、description、選用的 license）加上 markdown 指令
4. **位置很重要**：`.github/skills/` 用於專案/團隊共用，`~/.copilot/skills/` 用於個人使用
5. **描述是關鍵**：撰寫符合你自然提問方式的描述

> 📋 **快速參考**：請參閱 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) 取得完整的指令和快捷鍵清單。

---

## ➡️ 接下來

Skills 透過自動載入的指令擴展了 Copilot 的能力。但連接到外部服務呢？這就是 MCP 的用武之地。

在 **[第 06 章：MCP Servers](../06-mcp-servers/README-zh_tw.md)** 中，你將學習：

- 什麼是 MCP（Model Context Protocol）
- 連接到 GitHub、檔案系統和文件服務
- 設定 MCP 伺服器
- 多伺服器工作流程

---

**[← 回到第 04 章](../04-agents-custom-instructions/README-zh_tw.md)** | **[繼續前往第 06 章 →](../06-mcp-servers/README-zh_tw.md)**
