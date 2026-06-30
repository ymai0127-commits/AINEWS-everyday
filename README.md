# AINEWS-everyday 🤖📰

每天自动收集 AI 和科技领域的最新新闻，���送到你的邮箱。

## ✨ 功能特性

✨ **自动化新闻收集**
- 每天晚上 **11:00 (北京时间)** 自动运行
- 从 **8+ 优质新闻源** 收集最新 AI 新闻
- 包含完整的信息来源和时间戳
- 自动按分类整理新闻

📧 **智能邮件推送**
- 每天自动发送到指定邮箱
- **专业 HTML 格式**，美观易读
- 新闻按分类展示（论文、创业、产品等）
- 支持 Gmail 等主流邮箱

⏰ **无服务器部署**
- 使用 GitHub Actions 每天自动运行
- 无需本地服务器或付费服务
- 完全免费，自动存档新闻

## 🔗 新闻来源 (8+ Premium Sources)

| 来源 | 类别 | 说明 |
|------|------|------|
| **Hacker News** | Technology & Startups | 科技和创业新闻 |
| **ArXiv** | AI Research & Papers | 最新 AI/ML 研究论文 |
| **TechCrunch** | Tech News | 科技新闻和产品 |
| **Product Hunt** | New Products | 新产品发现 |
| **Towards Data Science** | AI Articles | 高质量技术文章 |
| **Deeplearning.AI** | AI Education | Andrew Ng 创办的 AI 教育平台 |
| **OpenAI Blog** | OpenAI News | OpenAI 最新动态 |
| **Google AI Blog** | Google AI | Google AI 研究进展 |

## 🚀 快速开始

### 1️⃣ Fork 本仓库

点击右上角的 **Fork** 按钮

### 2️⃣ 配置环境变量

在你 fork 的仓库中，进入 **Settings → Secrets and variables → Actions**，添加以下 3 个 Secrets：

```
RECIPIENT_EMAIL: 你的邮箱地址 (接收新闻的邮箱)
SENDER_EMAIL: 发送邮箱地址 (推荐使用 Gmail)
SENDER_PASSWORD: 邮箱应用密码
```

### 3️⃣ 配置 Gmail (推荐)

**如果使用 Gmail：**
1. 打开 [Google Account Security](https://myaccount.google.com/security)
2. 启用 **2-Step Verification (两步验证)**
3. 在安全设置中生成 **App Password (应用专用密码)**
4. 将应用密码复制到 `SENDER_PASSWORD`

**如果使用其他邮箱：**
- QQ邮箱: 使用授权码而非密码
- 163邮箱: 类似 QQ，需要生成授权码
- Outlook: 使用应用密码

### 4️⃣ 启用 GitHub Actions

仓库的 **Actions** 选项卡中，点击 **Enable workflows**

### 5️⃣ 完成！

- 工作流每天北京时间 **晚上 11:00** 自动运行
- 也可以手动触发: 进入 **Actions** 选项卡，点击 **Run workflow**

## 📁 项目结构

```
.
├── .github/
│   └── workflows/
│       └── daily-news.yml              # GitHub Actions 工作流（每天 23:00 执行）
├── scripts/
│   ├── fetch_news.py                   # 新闻爬取脚本（8个数据源）
│   ├── send_email.py                   # 邮件发送脚本（HTML 格式）
│   └── requirements.txt                # Python 依赖
├── news/
│   └── 2026-XX-XX.json                # 每日新闻 JSON 存档
└── README.md
```

## 🔧 本地运行

### 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 设置环境变量

```bash
export RECIPIENT_EMAIL="your-email@gmail.com"
export SENDER_EMAIL="sender@gmail.com"
export SENDER_PASSWORD="your-app-password"
```

### 运行脚本

```bash
# 第一步：爬取新闻
python scripts/fetch_news.py

# 第二步：发送邮件
python scripts/send_email.py
```

## ⚙️ 自定义配置

### 修改运行时间

编辑 `.github/workflows/daily-news.yml`：

```yaml
schedule:
  - cron: '0 15 * * *'  # UTC 15:00 = 北京时间 23:00
                        # 修改数字来改变时间
                        # 例如: 0 10 * * * = 北京时间 18:00
```

Cron 格式: `分钟 小时 日期 月份 星期`

### 添加新的新闻源

在 `scripts/fetch_news.py` 中：

1. 创建新的 NewsSource 子类
2. 实现 `fetch()` 方法
3. 在 `fetch_all_news()` 中添加到 sources 列表

### 修改邮件格式

编辑 `scripts/send_email.py` 中的 `generate_html_email()` 函数调整 HTML/CSS

## 📊 邮件示例

收到的邮件会按以下分类展示：

- 🔬 **AI Research & Papers** - 最新论文
- 🚀 **Technology & Startups** - 科技新闻
- 💡 **New AI Products & Tools** - 新产品
- 📚 **AI Technical Articles** - 技术文章
- 📢 **OpenAI/Google AI News** - 大厂动态

## 🐛 故障排除

### ❌ 没有收到邮件

1. **检查 GitHub Actions 执行日志**
   - 进入 **Actions** 选项卡
   - 点击最近的 workflow run
   - 查看 "Fetch AI News" 或 "Send Email Digest" 步骤的日志

2. **验证环境变量**
   - 检查 Secrets 是否正确配置
   - 确保没有多余空格

3. **检查邮箱设置**
   - Gmail: 确认已启用 2FA 和应用密码
   - 其他邮箱: 检查是否需要授权码
   - 查看垃圾邮件文件夹

### ❌ 新闻数量少

- 某些源可能暂时无法访问（网络问题）
- 脚本会自动重试，但不会中断
- 检查日志查看具体的失败源

### ❌ "Authentication failed"

- 确认 SENDER_PASSWORD 是 **应用专用密码**，不是账户密码
- 对于 Gmail，必须先启用 2FA

## 📝 许可证

MIT

## 👨‍💻 贡献

欢迎提交 Issue 和 Pull Request！

- 发现 Bug？提交 Issue
- 想添加新闻源？发送 PR
- 改进邮件格式？发送 PR

## 🌟 如果有帮助

如果这个项目对你有帮助，请 ⭐ Star 一下！

---

**最后更新**: 2026-06-30  
**维护者**: [ymai0127-commits](https://github.com/ymai0127-commits)
