@echo off
REM ============================================================================
REM upload_to_gitee.bat
REM Purpose: Add, commit, and push Lugwit_Module to Gitee repository
REM Usage: Double-click this file or run from command line in Lugwit_Module dir
REM Note: Requires Git installed and PATH configured
REM ============================================================================

setlocal enabledelayedexpansion

REM ---------- Configuration ----------
set REPO_DIR=%~dp0
set BRANCH=main
set REMOTE=origin
set GITEE_URL=https://gitee.com/lugwit123/Lugwit_Module

echo.
echo === Lugwit Module Upload to Gitee ===
echo Repository: %REPO_DIR%
echo Branch: %BRANCH%
echo Remote: %REMOTE%
echo Gitee URL: %GITEE_URL%
echo.

REM ---------- Check if Git is installed ----------
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found in PATH. Please install Git first.
    echo Visit: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM ---------- Navigate to repo directory ----------
cd /d "%REPO_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to change to directory: %REPO_DIR%
    pause
    exit /b 1
)

REM ---------- Check if this is a git repository ----------
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [INFO] Not a git repository. Initializing...
    git init
    if errorlevel 1 (
        echo [ERROR] Failed to initialize git repository.
        pause
        exit /b 1
    )
)

REM ---------- Check and set remote URL ----------
echo [INFO] Checking remote repository...
git remote get-url %REMOTE% >nul 2>&1
if errorlevel 1 (
    echo [INFO] Remote '%REMOTE%' not found. Adding remote...
    git remote add %REMOTE% %GITEE_URL%
    if errorlevel 1 (
        echo [ERROR] Failed to add remote repository.
        pause
        exit /b 1
    )
    echo [INFO] Remote '%REMOTE%' added: %GITEE_URL%
) else (
    for /f "tokens=*" %%i in ('git remote get-url %REMOTE%') do set CURRENT_URL=%%i
    if not "!CURRENT_URL!"=="%GITEE_URL%" (
        echo [INFO] Updating remote URL from !CURRENT_URL! to %GITEE_URL%
        git remote set-url %REMOTE% %GITEE_URL%
        if errorlevel 1 (
            echo [ERROR] Failed to update remote URL.
            pause
            exit /b 1
        )
    ) else (
        echo [INFO] Remote URL is correct: %GITEE_URL%
    )
)
echo.

REM ---------- Show current status ----------
echo [INFO] Current branch:
git rev-parse --abbrev-ref HEAD
echo.

REM ---------- Stage all changes ----------
echo [INFO] Staging changes...
git add -A
if errorlevel 1 (
    echo [ERROR] Failed to stage changes.
    pause
    exit /b 1
)

REM ---------- Check if there are changes to commit ----------
git diff --cached --quiet >nul 2>&1
if not errorlevel 1 (
    echo [INFO] No changes to commit.
    goto :push
)

REM ---------- Commit changes ----------
echo.
set /p COMMIT_MSG="[INPUT] Enter commit message (leave empty for default): "
if "!COMMIT_MSG!"=="" (
    set COMMIT_MSG=Auto update Lugwit_Module
)

echo [INFO] Committing with message: !COMMIT_MSG!
git commit -m "!COMMIT_MSG!"
if errorlevel 1 (
    echo [ERROR] Failed to commit changes.
    pause
    exit /b 1
)
echo [INFO] Changes committed successfully.
echo.

:push
REM ---------- Push to remote ----------
echo [INFO] Pushing to %REMOTE%/%BRANCH%...
git push -u %REMOTE% %BRANCH%
if errorlevel 1 (
    echo [ERROR] Failed to push. Check:
    echo   - Network connection
    echo   - Remote URL: git remote -v
    echo   - Credentials/SSH key or access token
    echo   - Branch name: %BRANCH%
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Push completed successfully!
echo.
pause
endlocal
exit /b 0
