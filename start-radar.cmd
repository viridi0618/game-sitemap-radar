@echo off
setlocal
chcp 65001 >nul

set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

:menu
cls
echo ==========================================
echo        游戏关键词雷达启动器
echo ==========================================
echo.
echo  1. 首次设置 / 初始化数据库
echo  2. 运行完整雷达扫描
echo  3. 只生成报告
echo  4. 导出所有已知 URL 到 CSV
echo  5. 打开报告文件夹
echo  6. 编辑种子站点配置
echo  7. 为候选游戏生成写作计划
echo  8. 为写作项目生成 brief
echo  9. 为写作项目生成草稿
echo 10. 检查草稿质量
echo 11. 导出写作任务清单
echo 12. 退出
echo.
set /p choice=请选择操作 ^(1-12^): 

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
set /p candidate=候选游戏名称: 
python -m radar.cli plan-writing --candidate "%candidate%" --force
goto pause_menu

:briefs
set /p project=写作项目 / 游戏名称: 
python -m radar.cli generate-briefs --project "%project%"
goto pause_menu

:drafts
set /p project=写作项目 / 游戏名称: 
python -m radar.cli generate-drafts --project "%project%"
goto pause_menu

:check_drafts
set /p project=写作项目 / 游戏名称: 
python -m radar.cli check-drafts --project "%project%"
goto pause_menu

:export_writing
set /p project=写作项目 / 游戏名称: 
python -m radar.cli export-writing --project "%project%"
goto pause_menu

:run_python
echo.
echo 正在运行: python -m radar.cli %1
echo.
python -m radar.cli %1
if errorlevel 1 (
  echo.
  echo 命令运行失败。如果没有安装 Python，请安装 Python 3.11+ 后再试。
)
exit /b

:pause_menu
echo.
pause
goto menu

:end
endlocal
