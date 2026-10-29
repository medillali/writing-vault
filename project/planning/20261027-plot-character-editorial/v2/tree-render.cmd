@echo off
setlocal
set NODE_PATH=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules
set PLOT_BROWSER_EXE=%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-1228\chrome-headless-shell-win64\chrome-headless-shell.exe
"%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" writing-vault\library\reports\zongheng-tianxia\atlas\tree\render.cjs
