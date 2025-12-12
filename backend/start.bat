@echo off
echo ========================================
echo Bailian聊天机器人后端启动脚本
echo ========================================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt

REM 检查是否存在.env文件
if not exist ".env" (
    echo 警告: 未找到.env文件
    echo 请复制.env.example为.env并配置相关参数
    echo.
    pause
)

REM 启动服务
echo 启动服务...
python run.py

pause