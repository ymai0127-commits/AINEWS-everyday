# AINEWS-everyday 🤖📰

每天自动收集 AI 和科技领域的最新新闻，发送到你的邮箱。

## 功能特性

✨ **自动化新闻收集**
- 每天收集 20 条最新 AI/科技新闻
- 多个权威信息源
- 包含完整的信息来源和时间戳

📧 **邮件推送**
- 每天自动发送到指定邮箱
- 清晰的 HTML 格式
- 包含新闻标题、摘要、来源、发布时间

⏰ **定时执行**
- 使用 GitHub Actions 每天自动运行
- 无需本地服务器
- 完全免费

## 新闻来源

- **HN**: Hacker News - 科技和创业新闻
- **ArXiv**: 最新 AI 研究论文
- **TechCrunch**: 科技初创和产品新闻
- **Product Hunt**: 新产品发现
- **Medium**: 技术文章和分析

## 快速开始

### 1. 配置环境变量

在 GitHub 仓库设置中添加以下 Secrets：

```
RECIPIENT_EMAIL: 你的邮箱地址 (接收新闻的邮箱)
SENDER_EMAIL: 发送邮箱地址 (推荐使用 Gmail)
SENDER_PASSWORD: 邮箱授权密码或密钥
```

### 2. 配置发送邮箱

**使用 Gmail 的步骤：**
1. 启用 2FA (两步验证)
2. 生成应用专用密码
3. 将应用密码添加到 `SENDER_PASSWORD`

### 3. 手动触发或等待定时执行

工作流每天 UTC 时间 08:00 自动运行。

## 项目结构

```
.
├── .github/
│   └── workflows/
│       └── daily-news.yml       # GitHub Actions 工作流
├── scripts/
│   ├── fetch_news.py           # 新闻爬取脚本
│   ├── send_email.py           # 邮件发送脚本
│   └── requirements.txt         # Python 依赖
├── README.md                   # 本文件
└── news/
    └── 2026-04-29.json        # 每日新闻存档
```

## 使用方法

### 本地运行

```bash
# 安装依赖
pip install -r scripts/requirements.txt

# 设置环境变量
export RECIPIENT_EMAIL="your-email@gmail.com"
export SENDER_EMAIL="sender@gmail.com"
export SENDER_PASSWORD="your-app-password"

# 运行爬虫和发送邮件
python scripts/fetch_news.py
python scripts/send_email.py
```

### 自动运行

无需任何操作，GitHub Actions 会每天自动执行。

## 自定义配置

编辑 `.github/workflows/daily-news.yml` 修改：
- 运行时间 (cron schedule)
- 新闻数量 (默认 20)
- 信息源

## 开发者

[ymai0127-commits](https://github.com/ymai0127-commits)

## 许可证

MIT
