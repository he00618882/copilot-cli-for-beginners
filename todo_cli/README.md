# To-Do List CLI (Python)

## 專案說明
這是一個以 Python 撰寫的命令列 To-Do List 應用程式，支援以下核心功能：

- 新增任務
- 列出任務
- 標記完成
- 刪除任務

資料會儲存在本地 JSON 檔案（預設 `tasks.json`），符合 [PRD](../PRD.md) 的驗收準則。

## 安裝方式
### 1. 進入專案目錄
```bash
cd /workspaces/copilot-cli-for-beginners
```

### 2. （可選）建立虛擬環境
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安裝測試依賴
```bash
pip install pytest
```

## 使用方式
使用模組方式執行：

```bash
python3 -m todo_cli <command> [args] [--file <path>]
```

可用指令：

- `add <title>`：新增任務
- `list`：列出所有任務
- `complete <id>`：將指定 ID 任務標記為完成
- `delete <id>`：刪除指定 ID 任務

可用選項：

- `--file <path>`：指定 JSON 儲存檔案路徑（預設 `tasks.json`）

## 範例
### 新增任務
```bash
python3 -m todo_cli add "買牛奶"
# 已新增任務 #1: 買牛奶
```

### 列出任務
```bash
python3 -m todo_cli list
# [ ] 1: 買牛奶
```

### 標記完成
```bash
python3 -m todo_cli complete 1
# 已完成任務 #1: 買牛奶
```

### 再次列出任務
```bash
python3 -m todo_cli list
# [x] 1: 買牛奶
```

### 刪除任務
```bash
python3 -m todo_cli delete 1
# 已刪除任務 #1
```

## 執行測試
```bash
python3 -m pytest -q
```
