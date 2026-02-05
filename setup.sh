#!/bin/bash
# Script de Setup Automático para iPrevencion (Linux/Mac)
# Para Windows: ver DEPLOYMENT.md

set -e  # Exit on error

echo "================================"
echo "🚀 iPrevencion - Setup Script"
echo "================================"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. Check Python version
log_info "Verificando Python..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ $python_version == 3.9* ]] || [[ $python_version == 3.10* ]] || [[ $python_version == 3.11* ]]; then
    log_success "Python $python_version detectado"
else
    log_error "Python 3.10+ requerido (encontrado: $python_version)"
    exit 1
fi

# 2. Check PostgreSQL
log_info "Verificando PostgreSQL..."
if command -v psql &> /dev/null; then
    pg_version=$(psql --version)
    log_success "PostgreSQL encontrado: $pg_version"
else
    log_error "PostgreSQL no encontrado. Instálalo con: brew install postgresql"
    exit 1
fi

# 3. Create DB
log_info "Creando base de datos..."
psql -U $(whoami) -tc "SELECT 1 FROM pg_database WHERE datname = 'iprevencion'" | grep -q 1 || psql -U $(whoami) -c "CREATE DATABASE iprevencion;"
log_success "Base de datos lista"

# 4. Backend Setup
log_info "Configurando Backend..."
cd backend

# Create venv
python3 -m venv venv
source venv/bin/activate
log_success "Virtual environment creado"

# Install dependencies
pip install -r requirements.txt
log_success "Dependencias del backend instaladas"

# Create .env
if [ ! -f .env ]; then
    cp .env.example .env
    # Generar SECRET_KEY seguro
    SECRET=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
    sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET/" .env
    log_success ".env creado con SECRET_KEY seguro"
    
    echo ""
    log_info "⚠️ Edita backend/.env y agrega:"
    echo "   GEMINI_API_KEY=tu-key-aqui"
    echo ""
fi

deactivate
cd ..

# 5. Frontend Setup
log_info "Configurando Frontend..."
cd frontend

# Create venv
python3 -m venv venv
source venv/bin/activate
log_success "Virtual environment creado"

# Install dependencies
pip install -r requirements.txt
log_success "Dependencias del frontend instaladas"

# Create .env
if [ ! -f .env ]; then
    cp .env.example .env
    log_success ".env creado"
fi

deactivate
cd ..

log_success "================================"
log_success "✨ Setup completado!"
log_success "================================"
echo ""
echo "📝 Instrucciones para ejecutar:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python -m uvicorn main:app --reload"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  source venv/bin/activate"
echo "  streamlit run streamlit_app.py"
echo ""
echo "🌐 Acceder a:"
echo "  Frontend: http://localhost:8501"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
