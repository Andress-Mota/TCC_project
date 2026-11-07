@echo off
echo Iniciando TCC - Classificacao de Imagens...
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
	echo ERRO: ambiente virtual nao encontrado em .venv\Scripts\python.exe
	pause
	exit /b 1
)

rem Mantem a janela aberta para que erros do backend fiquem visiveis.
start "TCC Backend" cmd /k ""%CD%\.venv\Scripts\python.exe" "%CD%\backend\app.py""
timeout /t 3 /nobreak >nul
start "" "http://localhost:5000"
