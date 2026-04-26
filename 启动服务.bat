@echo off
echo ====================================
echo   大众生活 - 本地生活服务平台
echo ====================================
echo.
cd /d "%~dp0"

echo [1/3] 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
python -c "import fastapi, uvicorn, sqlalchemy" 2>nul
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
)

echo.
echo [3/3] 启动服务器...
echo ====================================
echo 服务即将启动，请稍候...
echo 启动成功后，请在浏览器中访问: http://localhost:8000
echo 按 Ctrl+C 可以停止服务
echo ====================================
echo.

uvicorn backend.main:app --reload

pause
