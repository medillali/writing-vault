@echo off
setlocal
set TREE_DEPS=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies
set NODE_PATH=%TREE_DEPS%\node\node_modules
set VIZ_MODULE=%NODE_PATH%\@viz-js\viz
set PLOT_BROWSER_EXE=%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-1228\chrome-headless-shell-win64\chrome-headless-shell.exe
"%TREE_DEPS%\python\python.exe" -X utf8 "%~dp0rebuild.py" --prepare
if errorlevel 1 exit /b 1
"%TREE_DEPS%\node\bin\node.exe" "%~dp0layout.cjs"
if errorlevel 1 exit /b 1
"%TREE_DEPS%\python\python.exe" -X utf8 "%~dp0rebuild.py"
if errorlevel 1 exit /b 1
"%TREE_DEPS%\node\bin\node.exe" "%~dp0render.cjs"
if errorlevel 1 exit /b 1
"%TREE_DEPS%\python\python.exe" -X utf8 "%~dp0verify.py"
