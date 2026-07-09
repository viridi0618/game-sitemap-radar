$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $AppDir

function Invoke-RadarCommand {
    param([Parameter(Mandatory = $true)][string[]]$ArgsList)

    Write-Host ""
    Write-Host ("正在运行: python -m radar.cli " + ($ArgsList -join " "))
    Write-Host ""
    & python -m radar.cli @ArgsList
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "命令运行失败。如果没有安装 Python，请安装 Python 3.11+ 后再试。"
    }
}

function Pause-Menu {
    Write-Host ""
    Read-Host "按 Enter 返回菜单"
}

while ($true) {
    Clear-Host
    Write-Host "=========================================="
    Write-Host "       游戏关键词雷达启动器"
    Write-Host "=========================================="
    Write-Host ""
    Write-Host "  1. 首次设置 / 初始化数据库"
    Write-Host "  2. 导入 Roblox 榜单 CSV"
    Write-Host "  3. 尝试在线抓取 Roblox 榜单（实验）"
    Write-Host "  4. 生成 Roblox 报告"
    Write-Host "  5. 运行 Sitemap 雷达扫描"
    Write-Host "  6. 生成 Sitemap 报告"
    Write-Host "  7. 生成 Fusion 综合报告"
    Write-Host "  8. 导出所有已知 URL 到 CSV"
    Write-Host "  9. 打开报告文件夹"
    Write-Host " 10. 编辑种子站点配置"
    Write-Host " 11. 为候选游戏生成写作计划"
    Write-Host " 12. 为写作项目生成 brief"
    Write-Host " 13. 为写作项目生成草稿"
    Write-Host " 14. 检查草稿质量"
    Write-Host " 15. 导出写作任务清单"
    Write-Host " 16. 退出"
    Write-Host ""

    $choice = Read-Host "请选择操作 (1-16)"

    switch ($choice) {
        "1" {
            Invoke-RadarCommand @("init")
            Pause-Menu
        }
        "2" {
            $csvPath = Read-Host "Roblox CSV 路径（直接回车使用 data\roblox-chart.csv）"
            if (-not $csvPath.Trim()) {
                $csvPath = "data\roblox-chart.csv"
            }
            Invoke-RadarCommand @("import-roblox-chart", "--csv", $csvPath)
            Pause-Menu
        }
        "3" {
            Write-Host "Roblox 在线榜单接口可能失效，失败时请改用 CSV 导入。"
            Invoke-RadarCommand @("roblox-snapshot")
            Pause-Menu
        }
        "4" {
            Invoke-RadarCommand @("roblox-report")
            Pause-Menu
        }
        "5" {
            Invoke-RadarCommand @("run")
            Pause-Menu
        }
        "6" {
            Invoke-RadarCommand @("report")
            Pause-Menu
        }
        "7" {
            Invoke-RadarCommand @("fusion-report")
            Pause-Menu
        }
        "8" {
            Invoke-RadarCommand @("export")
            Pause-Menu
        }
        "9" {
            if (-not (Test-Path "outputs")) {
                New-Item -ItemType Directory -Path "outputs" | Out-Null
            }
            Start-Process "outputs"
        }
        "10" {
            if (-not (Test-Path "config\seeds.yaml")) {
                & python -m radar.cli init
            }
            Start-Process notepad "config\seeds.yaml"
        }
        "11" {
            $candidate = Read-Host "候选游戏名称"
            if ($candidate.Trim()) {
                Invoke-RadarCommand @("plan-writing", "--candidate", $candidate, "--force")
            }
            Pause-Menu
        }
        "12" {
            $project = Read-Host "写作项目 / 游戏名称"
            if ($project.Trim()) {
                Invoke-RadarCommand @("generate-briefs", "--project", $project)
            }
            Pause-Menu
        }
        "13" {
            $project = Read-Host "写作项目 / 游戏名称"
            if ($project.Trim()) {
                Invoke-RadarCommand @("generate-drafts", "--project", $project)
            }
            Pause-Menu
        }
        "14" {
            $project = Read-Host "写作项目 / 游戏名称"
            if ($project.Trim()) {
                Invoke-RadarCommand @("check-drafts", "--project", $project)
            }
            Pause-Menu
        }
        "15" {
            $project = Read-Host "写作项目 / 游戏名称"
            if ($project.Trim()) {
                Invoke-RadarCommand @("export-writing", "--project", $project)
            }
            Pause-Menu
        }
        "16" {
            break
        }
        default {
            Write-Host "无效选择，请输入 1-16。"
            Pause-Menu
        }
    }
}

