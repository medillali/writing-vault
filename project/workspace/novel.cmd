@echo off
setlocal
set "NOVEL_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%NOVEL_PYTHON%" (
  "%NOVEL_PYTHON%" "%~dp0distill-novels\scripts\library.py" --vault "%~dp0writing-vault" %*
  exit /b
)
python "%~dp0distill-novels\scripts\library.py" --vault "%~dp0writing-vault" %*
exit /b
