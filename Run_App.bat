@echo off
title Kartini AI Server
set CURRENT_DIR=%~dp0
cd /d %CURRENT_DIR%

echo ==============================================
echo       SEDANG MENJALANKAN KARTINI AI
echo ==============================================
echo 1. Membuka Browser ke http://127.0.0.1:5000
echo 2. Menjalankan Flask Server...
echo ==============================================

:: Membuka browser secara otomatis
start http://127.0.0.1:5000

:: Menjalankan python dari virtual environment
.venv\Scripts\python.exe app.py

pause
