# CI/CD 整合

> 📖 **先備條件**：請先完成[第 07 章：整合應用](../07-putting-it-together/README-zh_tw.md)後再閱讀本附錄。
>
> ⚠️ **本附錄適合已有現行 CI/CD 流程的團隊。** 若你對 GitHub Actions 或 CI/CD 概念較不熟悉，請先從第 07 章的[程式碼審查自動化](../07-putting-it-together/README-zh_tw.md#workflow-3-code-review-automation-optional)章節中，較簡單的 pre-commit hook 方式開始。

本附錄說明如何將 GitHub Copilot CLI 整合至 CI/CD 流程，以在 pull request 上自動執行程式碼審查。

---

## GitHub Actions 工作流程

此工作流程會在 pull request 被開啟或更新時，自動審查有變動的檔案：

```yaml
# .github/workflows/copilot-review.yml
name: Copilot Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed to compare with main branch

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Get list of changed JS/TS files
          FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts|jsx|tsx)$' || true)
          
          if [ -z "$FILES" ]; then
            echo "No JavaScript/TypeScript files changed"
            exit 0
          fi
          
          echo "# Copilot Code Review" > review.md
          echo "" >> review.md
          
          for file in $FILES; do
            echo "Reviewing $file..."
            echo "## $file" >> review.md
            echo "" >> review.md
            
            # Use --silent to suppress progress output
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // Only post if there's meaningful content
            if (review.includes('CRITICAL') || review.includes('HIGH')) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: review
              });
            } else {
              console.log('No critical issues found, skipping comment');
            }
```

---

## 設定選項

### 限制審查範圍

你可以將審查聚焦在特定類型的問題上：

```yaml
# Security-only review
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# Performance-only review
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### 處理大型 PR

對於包含大量檔案的 PR，可考慮分批處理或設定限制：

```yaml
# Limit to first 10 files
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# Or set a timeout per file
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### 團隊設定

為讓團隊成員的審查結果保持一致，可建立共用設定檔：

```json
// .copilot/config.json (committed to repo)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## 替代方案：PR 審查 Bot

若需要更完善的審查工作流程，可考慮使用 GitHub Copilot 雲端 agent：

```yaml
# .github/workflows/copilot-agent-review.yml
name: Request Copilot Review

on:
  pull_request:
    types: [opened, ready_for_review]

jobs:
  request-review:
    runs-on: ubuntu-latest
    steps:
      - name: Request Copilot Review
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.pulls.requestReviewers({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              reviewers: ['copilot[bot]']
            });
```

---

## CI/CD 整合最佳實踐

1. **使用 `--silent` 旗標**——抑制進度輸出，讓日誌更清晰
2. **設定 timeout**——避免卡住的審查阻塞整個流程
3. **篩選檔案類型**——只審查相關檔案（略過自動產生的程式碼與相依套件）
4. **注意 rate limiting**——對大型 PR 的審查請求分散執行
5. **優雅地處理失敗**——不要因審查失敗而阻擋合併；記錄錯誤後繼續執行

---

## 疑難排解

### CI 中出現「Authentication failed」

請確認工作流程具有正確的權限設定：

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### 審查逾時

增加 timeout 時間或縮小審查範圍：

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### 大型檔案超出 token 限制

略過過大的檔案：

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← 返回第 07 章](../07-putting-it-together/README-zh_tw.md)** | **[返回附錄](README-zh_tw.md)**
