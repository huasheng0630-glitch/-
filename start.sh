#!/bin/bash
# 股票/加密货币新闻情感分析系统启动脚本
# 作者：自动生成
# 日期：2026-03-14

echo "========================================"
echo "股票/加密货币新闻情感分析系统"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查虚拟环境
if [ ! -f "venv/bin/python" ]; then
    echo "警告: 未找到虚拟环境，正在创建..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "错误: 创建虚拟环境失败"
        exit 1
    fi
    echo "正在安装依赖包..."
    source venv/bin/activate
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 安装依赖包失败"
        exit 1
    fi
    deactivate
fi

# 激活虚拟环境并运行应用
echo "正在启动应用..."
echo
echo "服务器地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务器"
echo "========================================"
echo

source venv/bin/activate
python app.py

if [ $? -ne 0 ]; then
    echo
    echo "错误: 应用启动失败"
    echo "请检查:"
    echo "1. Python版本是否为3.8+"
    echo "2. 依赖包是否安装完成"
    echo "3. 配置文件是否正确"
    exit 1
fi