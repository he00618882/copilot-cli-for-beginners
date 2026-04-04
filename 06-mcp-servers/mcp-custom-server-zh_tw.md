# 建立自訂 MCP 伺服器

> ⚠️ **此內容完全是選用的。** 你可以只使用預建的 MCP 伺服器（GitHub、filesystem、Context7）就能高效使用 Copilot CLI。本指南適合想要將 Copilot 連接到自訂內部 API 的開發者。更多詳情請參閱 [MCP for Beginners 課程](https://github.com/microsoft/mcp-for-beginners)。
>
> **前置條件：**
> - 熟悉 Python
> - 了解 `async`/`await` 模式
> - 系統上有可用的 `pip`（此 dev container 已包含）
>
> **[← 返回第 06 章：MCP 伺服器](README-zh_tw.md)**

---

想要將 Copilot 連接到你自己的 API 嗎？以下是如何在 Python 中建立一個簡單的 MCP 伺服器，用來查詢書籍資訊，與你在整個課程中使用的書籍應用程式專案相互呼應。

## 專案設定

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **`mcp` 套件是什麼？** 它是用於建立 MCP 伺服器的官方 Python SDK。它處理協定細節，讓你可以專注在你的工具上。

## 伺服器實作

建立一個名為 `server.py` 的檔案：

```python
# server.py
import json
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("book-lookup")

# Sample book database (in a real server, this could query an API or database)
BOOKS_DB = {
    "978-0-547-92822-7": {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "genre": "Fantasy",
    },
    "978-0-451-52493-5": {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian Fiction",
    },
    "978-0-441-17271-9": {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Science Fiction",
    },
}


@mcp.tool()
def lookup_book(isbn: str) -> str:
    """Look up a book by its ISBN and return title, author, year, and genre."""
    book = BOOKS_DB.get(isbn)
    if book:
        return json.dumps(book, indent=2)
    return f"No book found with ISBN: {isbn}"


@mcp.tool()
def search_books(query: str) -> str:
    """Search for books by title or author. Returns all matching results."""
    query_lower = query.lower()
    results = [
        {**book, "isbn": isbn}
        for isbn, book in BOOKS_DB.items()
        if query_lower in book["title"].lower()
        or query_lower in book["author"].lower()
    ]
    if results:
        return json.dumps(results, indent=2)
    return f"No books found matching: {query}"


@mcp.tool()
def list_all_books() -> str:
    """List all books in the database with their ISBNs."""
    books_list = [
        {"isbn": isbn, "title": book["title"], "author": book["author"]}
        for isbn, book in BOOKS_DB.items()
    ]
    return json.dumps(books_list, indent=2)


if __name__ == "__main__":
    mcp.run()
```

**這裡發生了什麼：**

| 部分 | 功能 |
|------|------|
| `FastMCP("book-lookup")` | 建立一個名為 "book-lookup" 的伺服器 |
| `@mcp.tool()` | 將函式註冊為 Copilot 可以呼叫的工具 |
| 型別提示 + 文件字串 | 告訴 Copilot 每個工具的功能和所需的參數 |
| `mcp.run()` | 啟動伺服器並監聽請求 |

> 💡 **為什麼使用裝飾器？** `@mcp.tool()` 裝飾器就是你所需要的全部。MCP SDK 會自動讀取你函式的名稱、型別提示和文件字串來產生工具的 schema。不需要手動編寫 JSON schema！

## 設定

將以下內容加入你的 `~/.copilot/mcp-config.json`：

```json
{
  "mcpServers": {
    "book-lookup": {
      "type": "local",
      "command": "python3",
      "args": ["./book-lookup-mcp-server/server.py"],
      "tools": ["*"]
    }
  }
}
```

## 使用方式

```bash
copilot

> Look up the book with ISBN 978-0-547-92822-7
# 中文 Prompt：查詢 ISBN 978-0-547-92822-7 的書籍

{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "genre": "Fantasy"
}

> Search for books by Orwell
# 中文 Prompt：搜尋 Orwell 的書籍

[
  {
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "genre": "Dystopian Fiction",
    "isbn": "978-0-451-52493-5"
  }
]

> List all available books
# 中文 Prompt：列出所有可用的書籍

[Shows all books in the database with ISBNs]
```

## 後續步驟

建立基本伺服器後，你可以：

1. **新增更多工具** - 每個 `@mcp.tool()` 函式都會成為 Copilot 可以呼叫的工具
2. **連接真實 API** - 將模擬的 `BOOKS_DB` 替換為實際的 API 呼叫或資料庫查詢
3. **新增驗證** - 安全地處理 API 金鑰和 token
4. **分享你的伺服器** - 發布到 PyPI，讓其他人可以使用 `pip` 安裝

## 參考資源

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP 伺服器範例](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners 課程](https://github.com/microsoft/mcp-for-beginners)

---

**[← 返回第 06 章：MCP 伺服器](README-zh_tw.md)**
