@echo off
setlocal
set NODE_PATH=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules
set VIZ_MODULE=%NODE_PATH%\@viz-js\viz
"%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" writing-vault\library\reports\zongheng-tianxia\atlas\tree\layout.cjs
