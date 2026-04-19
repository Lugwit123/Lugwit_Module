@echo off
echo Testing build process...
echo Current directory: %CD%
echo.

echo Changing to script directory...
cd /d "%~dp0"
echo New directory: %CD%
echo.

echo Listing Python files:
dir /b *.py
echo.

echo Running rez-build...
rez-build --install

echo.
echo Build completed with exit code: %ERRORLEVEL%
pause
