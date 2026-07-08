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
echo  7. Plan writing for a candidate
echo  8. Generate briefs for a project
echo  9. Generate drafts for a project
echo 10. Check drafts for a project
echo 11. Export writing task list
echo 12. Exit
echo.
set /p choice=Choose an option ^(1-12^): 

if "%choice%"=="1" goto init
if "%choice%"=="2" goto run
if "%choice%"=="3" goto report
if "%choice%"=="4" goto export
if "%choice%"=="5" goto outputs
if "%choice%"=="6" goto config
if "%choice%"=="7" goto plan_writing
if "%choice%"=="8" goto briefs
if "%choice%"=="9" goto drafts
if "%choice%"=="10" goto check_drafts
if "%choice%"=="11" goto export_writing
if "%choice%"=="12" goto end
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

:plan_writing
set /p candidate=Candidate game name: 
python -m radar.cli plan-writing --candidate "%candidate%" --force
goto pause_menu

:briefs
set /p project=Project game name: 
python -m radar.cli generate-briefs --project "%project%"
goto pause_menu

:drafts
set /p project=Project game name: 
python -m radar.cli generate-drafts --project "%project%"
goto pause_menu

:check_drafts
set /p project=Project game name: 
python -m radar.cli check-drafts --project "%project%"
goto pause_menu

:export_writing
set /p project=Project game name: 
python -m radar.cli export-writing --project "%project%"
goto pause_menu

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
