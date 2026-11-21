# earshot 을 내 PC 에 설치하고 Claude Code 에 연결하기

[earshot](https://github.com/Leonxlnx/earshot) 은 소리를 못 듣는 AI 코딩 에이전트에게 "귀"를 달아 주는 도구입니다.
소리 파일을 말로 설명해 주고, 효과음을 고르고, 영상 사운드 싱크·음량을 점검합니다. CPU 만으로 돌아갑니다.

## 가장 쉬운 방법 (Windows)

1. 이 폴더의 `install-earshot-windows.ps1` 을 PC 에 내려받습니다.
2. 시작 메뉴에서 **PowerShell** 을 열고, 파일이 있는 폴더로 이동한 뒤 아래 한 줄을 실행합니다.

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install-earshot-windows.ps1
   ```

3. 끝나면 Claude Code 를 껐다 켭니다.

스크립트가 하는 일 (README 순서 그대로):

| 단계 | 내용 |
|---|---|
| 1 | 파이썬 3.10 이상 확인, 없으면 Python 3.12 설치 (winget) |
| 2 | ffmpeg / git 확인, 없으면 설치 (winget) |
| 3 | `C:\Users\<내이름>\earshot` 에 저장소 받기 |
| 4 | `.venv` 가상환경 만들고 CPU 용 torch 설치 |
| 5 | `pip install -e ".[mcp,llm,dev]"` 로 earshot 설치 |
| 6 | `claude mcp add earshot --scope user ...` 로 **모든 프로젝트**에서 쓰도록 등록 + `skills/earshot`, `skills/real-sound` 를 `~/.claude/skills` 에 복사 |
| 7 | `earshot doctor` 로 점검 |

## 직접 한 줄씩 하고 싶다면 (Windows PowerShell)

```powershell
winget install -e --id Python.Python.3.12      # 파이썬이 없을 때만
winget install -e --id Gyan.FFmpeg             # ffmpeg 가 없을 때만
# (설치 후 PowerShell 창을 새로 여세요)

git clone https://github.com/Leonxlnx/earshot $HOME\earshot
cd $HOME\earshot
py -3 -m venv .venv
.venv\Scripts\python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv\Scripts\python -m pip install -e ".[mcp,llm,dev]"

claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- "$HOME\earshot\.venv\Scripts\python.exe" -m earshot mcp

mkdir $HOME\.claude\skills -Force
Copy-Item -Recurse -Force skills\earshot, skills\real-sound $HOME\.claude\skills

.venv\Scripts\python -m earshot doctor
```

## Mac 이라면 (터미널)

```bash
brew install python@3.12 ffmpeg git            # 없을 때만
git clone https://github.com/Leonxlnx/earshot ~/earshot && cd ~/earshot
python3 -m venv .venv
.venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -e ".[mcp,llm,dev]"
claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- ~/earshot/.venv/bin/python -m earshot mcp
mkdir -p ~/.claude/skills && cp -r skills/earshot skills/real-sound ~/.claude/skills/
.venv/bin/python -m earshot doctor
```

## 알아 두면 좋은 것

- **처음 쓸 때 모델 2개(약 1.1GB)를 내려받습니다.** 미리 받아 두려면 `.venv\Scripts\python -m earshot doctor --fetch`.
- 연결 확인: Claude Code 에서 `/mcp` 를 입력하면 `earshot` 이 보여야 합니다. 터미널에서는 `claude mcp list`.
- PC 가 느려 earshot 연결이 시간 초과되면 Claude Code 를 `MCP_TIMEOUT=60000` 환경변수와 함께 실행하세요.
- 업데이트: `cd $HOME\earshot; git pull; .venv\Scripts\python -m pip install -e ".[mcp,llm,dev]"`
