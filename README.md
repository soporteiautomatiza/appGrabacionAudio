# 🏗️ iPrevencion - Arquitectura Profesional con FastAPI + PostgreSQL + Streamlit

## 📋 Descripción General

**iPrevencion** es un sistema robusto de gestión de grabaciones de audio con capacidades de transcripción automática, análisis de oportunidades de negocio, y chat inteligente potenciado por Google Gemini.

## 🚀 Quick Start (Local)

### Requisitos:
- Python 3.10+, PostgreSQL 13+, Google Gemini API Key

### Instalación:

```bash
# Backend
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env  # Configura tus credenciales

# Frontend (otra terminal)
cd frontend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

### Ejecutar:

```bash
# Terminal 1: Backend
cd backend && uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend && streamlit run streamlit_app.py
```

API disponible en: http://localhost:8000/docs
Frontend: http://localhost:8501

---

## 🌐 Despliegue en Railway

1. Ir a https://railway.app → Conectar GitHub
2. Crear PostgreSQL Database
3. Configurar Backend:
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Agregar variables: DATABASE_URL, SECRET_KEY, GEMINI_API_KEY, ENVIRONMENT=production
5. Desplegar Frontend en Streamlit Cloud o como segundo servicio

---

## 🚀 Despliegue en Render

### Backend:
- New → Web Service → Conectar GitHub
- Build: `pip install -r backend/requirements.txt`
- Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- PostgreSQL Database (crear en Render)

### Frontend:
- New → Web Service
- Start: `cd frontend && streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

---

## 🔌 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/auth/register` | POST | Registrar usuario |
| `/auth/login` | POST | Login con email/contraseña |
| `/audios/upload` | POST | Subir audio y transcribir |
| `/audios/` | GET | Listar audios del usuario |
| `/chat/send` | POST | Enviar pregunta al chat |
| `/chat/history` | GET | Obtener historial |
| `/history/` | GET | Historial completo |

---

## ✅ Características

- ✔️ Autenticación JWT + Bcrypt
- ✔️ Carga de audios multiformato
- ✔️ Transcripción automática con Gemini
- ✔️ Extracción de palabras clave
- ✔️ Chat inteligente con contexto
- ✔️ Base de datos PostgreSQL multitenante
- ✔️ API REST completamente documentada
- ✔️ UI moderna con Streamlit

---

## 📊 Estructura

```
backend/ → FastAPI, modelos SQLAlchemy, servicios Gemini
frontend/ → Streamlit, cliente HTTP de la API
uploads/ → Almacenamiento de audios (generado)
```

---

## 🔐 Seguridad

- Contraseñas con bcrypt
- JWT con expiración
- CORS configurado
- Variables de entorno para secrets
- Validación de archivos
- Logs auditados

---

**Arquitecto Senior | FastAPI + PostgreSQL + Streamlit | Sistema de Audio Inteligente con IA | 2026**
