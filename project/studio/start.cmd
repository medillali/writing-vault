@echo off
chcp 65001 >nul
setlocal
set "NOVEL_PY=python"
py -3 --version >nul 2>&1
if not errorlevel 1 set "NOVEL_PY=py -3"
%NOVEL_PY% -X utf8 "%~dp0launch.py"
if errorlevel 1 pause
