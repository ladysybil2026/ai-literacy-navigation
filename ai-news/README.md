---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100d0975a36ef2e8545f1229b601364bce5aabf14e2c638ba4969a94783b17e3860022100f55e12757881c68c6afd70409fa407cc060c62beb1c86d5f86f25c6e53bfc3f6
    ReservedCode2: 304402207b2d9386fa5d271d6864f7caadc6dab57db87b72f5eb40f67366f984f29c5ac2022069322cd133d693df6b91818ba013fc0402a0d04903262369e25aed89fb642b78
---

# AI新闻自动生成系统

## 项目说明

本系统用于自动生成每日AI新闻，可集成到上海第二工业大学AI素养平台。

### 功能特点

- ✅ 自动搜索当日AI新闻
- ✅ 智能分类（AI模型、AI产业、AI政策、AI安全、AI活动）
- ✅ 符合项目现有样式的HTML输出
- ✅ 每日自动更新

### 文件结构

```
ai-news/
├── ai-news-generator.py  # 主生成脚本
├── ai-news.html         # 生成的新闻HTML（每日更新）
├── README.md            # 本说明文件
└── archive/             # 历史存档
    └── ai-news-YYYYMMDD.html
```

## 使用方法

### 方法一：使用已设置的定时任务（推荐）

系统已配置每天早上9点自动运行，你只需：

1. 每天早上9点后，查看生成的HTML文件
2. 复制 `ai-news.html` 中的内容
3. 替换到你项目中的"AI新鲜事"栏目

### 方法二：手动运行脚本

```bash
cd /workspace/ai-news
python3 ai-news-generator.py
```

### 方法三：集成到你的GitHub项目

#### 步骤1：下载脚本到本地

将以下文件下载到你的电脑：
- `/workspace/ai-news/ai-news-generator.py`
- `/workspace/ai-news/ai-news.html`（示例输出）

#### 步骤2：在Trae IDE中打开

1. 在Trae中打开你的项目：`file:///D:/AAA学习论文重要要要要要要要要/coding 实例/AI素养导航`
2. 创建新文件：`ai-news-generator.py`，粘贴下载的脚本内容

#### 步骤3：设置GitHub Actions自动运行

在你的GitHub仓库中添加 `.github/workflows/ai-news.yml`：

```yaml
name: Daily AI News
on:
  schedule:
    - cron: '0 1 * * *'  # 每天早上9点（北京时间）
  workflow_dispatch:      # 支持手动触发

jobs:
  generate-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Generate AI News
        run: python ai-news-generator.py

      - name: Commit and push
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add ai-news.html
          git diff --staged --quiet || git commit -m "Auto update AI news $(date +'%Y-%m-%d')"
          git push
```

## 预览效果

查看今日生成的新闻示例：
- 文件：`ai-news.html`
- 样式：符合项目现有CSS样式

## 自定义配置

在 `ai-news-generator.py` 中修改以下参数：

```python
NEWS_COUNT = 8                    # 生成的新闻数量
SEARCH_QUERIES = [...]            # 搜索关键词
PROJECT_PATH = "/workspace/ai-news/"  # 输出路径
```

## 注意事项

1. **定时任务**：系统在云端运行，生成的文件保存在这里，你需要复制到本地项目
2. **手动同步**：由于权限限制，建议每天手动将生成的内容复制到你的项目中
3. **网络要求**：脚本需要网络访问来搜索新闻

## 技术支持

如有问题，请检查：
1. 网络连接是否正常
2. Python版本是否 >= 3.6
3. 依赖是否正确安装
