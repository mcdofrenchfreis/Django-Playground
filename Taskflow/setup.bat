@echo off
REM Setup script for Django Todo App on Windows

echo ============================================
echo   Django Todo List App - Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully

echo.
echo [2/5] Running migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to run migrations
    pause
    exit /b 1
)
echo ✓ Migrations applied successfully

echo.
echo [3/5] Collecting static files...
python manage.py collectstatic --noinput >nul 2>&1
echo ✓ Static files collected

echo.
echo [4/5] Creating superuser...
echo Please enter superuser credentials:
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo Error: Failed to create superuser
    pause
    exit /b 1
)
echo ✓ Superuser created successfully

echo.
echo [5/5] Setup complete!
echo.
echo ============================================
echo   Next Steps:
echo ============================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then open your browser and go to:
echo   http://127.0.0.1:8000/
echo.
echo Admin panel (after creating superuser):
echo   http://127.0.0.1:8000/admin/
echo.
echo ============================================
pause
