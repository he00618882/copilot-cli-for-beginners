![Chapter 00: Quick Start](images/chapter-header.png)

歡迎！在本章中，你將安裝 GitHub Copilot CLI（命令列介面），使用你的 GitHub 帳號登入，並驗證一切正常運作。這是一個快速設定章節。完成設定後，真正的示範將從第 01 章開始！

## 🎯 學習目標

完成本章後，你將：

- 安裝 GitHub Copilot CLI
- 使用你的 GitHub 帳號登入
- 透過簡單測試驗證其正常運作

> ⏱️ **預估時間**：約 10 分鐘（閱讀 5 分鐘 + 實作 5 分鐘）

---

## ✅ 前置條件

- **GitHub 帳號**且具備 Copilot 存取權限。[查看訂閱方案](https://github.com/features/copilot/plans)。學生/教師可透過 [GitHub Education](https://education.github.com/pack) 免費取得 Copilot Pro。
- **終端機基礎操作**：熟悉 `cd` 和 `ls` 等指令

### 何謂「Copilot 存取權限」

GitHub Copilot CLI 需要有效的 Copilot 訂閱。你可以在 [github.com/settings/copilot](https://github.com/settings/copilot) 確認你的狀態。你應該會看到以下其中之一：

- **Copilot Individual** - 個人訂閱
- **Copilot Business** - 透過你的組織
- **Copilot Enterprise** - 透過你的企業
- **GitHub Education** - 已驗證學生/教師免費使用

若你看到「You don't have access to GitHub Copilot」，你需要使用免費方案、訂閱付費方案，或加入提供存取權限的組織。

---

## 安裝

> ⏱️ **時間估計**：安裝需要 2-5 分鐘。驗證身份另需 1-2 分鐘。

### GitHub Codespaces（免安裝）

如果你不想安裝任何前置條件，可以使用 GitHub Codespaces，它已預先備妥 GitHub Copilot CLI（你需要登入），並預先安裝了 Python 和 pytest。

1. 將[此儲存庫 Fork](https://github.com/github/copilot-cli-for-beginners/fork) 到你的 GitHub 帳號
2. 選擇 **Code** > **Codespaces** > **Create codespace on main**
3. 等待幾分鐘讓容器建置完成
4. 準備就緒！終端機將在 Codespace 環境中自動開啟。

> 💡 **在 Codespace 中驗證**：執行 `cd samples/book-app-project && python book_app.py help` 確認 Python 和範例應用程式正常運作。

### 本機安裝

若你想在本機執行 Copilot CLI 並搭配課程範例，請依照以下步驟操作。

1. 複製儲存庫以取得本機的課程範例：

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 使用以下其中一種方式安裝 Copilot CLI。

    > 💡 **不確定要選哪個？** 如果你已安裝 Node.js，使用 `npm` 是最快的方式。否則，選擇符合你系統的選項。

    ### 所有平台（npm）

    ```bash
    # If you have Node.js installed, this is a quick way to get the CLI
    npm install -g @github/copilot
    ```

    ### macOS/Linux（Homebrew）

    ```bash
    brew install copilot-cli
    ```

    ### Windows（WinGet）

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux（安裝腳本）

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

---

## 驗證身份

在 `copilot-cli-for-beginners` 儲存庫的根目錄開啟終端機視窗，啟動 CLI 並允許存取該資料夾。

```bash
copilot
```

系統會要求你信任包含儲存庫的資料夾（如果你尚未信任）。你可以選擇單次信任或在所有未來的工作階段中信任。

<img src="images/copilot-trust.png" alt="Trusting files in a folder with the Copilot CLI" width="800"/>

信任資料夾後，你可以使用 GitHub 帳號登入。

```
> /login
```

**接下來會發生什麼：**

1. Copilot CLI 顯示一次性驗證碼（例如 `ABCD-1234`）
2. 你的瀏覽器會開啟 GitHub 的裝置授權頁面。若尚未登入 GitHub，請先登入。
3. 在提示處輸入驗證碼
4. 選擇「Authorize」授予 GitHub Copilot CLI 存取權限
5. 返回你的終端機——你已成功登入！

<img src="images/auth-device-flow.png" alt="Device Authorization Flow - showing the 5-step process from terminal login to signed-in confirmation" width="800"/>

*裝置授權流程：你的終端機產生驗證碼，你在瀏覽器中確認，Copilot CLI 完成驗證。*

**提示**：登入狀態會在工作階段之間保留。除非你的 token 過期或明確登出，否則只需執行一次。

---

## 驗證是否正常運作

### 步驟 1：測試 Copilot CLI

現在你已登入，讓我們驗證 Copilot CLI 是否正常運作。在終端機中，若尚未啟動 CLI，請先啟動：

```bash
> Say hello and tell me what you can help with
# 中文 Prompt：跟我打個招呼，並告訴我你能幫什麼忙
```

收到回應後，你可以退出 CLI：

```bash
> /exit
```

---

<details>
<summary>🎬 看看實際效果！</summary>

![Hello Demo](images/hello-demo.gif)

*示範輸出結果僅供參考。你的模型、工具和回應可能與此處顯示的不同。*

</details>

---

**預期輸出**：一個友善的回應，列出 Copilot CLI 的各項功能。

### 步驟 2：執行範例 Book App

課程提供了一個範例應用程式，你將在整個課程中使用 CLI 來探索和改善它 *（你可以在 /samples/book-app-project 查看此程式碼）*。在開始之前，請先確認 *Python 書籍收藏終端機應用程式* 可以正常運作。根據你的系統執行 `python` 或 `python3`。

> **注意：** 課程中展示的主要範例使用 Python（`samples/book-app-project`），因此若你選擇本機安裝，需要在本機具備 [Python 3.10+](https://www.python.org/downloads/)（Codespace 已預先安裝）。如果你偏好其他語言，JavaScript（`samples/book-app-project-js`）和 C#（`samples/book-app-project-cs`）版本也提供使用。每個範例都有一份 README，內含該語言執行應用程式的說明。

```bash
cd samples/book-app-project
python book_app.py list
```

**預期輸出**：包含「The Hobbit」、「1984」和「Dune」在內的 5 本書清單。

### 步驟 3：搭配 Book App 試用 Copilot CLI

若你執行了步驟 2，請先回到儲存庫根目錄：

```bash
cd ../..   # Back to the repository root if needed
copilot 
> What does @samples/book-app-project/book_app.py do?
# 中文 Prompt：@samples/book-app-project/book_app.py 這個程式在做什麼？
```

**預期輸出**：book app 主要功能和指令的摘要說明。

若遇到錯誤，請查看下方的[疑難排解章節](#疑難排解)。

完成後，你可以退出 Copilot CLI：

```bash
> /exit
```

---

## ✅ 你已準備就緒！

安裝部分到此結束。真正有趣的內容從第 01 章開始，你將：

- 觀看 AI 審查 book app 並即時發現程式碼品質問題
- 學習三種使用 Copilot CLI 的不同方式
- 從自然語言描述產生可運行的程式碼

**[繼續前往第 01 章：First Steps →](../01-setup-and-first-steps/README-zh_tw.md)**

---

## 疑難排解

### "copilot: command not found"

CLI 未安裝。請嘗試不同的安裝方式：

```bash
# If brew failed, try npm:
npm install -g @github/copilot

# Or the install script:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. 在 [github.com/settings/copilot](https://github.com/settings/copilot) 確認你擁有 Copilot 訂閱
2. 若使用工作帳號，請確認你的組織允許 CLI 存取

### "Authentication failed"

重新驗證身份：

```bash
copilot
> /login
```

### 瀏覽器未自動開啟

請手動前往 [github.com/login/device](https://github.com/login/device) 並輸入終端機顯示的驗證碼。

### Token 已過期

直接再次執行 `/login`：

```bash
copilot
> /login
```

### 仍然遇到問題？

- 查看 [GitHub Copilot CLI 文件](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- 搜尋 [GitHub Issues](https://github.com/github/copilot-cli/issues)

---

## 🔑 重點回顧

1. **GitHub Codespace 是快速入門的好方法** - Python、pytest 和 GitHub Copilot CLI 均已預先安裝，讓你可以直接投入示範
2. **多種安裝方式** - 選擇適合你系統的方式（Homebrew、WinGet、npm 或安裝腳本）
3. **一次性驗證身份** - 登入狀態會保留直到 token 過期
4. **book app 可正常運作** - 整個課程中你都會使用 `samples/book-app-project`

> 📚 **官方文件**：[安裝 Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) 了解安裝選項和需求。

> 📋 **快速參考**：查看 [GitHub Copilot CLI 指令參考](https://docs.github.com/en/copilot/reference/cli-command-reference) 取得完整的指令和快捷鍵清單。

---

**[繼續前往第 01 章：First Steps →](../01-setup-and-first-steps/README-zh_tw.md)**
