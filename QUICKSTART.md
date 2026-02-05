# ⚡ Quick Start - 2 Minutos

## 🏃 Opción 1: Ejecución Automática

### Windows:
```bash
setup.bat
```

### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

**Luego sigue las instrucciones en pantalla.**

---

## 🏃 Opción 2: Manual (15 minutos)

### Terminal 1 - Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

# Copiar .env
copy .env.example .env
# IMPORTANTE: Edita .env y agrega:
# - GEMINI_API_KEY=tu-key-de-https://makersuite.google.com
# - DATABASE_URL si usas DB externa

python -m uvicorn main:app --reload
```

### Terminal 2 - Frontend:
```bash
cd frontend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

copy .env.example .env

streamlit run streamlit_app.py
```

---

## 🌐 Acceder

| Componente | URL |
|-----------|-----|
| **Frontend** | http://localhost:8501 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## ⚙️ Primero: Configurar .env

### Backend (`backend/.env`):
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://postgres@localhost:5432/iprevencion
SECRET_KEY=dev-secret-change-in-production
GEMINI_API_KEY=TU_API_KEY_AQUI
```

### Obtener GEMINI_API_KEY:
1. Ir a https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copiar al .env

---

## 🧪 Probar

### En el Frontend:
1. Click "Registrarme"
2. Completa formulario
3. Carga un archivo MP3
4. Espera transcripción (5-10 seg)
5. ¡Chatea con la IA!

### Con Curl (API):
```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"SecurePass123"}'
```

Ver más ejemplos en `TESTING.md`

---

## 🐳 Opción 3: Docker (Avanzado)

```bash
docker-compose up
# Espera a que termine...
# Acceder: http://localhost:8501
```

---

## 📚 Documentación

- **README.md** - Guía completa
- **DEPLOYMENT.md** - Deploy a Railroad/Render
- **ARCHITECTURE.md** - Diagramas
- **TESTING.md** - Ejemplos API
- **INDEX.md** - Índice de archivos

---

## ⚠️ Requisitos

- Python 3.10+
- PostgreSQL 13+ (o Supabase)
- Google Gemini API Key (gratis)

---

## ❌ Si Hay Errores

| Error | Solución |
|-------|----------|
| `Connection refused` | Backend no corriendo - inicia en Terminal 1 |
| `No such DB` | Crear BD: `psql -U postgres -c "CREATE DATABASE iprevencion;"` |
| `GEMINI_API_KEY not found` | Editar backend/.env y agregar key |
| `Port 8501 already in use` | `streamlit run streamlit_app.py --server.port 8502` |

---

## ✅ Listo!

```
✨ Felicidades! Tu aplicación está corriendo.
✨ Frontend: http://localhost:8501
✨ API Docs: http://localhost:8000/docs  
✨ Registra, carga audios, ¡chatea!
```

---

**Para desplegar a la nube:** Lee `DEPLOYMENT.md` (Railway o Render en 20 min)

**Para entender la arquitectura:** Lee `ARCHITECTURE.md`

**¡Disfruta! 🚀**
