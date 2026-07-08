@echo off
setlocal
chcp 65001 >nul

set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

:menu
cls
echo ==========================================
echo        Game Sitemap Radar Launcher
echo ==========================================
echo.
echo  1. First-time setup / initialize database
echo  2. Run full radar scan
echo  3. Generate report only
echo  4. Export all known URLs to CSV
echo  5. Open reports folder
echo  6. Edit seed sites config
echo  7. Exit
echo.
set /p choice=Choose an option ^(1-7^): 

if "%choice%"=="1" goto init
if "%choice%"=="2" goto run
if "%choice%"=="3" goto report
if "%choice%"=="4" goto export
if "%choice%"=="5" goto outputs
if "%choice%"=="6" goto config
if "%choice%"=="7" goto end
goto menu

:init
call :run_python init
goto pause_menu

:run
call :run_python run
goto pause_menu

:report
call :run_python report
goto pause_menu

:export
call :run_python export
goto pause_menu

:outputs
if not exist "outputs" mkdir "outputs"
start "" "outputs"
goto menu

:config
if not exist "config\seeds.yaml" (
  python -m radar.cli init
)
notepad "config\seeds.yaml"
goto menu

:run_python
echo.
echo Running: python -m radar.cli %1
echo.
python -m radar.cli %1
if errorlevel 1 (
  echo.
  echo Command failed. If Python is missing, install Python 3.11+ and try again.
)
exit /b

:pause_menu
echo.
pause
goto menu

:end
endlocal

