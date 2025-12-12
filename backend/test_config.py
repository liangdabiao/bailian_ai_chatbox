#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置测试脚本
用于验证环境变量和API连接是否正确
"""

import os
import sys
from dotenv import load_dotenv
from app import Config, dashscope

def test_environment():
    """测试环境变量"""
    print("🔧 检查环境变量配置...")

    load_dotenv()

    # 检查API_KEY
    api_key = os.getenv('API_KEY', Config.API_KEY)
    if api_key == 'sk-your-api-key-here':
        print("❌ API_KEY 未配置，请在 .env 文件中设置正确的阿里云DashScope API Key")
        return False
    else:
        print(f"✅ API_KEY: {api_key[:10]}...")

    # 检查APP_ID
    app_id = os.getenv('APP_ID', Config.APP_ID)
    if app_id == 'your-app-id-here':
        print("❌ APP_ID 未配置，请在 .env 文件中设置正确的百炼应用ID")
        return False
    else:
        print(f"✅ APP_ID: {app_id}")

    return True

def test_api_connection():
    """测试API连接"""
    print("\n🔗 测试阿里云百炼API连接...")

    try:
        from dashscope import Application
        from http import HTTPStatus

        # 简单的测试请求
        response = Application.call(
            api_key=Config.API_KEY,
            app_id=Config.APP_ID,
            prompt='你好，请回复"测试成功"',
            temperature=0.1
        )

        if response.status_code == HTTPStatus.OK:
            print("✅ API连接成功")
            print(f"📝 测试回复: {response.output.text[:50]}...")
            return True
        else:
            print(f"❌ API连接失败: {response.message}")
            return False

    except Exception as e:
        print(f"❌ API连接异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 Bailian聊天机器人后端配置测试")
    print("=" * 50)

    # 测试环境变量
    if not test_environment():
        print("\n❌ 环境变量配置有误，请检查 .env 文件")
        sys.exit(1)

    # 测试API连接
    if not test_api_connection():
        print("\n❌ API连接失败，请检查网络和凭证")
        sys.exit(1)

    print("\n🎉 所有测试通过！可以启动服务了")
    print("\n启动命令: python run.py")

if __name__ == '__main__':
    main()