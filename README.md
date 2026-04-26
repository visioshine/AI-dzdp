# 大众生活 - 本地生活服务平台

这是一个仿大众点评的本地生活服务平台项目。

## 项目结构

```
AI-dzdp/
├── backend/              # FastAPI 后端
│   ├── main.py          # 主应用文件
│   ├── auth.py          # 认证相关
│   ├── config.py        # 配置
│   ├── database.py      # 数据库连接
│   ├── models.py        # 数据模型
│   ├── schemas.py       # Pydantic schemas
│   └── email_service.py # 邮件服务
├── index.html           # 前端页面
├── mock_data.js         # 模拟数据
├── requirements.txt     # Python 依赖
├── start_server.js      # Node.js 模拟服务器
└── dianping.db          # SQLite 数据库
```

## 运行方式

### 方式一：使用 FastAPI 完整后端（推荐）

#### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

#### 2. 启动后端服务器

```bash
python run.py
```

或者直接使用 uvicorn：

```bash
uvicorn backend.main:app --reload
```

#### 3. 访问应用

打开浏览器访问：http://localhost:8000

### 方式二：使用 Node.js 模拟服务器

如果没有安装 Python，可以使用 Node.js 模拟服务器：

```bash
node start_server.js
```

然后访问：http://localhost:8000

### 方式三：直接打开 index.html

直接在浏览器中打开 `index.html` 文件，大部分功能可以正常使用（API 请求会使用模拟数据作为 fallback）。

## 功能特性

- 用户注册和登录
- 商家浏览和搜索
- 商家分类筛选
- 商家详情查看
- 商品评价和评分
- 用户个人中心
- 密码重置功能
- 收藏功能
- 响应式设计

## 测试账户

- 用户名：`demo`
- 密码：`demo123`
- 邮箱：`demo@example.com`

## 密码重置功能

在找回密码页面，输入任意邮箱，系统会在控制台显示 6 位验证码，使用该验证码即可完成密码重置。

## 配置

如需配置邮件服务，请编辑 `.env` 文件：

```env
ENABLE_EMAIL_SENDING=true
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-password
SENDER_EMAIL=your-email@example.com
SECRET_KEY=your-secret-key
```
