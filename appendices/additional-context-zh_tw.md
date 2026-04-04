# 額外的 Context 功能

> 📖 **先備條件**：請先完成[第 02 章：Context 與對話](../02-context-conversations/README-zh_tw.md)後再閱讀本附錄。

本附錄涵蓋兩個額外的 context 功能：使用圖片，以及管理多個目錄的權限。

---

## 使用圖片

你可以使用 `@` 語法在對話中加入圖片。Copilot 能夠分析截圖、設計稿、圖表及其他視覺內容。

### 基本圖片參照

```bash
copilot

> @screenshot.png What's happening in this UI?
# 中文 Prompt：@screenshot.png 這個 UI 發生了什麼事？

# Copilot analyzes the image and responds

> @mockup.png @current-design.png Compare these two designs
# 中文 Prompt：@mockup.png @current-design.png 比較這兩個設計

# You can also drag and drop images or paste from clipboard
```

### 支援的圖片格式

| 格式 | 最適合的用途 |
|------|-------------|
| PNG | 截圖、UI 設計稿、圖表 |
| JPG/JPEG | 照片、複雜圖片 |
| GIF | 簡單圖表（僅第一幀） |
| WebP | 網頁截圖 |

### 圖片的實際應用場景

**1. UI 除錯**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
# 中文 Prompt：@bug-screenshot.png 按鈕沒有正確對齊，可能是哪個 CSS 造成的？
```

**2. 設計實作**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
# 中文 Prompt：@figma-export.png 撰寫符合此設計的 HTML 和 Tailwind CSS
```

**3. 錯誤分析**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
# 中文 Prompt：@error-screenshot.png 這個錯誤是什麼意思，要怎麼 fix？
```

**4. 架構審查**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
# 中文 Prompt：@whiteboard-diagram.png 將這張架構圖轉換成可放入文件的 Mermaid diagram
```

**5. 前後對比**
```bash
> @before.png @after.png What changed between these two versions of the UI?
# 中文 Prompt：@before.png @after.png 這兩個 UI 版本之間有什麼變化？
```

### 結合圖片與程式碼

當圖片與程式碼 context 結合使用時，效果會更加強大：

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
# 中文 Prompt：截圖中的 header 看起來不對勁，是程式碼中的什麼造成的？
```

### 圖片使用技巧

- **裁剪截圖**，只保留相關部分（節省 context token）
- **使用高對比**，讓要分析的 UI 元素更清晰
- **必要時加上標注**——在上傳前圈出或標示問題區域
- **一張圖片對應一個概念**——多張圖片可以使用，但請保持聚焦

---

## 權限設定模式

Copilot 預設只能存取當前目錄中的檔案。若要存取其他位置的檔案，需要先授予存取權限。

### 新增目錄

```bash
# Add a directory to the allowed list
copilot --add-dir /path/to/other/project

# Add multiple directories
copilot --add-dir ~/workspace --add-dir /tmp
```

### 允許所有路徑

```bash
# Disable path restrictions entirely (use with caution)
copilot --allow-all-paths
```

### 在 Session 中操作

```bash
copilot

> /add-dir /path/to/other/project
# Now you can reference files from that directory

> /list-dirs
# See all allowed directories
```

### 用於自動化

```bash
# Allow all permissions for non-interactive scripts
copilot -p "Review @src/" --allow-all

# Or use the memorable alias
copilot -p "Review @src/" --yolo
```

### 需要多目錄存取的情境

以下是常見需要這些權限的使用場景：

1. **Monorepo 開發**——比對多個套件之間的程式碼
2. **跨專案重構**——更新共用函式庫
3. **文件撰寫專案**——參照多個程式碼庫
4. **遷移工作**——比對新舊實作

---

**[← 返回第 02 章](../02-context-conversations/README-zh_tw.md)** | **[返回附錄](README-zh_tw.md)**
