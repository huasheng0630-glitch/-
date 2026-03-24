@echo off
REM 股票/加密货币新闻情感分析系统启动脚本（修复版）
REM 作者：自动生成
REM 日期：2026-03-14
REM 修复问题：支持中文路径，不使用activate.bat

chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 股票/加密货币新闻情感分析系统
echo ========================================
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"
echo 工作目录: %cd%
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo 警告: 未找到虚拟环境，正在创建...
    python -m venv venv
    if errorlevel 1 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 正在安装依赖包...
    call venv\Scripts\pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 安装依赖包失败
        pause
        exit /b 1
    )
)

REM 直接使用venv的python，避免activate.bat问题
echo 正在启动应用...
echo.
echo 服务器地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

REM 检查端口占用
netstat -ano | findstr :5000 >nul
if not errorlevel 1 (
    echo 警告: 端口5000已被占用！
    echo 请关闭占用端口的程序或等待5秒后继续...
    timeout /t 5 /nobreak >nul
)

REM 启动应用
echo 正在启动Flask服务器...
"venv\Scripts\python.exe" app.py

if errorlevel 1 (
    echo.
    echo 错误: 应用启动失败
    echo 请检查:
    echo 1. Python版本是否为3.8+
    echo 2. 依赖包是否安装完成
    echo 3. 配置文件是否正确
    pause
    exit /b 1
)