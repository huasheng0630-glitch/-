@echo off
REM 股票/加密货币新闻情感分析系统诊断脚本（修复版）
REM 作者：自动生成
REM 日期：2026-03-14
REM 修复问题：支持中文路径，简化命令

chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 系统诊断脚本（修复版）
echo ========================================
echo 开始时间: %date% %time%
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"
set "LOG_FILE=diagnose_log.txt"
echo 工作目录: %cd%
echo 诊断日志: %LOG_FILE%
echo.

REM 清空并开始记录日志
echo ===== 诊断报告 %date% %time% ===== > %LOG_FILE%
echo 工作目录: %cd% >> %LOG_FILE%
echo. >> %LOG_FILE%

REM 1. 检查Python
echo 1. 检查Python安装...
echo 1. 检查Python安装... >> %LOG_FILE%
python --version 2>> %LOG_FILE%
if errorlevel 1 (
    echo 错误: Python未安装或不在PATH中 >> %LOG_FILE%
    echo 错误: Python未安装或不在PATH中
    goto :error
) else (
    python --version 2>nul && (python --version >> %LOG_FILE% && echo Python已安装 >> %LOG_FILE%)
    echo Python已安装
)

REM 2. 检查项目目录
echo.
echo 2. 检查项目目录结构...
echo. >> %LOG_FILE%
echo 2. 检查项目目录结构... >> %LOG_FILE%
dir /b >> %LOG_FILE%

REM 3. 检查虚拟环境
echo.
echo 3. 检查虚拟环境...
echo. >> %LOG_FILE%
echo 3. 检查虚拟环境... >> %LOG_FILE%
if exist "venv\Scripts\python.exe" (
    echo 虚拟环境已存在 >> %LOG_FILE%
    echo 虚拟环境已存在
    "venv\Scripts\python.exe" --version >> %LOG_FILE% 2>&1
) else (
    echo 虚拟环境不存在 >> %LOG_FILE%
    echo 虚拟环境不存在
)

REM 4. 检查依赖包
echo.
echo 4. 检查依赖包...
echo. >> %LOG_FILE%
echo 4. 检查依赖包... >> %LOG_FILE%
if exist "venv\Scripts\pip.exe" (
    echo 检查已安装的包... >> %LOG_FILE%
    "venv\Scripts\pip.exe" freeze >> %LOG_FILE% 2>&1
    echo 依赖包列表已保存到日志
) else (
    echo pip未找到 >> %LOG_FILE%
    echo pip未找到
)

REM 5. 测试Python模块导入（简化）
echo.
echo 5. 测试Python模块导入...
echo. >> %LOG_FILE%
echo 5. 测试Python模块导入... >> %LOG_FILE%

echo 测试Flask... >> %LOG_FILE%
"venv\Scripts\python.exe" -c "import flask; print('Flask导入成功')" >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo Flask导入失败 >> %LOG_FILE%
    echo Flask导入失败
) else (
    echo Flask导入成功 >> %LOG_FILE%
    echo Flask导入成功
)

echo 测试requests... >> %LOG_FILE%
"venv\Scripts\python.exe" -c "import requests; print('requests导入成功')" >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo requests导入失败 >> %LOG_FILE%
    echo requests导入失败
) else (
    echo requests导入成功 >> %LOG_FILE%
    echo requests导入成功
)

echo 测试textblob... >> %LOG_FILE%
"venv\Scripts\python.exe" -c "import textblob; print('textblob导入成功')" >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo textblob导入失败 >> %LOG_FILE%
    echo textblob导入失败
) else (
    echo textblob导入成功 >> %LOG_FILE%
    echo textblob导入成功
)

REM 6. 测试应用导入
echo.
echo 6. 测试应用导入...
echo. >> %LOG_FILE%
echo 6. 测试应用导入... >> %LOG_FILE%
"venv\Scripts\python.exe" -c "
try:
    from app import app
    print('应用导入成功')
except Exception as e:
    print('应用导入失败:', str(e))
" >> %LOG_FILE% 2>&1

if errorlevel 1 (
    echo 应用导入失败 >> %LOG_FILE%
    echo 应用导入失败
) else (
    echo 应用导入成功 >> %LOG_FILE%
    echo 应用导入成功
)

REM 7. 检查端口占用
echo.
echo 7. 检查端口5000占用...
echo. >> %LOG_FILE%
echo 7. 检查端口5000占用... >> %LOG_FILE%
netstat -ano | findstr :5000 >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo 端口5000未被占用 >> %LOG_FILE%
    echo 端口5000未被占用
) else (
    echo 端口5000已被占用 >> %LOG_FILE%
    echo 端口5000已被占用
)

REM 8. 快速启动测试（5秒）
echo.
echo 8. 快速启动测试（5秒）...
echo. >> %LOG_FILE%
echo 8. 快速启动测试（5秒）... >> %LOG_FILE%
echo 启动应用（5秒后停止）... >> %LOG_FILE%
start /B "测试应用" "venv\Scripts\python.exe" app.py
timeout /t 5 /nobreak >nul
taskkill /F /IM python.exe >nul 2>&1
echo 快速启动测试完成 >> %LOG_FILE%
echo 快速启动测试完成

REM 完成
echo.
echo ========================================
echo 诊断完成
echo 详细日志已保存到: %LOG_FILE%
echo 请将此文件内容发送给技术支持
echo ========================================

echo 按任意键打开日志文件...
pause >nul
start notepad %LOG_FILE%
exit /b 0

:error
echo.
echo ========================================
echo 诊断发现错误
echo 详细日志已保存到: %LOG_FILE%
echo 请将此文件内容发送给技术支持
echo ========================================
echo 按任意键打开日志文件...
pause >nul
start notepad %LOG_FILE%
exit /b 1