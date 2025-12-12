#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bailian Chatbot Backend - 阿里云百炼集成
 使用Python + Flask + 阿里云百炼API
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()
from typing import Dict, List, Any, Generator
from dashscope import Application
from http import HTTPStatus
import dashscope


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS以支持前端调用

# 配置
class Config:
    # API配置 - 对应原来的config.php中的设置
    API_KEY = os.getenv('API_KEY')  # 对应原来的$api_key，不再提供默认值
    APP_ID = os.getenv('APP_ID', 'your-app-id-here')  # 阿里云百炼应用ID

    # 聊天配置
    SYSTEM_PROMPT = "Answer questions only related to digital marketing, otherwise, say I dont know"
    TEMPERATURE = 0.7

    # 对话配置
    CONVERSATION_ID = "beefb91df1fe41f99bd3a9c242f64ff8"  # 对应原来的conversation_id

    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 8000

    # 超时配置
    TIMEOUT = 120
    CONNECT_TIMEOUT = 30

# 初始化DashScope
dashscope.api_key = Config.API_KEY

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'Bailian-chatbot-backend',
        'version': '1.0.0'
    })

@app.route('/myapi/v1/chat-bot-config', methods=['GET'])
def get_chat_bot_config():
    """获取聊天机器人配置 - 替代Bailian的load_chat_bot_base_configuration函数"""
    try:
        # 这里可以从数据库或配置文件读取，现在使用硬编码
        config = {
            'botStatus': 0,  # 0: 离线, 1: 在线
            'StartUpMessage': "Hi, How are you?",
            'fontSize': '16',
            'userAvatarURL': "https://liangdabiao.com/wp-content/uploads/2025/06/a8a894b8b3e9259bb02ab0a7832372bb.png",
            'botImageURL': "https://liangdabiao.com/wp-content/uploads/2025/06/c892d890243984bb66f17f138412d5f4.png",
            'commonButtons': [
                {
                    'buttonText': 'I want your help!!!',
                    'buttonPrompt': 'I have a question about your courses'
                },
                {
                    'buttonText': 'I want a Discount',
                    'buttonPrompt': 'I want a discount'
                }
            ]
        }

        logger.info("返回聊天机器人配置")
        return jsonify(config)

    except Exception as e:
        logger.error(f"获取配置时出错: {str(e)}")
        return jsonify({
            'error': 'Failed to get configuration',
            'message': str(e)
        }), 500

@app.route('/myapi/v1/chat-bot/stream', methods=['POST'])
def chat_bot_stream():
    """流式聊天响应端点"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        last_prompt = data.get('last_prompt', '')
        conversation_history = data.get('conversation_history', [])
        session_id = data.get('session_id', None)
        session_id = data.get('session_id', None)

        if not last_prompt:
            return jsonify({
                'success': False,
                'message': 'last_prompt is required'
            }), 400

        logger.info(f"收到流式聊天请求: {last_prompt[:50]}...")

        # 验证API Key
        if not Config.API_KEY:
            return jsonify({
                'success': False,
                'message': 'API Key is not configured'
            }), 500

        # 构建消息历史 - 对应原来的config.php逻辑
        messages = []

        # 添加系统消息
        messages.append({
            'role': 'system',
            'content': Config.SYSTEM_PROMPT
        })

        # 添加历史对话
        for item in conversation_history:
            if isinstance(item, dict) and 'role' in item and 'content' in item:
                messages.append({
                    'role': item['role'],
                    'content': item['content']
                })

        # 添加当前用户消息
        messages.append({
            'role': 'user',
            'content': last_prompt
        })

        # 返回流式响应
        def generate_stream():
            try:
                # 调用阿里云百炼流式API
                response = Application.call(
                    api_key=Config.API_KEY,
                    app_id=Config.APP_ID,
                    messages=messages,  # 传递完整对话历史
                    session_id=session_id,  # 传递会话ID（如果有）
                    stream=True,  # 启用流式输出
                    incremental_output=True,  # 启用增量输出
                    temperature=Config.TEMPERATURE
                )

                # 处理流式响应
                for chunk in response:
                    if chunk.status_code != HTTPStatus.OK:
                        error_data = {
                            'success': False,
                            'message': f'API Error: {chunk.message}',
                            'code': chunk.status_code
                        }
                        yield f"data: {json.dumps(error_data)}\n\n"
                        break

                    # 发送流式数据
                    if chunk.output and chunk.output.text:
                        stream_data = {
                            'success': True,
                            'content': chunk.output.text,  # 只返回原始Markdown内容
                            'finished': False,
                            'session_id': getattr(chunk.output, 'session_id', None)
                        }
                        yield f"data: {json.dumps(stream_data)}\n\n"

                # 发送完成信号
                end_data = {
                    'success': True,
                    'finished': True,
                    'message': 'Stream completed'
                }
                yield f"data: {json.dumps(end_data)}\n\n"

            except Exception as e:
                logger.error(f"流式响应生成错误: {str(e)}")
                error_data = {
                    'success': False,
                    'message': f'Stream generation error: {str(e)}',
                    'finished': True
                }
                yield f"data: {json.dumps(error_data)}\n\n"

        return Response(
            generate_stream(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )

    except Exception as e:
        logger.error(f"流式聊天请求处理错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Request processing error: {str(e)}'
        }), 500

@app.route('/myapi/v1/chat-bot', methods=['POST'])
def chat_bot_non_stream():
    """非流式聊天响应端点（保持向后兼容）"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        last_prompt = data.get('last_prompt', '')
        conversation_history = data.get('conversation_history', [])

        if not last_prompt:
            return jsonify({
                'success': False,
                'message': 'last_prompt is required'
            }), 400

        logger.info(f"收到非流式聊天请求: {last_prompt[:50]}...")

        # 验证API Key
        if not Config.API_KEY:
            return jsonify({
                'success': False,
                'message': 'API Key is not configured'
            }), 500

        # 构建消息历史
        messages = []
        messages.append({
            'role': 'system',
            'content': Config.SYSTEM_PROMPT
        })

        for item in conversation_history:
            if isinstance(item, dict) and 'role' in item and 'content' in item:
                messages.append({
                    'role': item['role'],
                    'content': item['content']
                })

        messages.append({
            'role': 'user',
            'content': last_prompt
        })

        # 调用阿里云百炼API（非流式）
        response = Application.call(
            api_key=Config.API_KEY,
            app_id=Config.APP_ID,
            messages=messages,  # 传递完整对话历史
            session_id=session_id,  # 传递会话ID（如果有）
            temperature=Config.TEMPERATURE
        )

        if response.status_code != HTTPStatus.OK:
            logger.error(f"API调用失败: {response.message}")
            return jsonify({
                'success': False,
                'message': f'API Error: {response.message}',
                'result': ''
            })

        # 返回响应（只返回原始Markdown内容）
        result = {
            'success': True,
            'message': 'Response Generated',
            'result': response.output.text,  # 只返回原始Markdown内容
            'session_id': getattr(response.output, 'session_id', None)  # 返回会话ID
        }

        logger.info("成功生成非流式响应")
        return jsonify(result)

    except Exception as e:
        logger.error(f"聊天请求处理错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Request processing error: {str(e)}',
            'result': ''
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("启动Bailian聊天机器人后端服务...")
    logger.info(f"服务地址: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"阿里云百炼App ID: {Config.APP_ID}")

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=True,
        threaded=True
    )