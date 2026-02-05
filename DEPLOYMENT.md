# 🔧 Guía de Implementación Paso a Paso

## Parte 1: Instalación Local

### Paso 1: Configurar la Base de Datos

**Opción A: PostgreSQL Local (Windows)**
```bash
# Descargar e instalar desde: https://www.postgresql.org/download/windows/
# Una vez instalado, abrir CMD y:
psql -U postgres
```

Luego en psql:
```sql
CREATE DATABASE iprevencion;
\password postgres  -- Cambiar contraseña
\quit
```

**Opción B: Supabase (Recomendado - te da BD lista en 1 minuto)**
1. Ir a https://supabase.com
2. Sign up (gratis)
3. Create new project
4. Copiar connection string (URL tipo: `postgresql://user:password@host:5432/postgres`)

---

### Paso 2: Configurar Variables de Entorno

#### 2a. Backend `.env`
```bash
cd backend
copy .env.example .env
```

Editar `backend/.env`:
```env
# Obligatorio
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://postgres:tucontraseña@localhost:5432/iprevencion
SECRET_KEY=cambiar-esto-a-algo-seguro-min-32-chars
GEMINI_API_KEY=obtén-tu-key-en-https://makersuite.google.com/app/apikey

# Opcional (defaults están bien)
UPLOAD_DIR=uploads
MAX_FILE_SIZE_MB=100
```

#### 2b. Frontend `.env`
```bash
cd frontend
copy .env.example .env
```

Editar `frontend/.env`:
```env
API_BASE_URL=http://localhost:8000
```

---

### Paso 3: Crear Virtual Environments

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Frontend (en otra terminal)
cd frontend
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### Paso 4: Ejecutar Localmente

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
venv\Scripts\activate
streamlit run streamlit_app.py --server.port 8501
```

Acceder: http://localhost:8501

---

## Parte 2: Despliegue en Railway

### Opción 1: Deploy desde GitHub

```bash
# 1. Inicializar git en tu proyecto
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tuusuario/appGrabacionAudio.git
git branch -M main
git push -u origin main
```

### 2. En Railway:

1. Ir a https://railway.app y hacer login con GitHub
2. `New Project` → `Deploy from GitHub repo`
3. Seleccionar tu repo
4. Railway detectará automáticamente que hay Python

### 3. Crear PostgreSQL en Railway:

1. En tu proyecto: `New` → `Database` → `PostgreSQL`
2. Railway automáticamente agregará variable: `DATABASE_URL`

### 4. Configurar Backend:

1. En el servicio web que creó Railway:
   - Settings → Environment
   - Agregar variables:
   ```env
   ENVIRONMENT=production
   DEBUG=false
   SECRET_KEY=genera-uno-nuevo-seguro
   GEMINI_API_KEY=tu-key
   UPLOAD_DIR=uploads
   ```

2. Build Command: `pip install -r backend/requirements.txt`
3. Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Agregar volume para `/app/uploads` (persistent storage)

### 5. Desplegar Frontend:

**Opción A: Streamlit Cloud (recomendado)**
1. Ir a https://share.streamlit.io
2. "New app" → Conectar GitHub
3. Repository: tu repo
4. Branch: main
5. Main file path: `frontend/streamlit_app.py`
6. Deploy
7. Agregar secreto en Advanced settings:
   ```
   API_BASE_URL = https://tu-backend-railway.railway.app
   ```

**Opción B: Otro servicio en Railway**
1. New → Web Service → Deploy from GitHub
2. Build: `pip install -r frontend/requirements.txt`
3. Start: `cd frontend && streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

---

## Parte 3: Despliegue en Render

### 1. Preparar el Repo

```bash
git init
git add .
git commit -m "Backend + Frontend"
git push
```

### 2. Crear Backend en Render:

1. https://render.com → `New +` → `Web Service`
2. Conectar GitHub
3. Nombre: `iprevencion-api`
4. Environment: `Python 3.10`
5. Build: `pip install -r backend/requirements.txt`
6. Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Free tier ✓
8. Create Web Service

### 3. Crear PostgreSQL en Render:

1. `New +` → `PostgreSQL`
2. Name: `iprevencion-db`
3. Crear

### 4. Conectar BD al Backend:

1. En el PostgreSQL creado, copiar `Internal Database URL`
2. En el servicio Backend → Settings → Environment
3. Agregar variable:
   ```
   DATABASE_URL=<el-url-que-copiaste>
   ```
4. Agregar más variables:
   ```
   ENVIRONMENT=production
   DEBUG=false
   SECRET_KEY=genera-uno-nuevo
   GEMINI_API_KEY=tu-key
   ```

### 5. Crear Frontend en Render:

1. `New +` → `Web Service`
2. Repository: tu repo
3. Build: `pip install -r frontend/requirements.txt`
4. Start: `cd frontend && streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
5. Environment variables:
   ```
   API_BASE_URL=https://tu-backend-render.onrender.com
   STREAMLIT_SERVER_PORT=10000
   ```

---

## Verificación de Despliegue

### El Backend debe mostrar:
```
✅ Base de datos inicializada
🚀 API running on http://0.0.0.0:8000
📖 Docs: https://tu-url/docs
```

### El Frontend debe:
- Permitir registro y login
- Cargar archivos de audio
- Mostrar transcripciones

### Testing rápido de API:
```bash
curl http://localhost:8000/health
# Debe retornar: {"status":"healthy"}

curl http://localhost:8000/docs
# Debe abrir interfaz Swagger
```

---

## 🚨 Troubleshooting

### "Connection refused" en la BD
```bash
# Verificar que PostgreSQL está corriendo
psql -U postgres
# Si falla, reiniciar el servidor PostgreSQL
```

### "GEMINI_API_KEY no configurada"
1. Ir a https://makersuite.google.com/app/apikey
2. Crear nueva API key
3. Copiar a .env o variable de entorno

### "Module not found" errores
```bash
# Asegurar que estás en el venv correcto
source venv/Scripts/activate
pip install -r requirements.txt
```

### Frontend no conecta con API
1. Revisar que backend está corriendo: http://localhost:8000/health
2. Verificar API_BASE_URL en frontend .env
3. Revisar CORS en backend config.py

---

## Monitoreo en Producción

### Railway/Render proporcionales:
- Logs automáticos
- Health checks
- Auto-restart si falla
- Métricas de CPU/RAM

Ver en el dashboard de cada plataforma.

---

## Actualizaciones Futuras

```bash
# Hacer cambios locales
git add .
git commit -m "Tu cambio"
git push

# Automáticamente Railway/Render re-desplegará
```

---

**¡Tu aplicación estará online en 15 minutos!** ⚡
