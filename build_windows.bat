@echo off
REM Quick Build Script for Fee Tracker on Windows
REM This script builds a standalone .exe for Windows

echo ====================================
echo Fee Tracker - Windows Build
echo ====================================
echo.

REM Step 1: Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Step 2: Build the executable
echo.
echo Building Windows application...
.venv\Scripts\pyinstaller.exe fee_tracker_windows.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\FeeTracker.exe" (
    echo.
    echo Build failed. Check the output above for errors.
    exit /b 1
)

echo.
echo ====================================
echo BUILD COMPLETE!
echo ====================================
echo.
echo Outputs:
echo    - Executable: dist\FeeTracker.exe
echo.
echo Next steps:
echo    1. Test: dist\FeeTracker.exe
echo    2. Distribute the entire dist folder or create an installer
echo.
