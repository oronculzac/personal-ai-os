@echo off
REM Quick activation script for Skills & Cowork virtual environment

echo Activating Skills ^& Cowork virtual environment...
call .agent\.venv\Scripts\activate.bat

echo.
echo Virtual environment activated!
echo You can now run skills and tools.
echo.
echo Examples:
echo   python .agent\core\skill_discovery.py
echo   python .agent\core\persona_manager.py --list
echo.
echo To deactivate: deactivate
