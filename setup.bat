@echo off
REM Script de Setup para Windows
REM iPrevencion - Automatic Setup

setlocal enabledelayedexpansion

echo.
echo ================================
echo 🚀 iPrevencion - Setup para Windows
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Descárgalo de: https://www.python.org
    exit /b 1
)
echo ✅ Python encontrado

REM Create Backend venv
echo.
echo Configurando Backend...
cd backend
if not exist venv (
    python -m venv venv
    echo ✅ VI virtual environment Backend creado
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Dependencias Backend instaladas

if not exist .env (
    copy .env.example .env
    echo ✅ .env Backend creado
    echo.
    echo ⚠️  Edita backend\.env y agrega:
    echo.
    echo    GEMINI_API_KEY=tu-key-aqui
    echo    DATABASE_URL=postgresql://postgres:password@localhost:5432/iprevencion
    echo.
)

call venv\Scripts\deactivate.bat
cd ..

REM Create Frontend venv
echo.
echo Configurando Frontend...
cd frontend
if not exist venv (
    python -m venv venv
    echo ✅ Virtual environment Frontend creado
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Dependencias Frontend instaladas

if not exist .env (
    copy .env.example .env
    echo ✅ .env Frontend creado
)

call venv\Scripts\deactivate.bat
cd ..

echo.
echo ================================
echo ✨ Setup completado!
echo ================================
echo.
echo 📝 Para ejecutar:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python -m uvicorn main:app --reload
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   venv\Scripts\activate
echo   streamlit run streamlit_app.py
echo.
echo 🌐 Acceder a:
echo   Frontend: http://localhost:8501
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.

pause
