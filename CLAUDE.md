# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Bailian chatbot backend system that has been migrated from PHP to Python, integrated with Alibaba Cloud's Bailian AI service (阿里云百炼). The system provides a streaming API for real-time chat responses with a conversational AI interface.

## Architecture

### Backend (Python Flask)
- **Main Application**: `backend/app.py` - Flask server with streaming chat endpoints
- **Entry Point**: `backend/run.py` - Application launcher with environment validation
- **Configuration**: Environment variables via `.env` file (see `.env.example`)
- **Dependencies**: Flask, Flask-CORS, dashscope SDK, requests, python-dotenv

### Frontend (HTML/CSS/JavaScript)
- **Main Interface**: `frontend/index.html` - Complete chat UI with embedded styles and scripts
- **API Integration**: JavaScript handles streaming responses with fallback to non-streaming
- **Markdown Support**: Client-side markdown-to-HTML conversion for AI responses

## Common Development Commands

### Environment Setup
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Copy and configure environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your API_KEY and APP_ID
```

### Testing and Validation
```bash
# Test configuration and API connectivity
python backend/test_config.py
```

### Running the Application
```bash
# Start the development server
python backend/run.py

# Alternative: Direct Flask execution
cd backend && python app.py
```

### Platform-Specific Scripts
```bash
# Windows
backend/start.bat

# Unix/Linux
bash backend/start.sh
```

## Key API Endpoints

- **Health Check**: `GET /health` - Service status monitoring
- **Configuration**: `GET /myapi/v1/chat-bot-config` - Bot UI settings
- **Streaming Chat**: `POST /myapi/v1/chat-bot/stream` - Real-time streaming responses
- **Non-Streaming Chat**: `POST /myapi/v1/chat-bot` - Traditional request/response

## Configuration Requirements

### Environment Variables (.env file)
- `API_KEY`: Alibaba Cloud DashScope API key (required)
- `APP_ID`: Bailian application ID (required)
- `HOST`: Server bind address (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `SYSTEM_PROMPT`: AI behavior instructions (default: digital marketing focus)
- `TEMPERATURE`: AI response randomness (default: 0.7)

### Integration with Alibaba Cloud Bailian
The system uses the DashScope SDK to connect to Alibaba Cloud Bailian (百炼) AI service. Key features:

- **Streaming Responses**: Real-time text generation with incremental output
- **Session Management**: Optional session IDs for conversation context
- **Markdown Processing**: Frontend converts AI markdown responses to HTML
- **Error Handling**: Automatic fallback from streaming to non-streaming API calls

## Development Notes

### Backend Development
- The Flask app runs with threading enabled for concurrent requests
- CORS is configured for cross-origin frontend requests
- All API responses follow consistent JSON format with success/error status
- Stream responses use Server-Sent Events (SSE) format

### Frontend Integration
- The single HTML file contains complete UI, styling, and JavaScript logic
- API endpoints are configurable at the top of the JavaScript section
- Streaming implementation includes typing animation and real-time content updates
- Built-in error handling with popup notifications

### Testing Configuration
Always run `test_config.py` before starting development to verify:
- Environment variables are properly set
- API connectivity to Alibaba Cloud services
- Application configuration validity

## File Structure
```
base-chatbot/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── run.py              # Application entry point
│   ├── test_config.py      # Configuration validation
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   ├── .env               # Actual environment (create from example)
│   ├── start.bat          # Windows startup script
│   └── start.sh           # Unix startup script
├── frontend/
│   ├── index.html          # Complete chat interface
│   └── 阿里云百炼api文档.txt  # API documentation
└── CLAUDE.md              # This file
```

## Important Notes

- The system migrated from Bailian PHP backend to Python Flask for better performance and AI integration
- API keys should never be committed to version control - always use environment variables
- The frontend expects the backend to run on `http://127.0.0.1:8000` by default
- Streaming responses provide better user experience but include automatic fallback to ensure reliability