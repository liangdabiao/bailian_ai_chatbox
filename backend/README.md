# Chatbot Backend - 阿里云百炼版

这是 聊天机器人的Python后端版本，集成阿里云百炼API，支持流式响应。

## 🚀 功能特性

- ✅ **流式响应**: 实时显示AI回复，提升用户体验
- ✅ **向后兼容**: 支持非流式API作为回退方案
- ✅ **阿里云百炼集成**: 使用先进的通义千问模型
- ✅ **REST API**: 标准的RESTful接口设计
- ✅ **错误处理**: 完善的错误处理和日志记录
- ✅ **CORS支持**: 支持跨域请求
- ✅ **健康检查**: 内置健康检查端点
- ✅ **配置化**: 通过环境变量进行配置

## 📋 系统要求

- Python 3.7+
- 阿里云百炼服务账号
- 有效的DashScope API Key和应用ID

## 🛠️ 快速开始

### 1. 克隆项目并进入后端目录

```bash
cd backend
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 阿里云百炼配置
DASHSCOPE_API_KEY=sk-your-dashscope-api-key-here
APP_ID=your-bailian-app-id-here

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True

# 聊天配置
SYSTEM_PROMPT=Answer questions only related to digital marketing, otherwise, say I dont know
TEMPERATURE=0.7
```

### 5. 启动服务

#### 使用启动脚本（推荐）

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### 手动启动
```bash
python run.py
```

### 6. 验证服务

访问健康检查端点：
```
http://localhost:8000/health
```

## 📡 API 端点

### 1. 健康检查
```
GET /health
```

### 2. 获取聊天机器人配置
```
GET /myapi/v1/chat-bot-config
```

### 3. 流式聊天（主要接口）
```
POST /myapi/v1/chat-bot/stream
Content-Type: application/json

{
    "last_prompt": "用户的消息",
    "conversation_history": [
        {"role": "user", "content": "历史消息1"},
        {"role": "assistant", "content": "历史回复1"}
    ]
}
```

### 4. 非流式聊天（回退接口）
```
POST /myapi/v1/chat-bot
Content-Type: application/json

{
    "last_prompt": "用户的消息",
    "conversation_history": [
        {"role": "user", "content": "历史消息1"},
        {"role": "assistant", "content": "历史回复1"}
    ]
}
```

## 🌐 前端集成

更新前端的API调用地址：

```javascript
// 流式API（主要使用）
const apiUrl = 'http://localhost:8000/myapi/v1/chat-bot/stream';
const botConfigurationUrl = 'http://localhost:8000/myapi/v1/chat-bot-config';

// 非流式API（回退使用）
const nonStreamApiUrl = 'http://localhost:8000/myapi/v1/chat-bot';
```

## 📁 项目结构

```
backend/
├── app.py              # 主应用文件
├── run.py              # 启动脚本
├── requirements.txt    # Python依赖
├── .env.example        # 环境变量示例
├── start.bat          # Windows启动脚本
├── start.sh           # Linux/Mac启动脚本
└── README.md          # 本文档
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `API_KEY` | API密钥（对应原来config.php中的$api_key） | `sk-0E` |
| `APP_ID` | 百炼应用ID | - |
| `HOST` | 服务器绑定地址 | `0.0.0.0` |
| `PORT` | 服务器端口 | `8000` |
| `DEBUG` | 调试模式 | `True` |
| `SYSTEM_PROMPT` | 系统提示词 | 数字营销相关限制 |
| `TEMPERATURE` | AI回复创造性（0-1） | `0.7` |

### 获取阿里云百炼凭证

1. 登录[阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 获取API Key：密钥管理页面（注意：这是DashScope API Key）
3. 获取App ID：应用管理页面

## 🚨 错误处理

### 常见错误及解决方案

1. **API Key错误**
   ```
   错误: Authentication failed
   解决: 检查API_KEY是否正确，确保使用阿里云DashScope API Key
   ```

2. **App ID错误**
   ```
   错误: App not found
   解决: 检查APP_ID是否正确
   ```

3. **网络连接问题**
   ```
   错误: Connection timeout
   解决: 检查网络连接和防火墙设置
   ```

4. **依赖包安装失败**
   ```
   解决: 使用 pip install --upgrade pip 升级pip
   ```

## 🔄 开发说明

### 添加新功能

1. 在 `app.py` 中添加新的路由处理函数
2. 使用Flask的 `@app.route()` 装饰器
3. 遵循现有的错误处理模式
4. 添加适当的日志记录

### 自定义系统提示词

修改 `.env` 文件中的 `SYSTEM_PROMPT` 或直接在 `app.py` 中修改 `Config.SYSTEM_PROMPT`。

### 调试模式

设置 `DEBUG=True` 可以看到详细的错误信息和请求日志。

## 📝 更新日志

### v1.0.0
- ✅ 初始版本发布
- ✅ 阿里云百炼API集成
- ✅ 流式响应支持
- ✅ 完整的REST API
- ✅ 错误处理和日志

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

本项目采用MIT许可证。