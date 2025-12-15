# Bailian 聊天机器人 - 阿里云百炼集成版

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![阿里云百炼](https://img.shields.io/badge/阿里云百炼-DashScope-orange.svg)](https://bailian.console.aliyun.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

这是一个基于  智能客服聊天机器人系统，基于python，并深度集成阿里云百炼 AI 服务，提供实时流式对话体验。

![系统架构图](./微信图片_20251212161526_172_338.png)

## ✨ 核心特性

### 🚀 技术亮点
- **流式响应** - 基于 Server-Sent Events (SSE) 的实时对话体验
- **智能回退** - 流式失败时自动切换至非流式模式
- **阿里云百炼集成** - 采用通义千问大模型，支持多轮对话
- **会话管理** - 支持云端和本地两种会话历史管理方式
- **Markdown 支持** - 前端自动渲染 AI 回复中的 Markdown 格式

### 🛠️ 开发特性
- **RESTful API** - 标准化的接口设计，易于集成
- **CORS 支持** - 完善的跨域请求处理
- **错误处理** - 详细的错误日志和用户友好的错误提示
- **配置化** - 通过环境变量灵活配置各项参数
- **健康检查** - 内置服务状态监控端点

### 💬 用户体验
- **实时打字动画** - 模拟真实对话体验
- **消息复制** - 一键复制 AI 回复内容
- **快捷按钮** - 预设常用问题快捷入口
- **响应式设计** - 支持桌面和移动设备
- **反馈系统** - 内置用户反馈收集功能

## 📋 系统要求

### 基础环境
- **Python**: 3.7 或更高版本
- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### 云服务要求
- **阿里云账号**: 已开通阿里云百炼服务
- **DashScope API Key**: 有效的 API 访问密钥
- **百炼应用 ID**: 已创建的智能体应用

## 🚀 快速开始

### 1️⃣ 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd bailian_ai_chatbox/backend

# 检查 Python 版本
python --version  # 确保 >= 3.7
```

### 2️⃣ 虚拟环境设置

**Windows 用户：**
```cmd
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

**Linux/macOS 用户：**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 3️⃣ 依赖安装

```bash
# 安装 Python 依赖包
pip install -r requirements.txt
```

### 4️⃣ 配置阿里云百炼

#### 4.1 获取阿里云百炼凭证
1. 登录 [阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. **获取 API Key**：在「密钥管理」页面创建并复制 API Key
3. **获取应用 ID**：在「应用管理」页面创建智能体应用并复制 APP_ID

#### 4.2 配置环境变量
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
```

编辑 `.env` 文件：
```env
# 阿里云百炼配置（必填）
API_KEY=sk-your-dashscope-api-key-here
APP_ID=your-bailian-app-id-here

# 服务器配置（可选）
HOST=0.0.0.0
PORT=8000
DEBUG=True

# AI 行为配置（可选）
SYSTEM_PROMPT=Answer questions only related to digital marketing, otherwise, say I dont know
TEMPERATURE=0.7
```

### 5️⃣ 配置验证

```bash
# 运行配置测试脚本
python test_config.py
```

如果看到 `🎉 所有测试通过！可以启动服务了` 提示，说明配置正确。

### 6️⃣ 启动服务

#### 方式一：使用启动脚本（推荐）

**Windows：**
```cmd
start.bat
```

**Linux/macOS：**
```bash
chmod +x start.sh
./start.sh
```

#### 方式二：手动启动
```bash
python run.py
```

### 7️⃣ 验证服务

访问健康检查端点：
```bash
curl http://localhost:8000/health
```

预期响应：
```json
{
    "status": "healthy",
    "service": "Bailian-chatbot-backend",
    "version": "1.0.0"
}
```

## 📡 API 接口文档

### 1. 健康检查

**端点**: `GET /health`

**响应示例**:
```json
{
    "status": "healthy",
    "service": "Bailian-chatbot-backend",
    "version": "1.0.0"
}
```

### 2. 获取聊天机器人配置

**端点**: `GET /myapi/v1/chat-bot-config`

**响应示例**:
```json
{
    "botStatus": 0,
    "StartUpMessage": "Hi, How are you?",
    "fontSize": "16",
    "userAvatarURL": "https://liangdabiao.com/wp-content/uploads/2025/06/a8a894b8b3e9259bb02ab0a7832372bb.png",
    "botImageURL": "https://liangdabiao.com/wp-content/uploads/2025/06/c892d890243984bb66f17f138412d5f4.png",
    "commonButtons": [
        {
            "buttonText": "I want your help!!!",
            "buttonPrompt": "I have a question about your courses"
        },
        {
            "buttonText": "I want a Discount",
            "buttonPrompt": "I want a discount"
        }
    ]
}
```

### 3. 流式聊天接口（主要使用）

**端点**: `POST /myapi/v1/chat-bot/stream`

**请求头**:
```http
Content-Type: application/json
```

**请求体**:
```json
{
    "last_prompt": "用户输入的最新消息",
    "conversation_history": [
        {
            "role": "user",
            "content": "历史用户消息"
        },
        {
            "role": "assistant",
            "content": "历史AI回复"
        }
    ],
    "session_id": "optional-session-id"
}
```

**响应**: Server-Sent Events 流式数据
```http
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

data: {"success": true, "content": "我是", "finished": false}

data: {"success": true, "content": "阿里云", "finished": false}

data: {"success": true, "content": "开发", "finished": true, "message": "Stream completed"}
```

### 4. 非流式聊天接口（备用回退）

**端点**: `POST /myapi/v1/chat-bot`

**请求体**: 与流式接口相同

**响应示例**:
```json
{
    "success": true,
    "message": "Response Generated",
    "result": "我是阿里云开发的大语言模型...",
    "session_id": "98ceb3ca0c4e4b05a20a00f913050b42"
}
```

## 🎨 前端集成

### 基础集成

将 `frontend/index.html` 部署到你的网站中，文件包含了完整的聊天界面。

### API 地址配置

在 `frontend/index.html` 中找到以下配置并修改：

```javascript
// 更新为你的后端服务地址
const apiUrl = 'http://your-domain.com:8000/myapi/v1/chat-bot/stream';
const botConfigurationUrl = 'http://your-domain.com:8000/myapi/v1/chat-bot-config';
const nonStreamApiUrl = 'http://your-domain.com:8000/myapi/v1/chat-bot';
```

### 自定义样式

聊天界面的样式可以通过修改 CSS 变量来自定义：

```css
:root {
    --chatbot-width: 350px;
    --chatbot-primary-color: #2B2A66;
    --chatbot-bg-color: #F1F1F1;
    /* 更多样式变量... */
}
```

## 🏗️ 项目架构

```
base-chatbot/
├── backend/                    # Python 后端
│   ├── app.py                 # Flask 主应用
│   ├── run.py                 # 应用启动入口
│   ├── test_config.py         # 配置测试脚本
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example          # 环境变量模板
│   ├── .env                  # 环境变量配置（需创建）
│   ├── start.bat             # Windows 启动脚本
│   ├── start.sh              # Unix/Linux 启动脚本
│   └── README.md             # 后端详细文档
├── frontend/                  # 前端界面
│   ├── index.html            # 完整的聊天界面（单文件）
│   └── 阿里云百炼api文档.txt  # API 参考文档
├── CLAUDE.md                  # Claude Code 助手指南
└── README.md                  # 本文档
```

## 🔧 高级配置

### 环境变量详解

| 变量名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `API_KEY` | String | ✅ | - | 阿里云 DashScope API Key |
| `APP_ID` | String | ✅ | - | 百炼智能体应用 ID |
| `HOST` | String | ❌ | 0.0.0.0 | 服务器绑定地址 |
| `PORT` | Integer | ❌ | 8000 | 服务器端口 |
| `DEBUG` | Boolean | ❌ | True | 调试模式开关 |
| `SYSTEM_PROMPT` | String | ❌ | 数字营销限制 | AI 系统提示词 |
| `TEMPERATURE` | Float | ❌ | 0.7 | AI 回复创造性 (0-1) |

### 自定义系统提示词

修改 `.env` 文件中的 `SYSTEM_PROMPT` 来定制 AI 的行为：

```env
# 示例：专业的客服助手
SYSTEM_PROMPT=你是一个专业的客服助手，请友好、耐心地回答用户问题，遇到无法回答的问题时建议联系人工客服。

# 示例：技术支持专家
SYSTEM_PROMPT=你是技术支持专家，专注于解决技术问题，提供准确的技术指导和解决方案。
```

### AI 创造性调节

通过 `TEMPERATURE` 参数控制 AI 回复的创造性：

- `0.0-0.3`: 更保守、准确的回复
- `0.4-0.7`: 平衡的回复（推荐）
- `0.8-1.0`: 更有创造性的回复

## 🚨 故障排除

### 常见问题及解决方案

#### 1. API 认证失败
**错误信息**: `Authentication failed`
**解决方案**:
```bash
# 检查 API Key 是否正确
python -c "import os; print('API Key:', os.getenv('API_KEY', 'Not set')[:20] + '...')"

# 确认使用的是 DashScope API Key，而不是其他阿里云服务的 Key
```

#### 2. 应用 ID 错误
**错误信息**: `App not found`
**解决方案**:
- 确认在百炼控制台中已创建应用
- 检查 `.env` 文件中的 `APP_ID` 是否正确复制

#### 3. 网络连接问题
**错误信息**: `Connection timeout`
**解决方案**:
```bash
# 测试网络连接
ping bailian.console.aliyun.com

# 检查防火墙设置，确保 8000 端口可访问
```

#### 4. 依赖安装失败
**解决方案**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 清除 pip 缓存
pip cache purge

# 重新安装
pip install -r requirements.txt
```

#### 5. 前端连接失败
**现象**: 前端无法连接后端服务
**解决方案**:
1. 检查后端服务是否正常启动
2. 确认前端代码中的 API 地址配置正确
3. 检查浏览器控制台的 CORS 错误信息

### 调试模式

启用调试模式获取更详细的日志信息：

```env
DEBUG=True
```

启动后将看到：
- 详细的请求/响应日志
- 错误堆栈信息
- API 调用详情

## 🔄 开发指南

### 添加新的 API 端点

1. 在 `app.py` 中添加新路由：
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    try:
        # 业务逻辑
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"新端点错误: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
```

2. 遵循现有的错误处理模式
3. 添加适当的日志记录
4. 更新 API 文档

### 自定义前端界面

1. 修改 `frontend/index.html` 中的样式变量
2. 添加新的 JavaScript 功能
3. 更新 API 调用逻辑
4. 测试在不同设备上的显示效果

### 部署到生产环境

1. **安全配置**:
   ```env
   DEBUG=False
   API_KEY=your-production-api-key
   ```

2. **使用 WSGI 服务器**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **配置反向代理** (Nginx):
   ```nginx
   location / {
       proxy_pass http://127.0.0.1:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

## 📊 性能优化

### 后端优化
- 使用 Gunicorn 或 uWSGI 部署生产环境
- 启用 Redis 缓存存储会话信息
- 配置适当的超时和重试机制

### 前端优化
- 启用 gzip 压缩
- 配置适当的缓存策略
- 优化图片和静态资源加载

## 📝 更新日志

### v1.0.0 (当前版本)
- ✅ 完成从 PHP 到 Python 的后端迁移
- ✅ 集成阿里云百炼 AI 服务
- ✅ 实现流式响应功能
- ✅ 添加自动回退机制
- ✅ 完善的错误处理和日志
- ✅ 提供完整的前端聊天界面
- ✅ 支持自定义配置和环境变量

### 计划中的功能
- 🔄 多语言支持
- 🔄 对话历史持久化
- 🔄 用户认证和权限管理
- 🔄 插件系统支持
- 🔄 高级分析面板

## 🤝 贡献指南

欢迎为项目做出贡献！

### 贡献流程
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 开发规范
- 遵循 PEP 8 Python 代码规范
- 添加适当的注释和文档字符串
- 确保所有测试通过
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙋‍♂️ 支持与反馈

### 获取帮助
- 📧 邮箱支持：[your-email@example.com]
- 💬 问题反馈：[GitHub Issues](https://github.com/your-username/your-repo/issues)
- 📖 文档：[项目 Wiki](https://github.com/your-username/your-repo/wiki)

### 常用链接
- [阿里云百炼控制台](https://bailian.console.aliyun.com/)
- [DashScope API 文档](https://help.aliyun.com/zh/model-studio/developer-reference/)
- [Flask 官方文档](https://flask.palletsprojects.com/)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！