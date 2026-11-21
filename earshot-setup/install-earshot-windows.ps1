# earshot 설치 + Claude Code 연결 스크립트 (Windows)
# 실행 방법: PowerShell 을 열고 이 파일이 있는 폴더에서
#   powershell -ExecutionPolicy Bypass -File .\install-earshot-windows.ps1
# README 의 "install from a clone" 순서를 그대로 따릅니다.

$ErrorActionPreference = 'Stop'
$Repo   = 'https://github.com/Leonxlnx/earshot'
$Target = Join-Path $HOME 'earshot'
$Skills = Join-Path $HOME '.claude\skills'

function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path', 'User')
}
function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Check($what) { if ($LASTEXITCODE -ne 0) { throw "$what 실패 (exit $LASTEXITCODE)" } }

# 파이썬 3.10 이상 찾기: py 런처 -> python 순서. 찾으면 실행 파일 경로를 돌려줌
function Find-Python {
    $probe = 'import sys; print(sys.executable if sys.version_info >= (3, 10) else "")'
    $found = $null
    $old = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try {
        if (Have 'py')     { $found = (& py -3 -c $probe 2>$null | Select-Object -Last 1) }
        if (-not $found -and (Have 'python')) { $found = (& python -c $probe 2>$null | Select-Object -Last 1) }
    } catch { $found = $null }
    $ErrorActionPreference = $old
    if ($found -and (Test-Path $found)) { return $found }
    return $null
}

Step '1/7 파이썬 3.10+ 확인'
$pyExe = Find-Python
if (-not $pyExe) {
    Write-Host '파이썬 3.10 이상이 없어 Python 3.12 를 설치합니다 (winget).'
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    Refresh-Path
    $pyExe = Find-Python
    if (-not $pyExe) { throw '파이썬 설치 후에도 찾지 못했습니다. PowerShell 을 새로 열고 다시 실행해 주세요.' }
}
& $pyExe --version

Step '2/7 ffmpeg / git 확인'
if (-not (Have 'ffmpeg') -or -not (Have 'ffprobe')) {
    Write-Host 'ffmpeg 가 없어 설치합니다 (winget, Gyan.FFmpeg).'
    winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
    Refresh-Path
}
if (-not (Have 'git')) {
    Write-Host 'git 이 없어 설치합니다 (winget).'
    winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements
    Refresh-Path
}
if (-not (Have 'ffmpeg')) { throw 'ffmpeg 를 찾지 못했습니다. PowerShell 을 새로 열고 다시 실행해 주세요.' }
if (-not (Have 'git'))    { throw 'git 을 찾지 못했습니다. PowerShell 을 새로 열고 다시 실행해 주세요.' }
ffmpeg -hide_banner -version | Select-Object -First 1

Step "3/7 저장소 받기 -> $Target"
if (Test-Path (Join-Path $Target '.git')) {
    git -C $Target pull --ff-only; Check 'git pull'
} else {
    git clone $Repo $Target; Check 'git clone'
}
Set-Location $Target

Step '4/7 가상환경 만들기 + CPU 용 torch 설치'
$venvPy = Join-Path $Target '.venv\Scripts\python.exe'
if (-not (Test-Path $venvPy)) { & $pyExe -m venv .venv; Check 'venv 생성' }
& $venvPy -m pip install --upgrade pip; Check 'pip 업그레이드'
& $venvPy -m pip install torch --index-url https://download.pytorch.org/whl/cpu; Check 'torch(CPU) 설치'

Step '5/7 earshot 설치'
& $venvPy -m pip install -e ".[mcp,llm,dev]"; Check 'earshot 설치'

Step '6/7 Claude Code 에 MCP 등록 (모든 프로젝트, --scope user) + 스킬 복사'
if (Have 'claude') {
    $old = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try { claude mcp remove earshot --scope user *> $null } catch { }   # 예전 등록이 있으면 지움
    $ErrorActionPreference = $old
    claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- $venvPy -m earshot mcp; Check 'MCP 등록'
    claude mcp get earshot
} else {
    Write-Warning 'claude 명령을 찾지 못해 MCP 등록을 건너뜁니다. Claude Code 설치 후 아래 줄을 실행하세요:'
    Write-Host "  claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- `"$venvPy`" -m earshot mcp"
}
New-Item -ItemType Directory -Force -Path $Skills | Out-Null
Copy-Item -Recurse -Force (Join-Path $Target 'skills\earshot')    $Skills
Copy-Item -Recurse -Force (Join-Path $Target 'skills\real-sound') $Skills
Get-ChildItem $Skills | Select-Object Name

Step '7/7 earshot doctor 점검'
& $venvPy -m earshot doctor

Write-Host "`n끝났습니다. Claude Code 를 다시 시작하면 earshot 도구와 스킬을 쓸 수 있습니다." -ForegroundColor Green
Write-Host '모델(약 1.1GB)을 미리 받아 두려면 아래 줄을 실행하세요:'
Write-Host "  & `"$venvPy`" -m earshot doctor --fetch"
