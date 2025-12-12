#!/bin/bash

echo "========================================"
echo "Bailian聊天机器人后端启动脚本"
echo "========================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查是否存在.env文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到.env文件"
    echo "请复制.env.example为.env并配置相关参数"
    echo ""
    read -p "按Enter继续，或Ctrl+C退出..."
fi

# 启动服务
echo "启动服务..."
python run.py