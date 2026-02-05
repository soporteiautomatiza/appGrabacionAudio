# 🏛️ Arquitectura de Sistema - iPrevencion

## 📊 Diagrama General de la Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INTERNET PUBLIC                             │
└────────────────────────────┬──────────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┬─────────────────┐
              │                            │                  │
    ┌─────────▼─────────┐      ┌──────────▼────────┐    ┌────▼──────────────┐
    │  FRONTEND (UI)    │      │  BACKEND (API)    │    │ STORAGE (Optional)│
    │  Streamlit        │      │  FastAPI          │    │ S3/GCS/Azure Blob │
    │  - Login/Register │◄────►│  - Auth endpoints │    │ (para audios)     │
    │  - Upload audios  │  HTTP│  - Audio routes   │    └───────────────────┘
    │  - Chat UI        │ JSON │  - Chat routes    │
    │  - History view   │      │  - History routes │
    │  Port: 8501       │      │  Port: 8000       │
    └─────────────────┬─┘      └────────┬──────────┘
                      │                 │
                      │    ┌────────────┴──────────────┐
                      │    │                           │
                      │    ▼                           ▼
                      │  ┌──────────────────────────────────────┐
                      │  │   DATABASE LAYER                     │
                      │  │   PostgreSQL 13+                     │
                      │  │                                      │
                      │  │  Tables:                             │
                      │  │  - users                             │
                      │  │  - audios                            │
                      │  │  - transcriptions                    │
                      │  │  - opportunities                     │
                      │  │  - chat_messages                     │
                      │  └──────────────────────────────────────┘
                      │
                      └─► Google Cloud Storage / Local Filesystem
                          (Archivos de audio cargados)
```

## 🔄 Flujo de Datos

### 1. Registro e Inicio de Sesión
```
Frontend (Login Form)
    │
    ├─► POST /auth/register {email, name, password}
    │       ├─► Hash password con bcrypt
    │       ├─► Crear usuario en DB
    │       └─► Retornar JWT tokens
    │
    └─► POST /auth/login {email, password}
            ├─► Validar credenciales
            ├─► Generar access_token y refresh_token
            └─► Retornar tokens
```

### 2. Carga y Transcripción de Audio
```
Frontend (Upload File)
    │
    └─► POST /audios/upload (Bearer token)
            │
            ├─► Validar formato y tamaño
            ├─► Guardar archivo en filesystem
            ├─► Crear record en tabla audios
            │
            ├─► [BACKGROUND] Transcriber Service
            │       ├─► Leer archivo de audio
            │       ├─► Enviar a Google Gemini
            │       ├─► Recibir transcripción
            │       ├─► Extraer palabras clave
            │       ├─► Almacenar en tabla transcriptions
            │       │
            │       └─► [BACKGROUND] Opportunities Extractor
            │               ├─► Analizar transcripción
            │               ├─► Buscar palabras clave
            │               ├─► Extraer contexto
            │               └─► Guardar opportunities
            │
            └─► Retornar audio record (estado: uploadeado)

Frontend (pooling)
    └─► GET /audios/{id} → Estado: completed + transcripción + opportunities
```

### 3. Chat Inteligente
```
Frontend (User asks question)
    │
    └─► POST /chat/send {content, audio_id}
            │
            ├─► Crear ChatMessage (role: user)
            ├─► Optimizar contexto:
            │   ├─► Si audio_id → usar transcripción de ese audio
            │   └─► Si no → combinar últimas transcripciones
            │
            ├─► Chat Service (Gemini)
            │   ├─► Construir prompt con contexto + pregunta
            │   ├─► Enviar a Gemini 2.0 Flash
            │   ├─► Recibir respuesta
            │   └─► Retornar respuesta
            │
            └─► Crear ChatMessage (role: assistant)

Frontend (show messages)
    └─► GET /chat/history?limit=50
            └─► Retornar lista ordenada de mensajes
```

## 🔐 Seguridad - Capas

### Capa 1: Transporte
- HTTPS forzado en producción
- TLS 1.3 en BD remota

### Capa 2: Autenticación
- Bcrypt para hashing de contraseñas (10 rounds)
- JWT HS256 para tokens
- Token expiration: 30 min (access), 7 días (refresh)

### Capa 3: Autorización
- Bearer token en cada request
- Validación de propietario de recursos
- RLS (Row Level Security) en DB si es posible

### Capa 4: Aplicación
- Validación de entrada (Pydantic schemas)
- Rate limiting en endpoints críticos
- CORS permitido solo para dominios conocidos
- Sanitización de archivos subidos

### Capa 5: Datos
- Contraseñas nunca en logs
- Encriptación de secrets en .env
- Backups automáticos en producción
- Auditoría de cambios

## 📦 Stack Tecnológico

### Backend
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | FastAPI | REST API framework |
| **ORM** | SQLAlchemy | Object-relational mapping |
| **Database** | PostgreSQL | Relational database |
| **Auth** | Python-jose + Passlib | JWT & password hashing |
| **AI/ML** | Google Gemini API | Transcription & Chat |
| **Server** | Uvicorn | ASGI server |

### Frontend
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Streamlit | Web app framework |
| **HTTP Client** | Requests | API calls |
| **State** | session_state | Client-side state |

### DevOps
| Service | Provider | Purpose |
|---------|----------|---------|
| **Database** | Railway / Render / Supabase | PostgreSQL hosting |
| **API** | Railway / Render | Backend hosting |
| **Frontend** | Streamlit Cloud / Railway | UI hosting |
| **Storage** | Local / S3 (optional) | Audio files |

## 🗂️ Organización del Código

### Backend Structure
```
backend/
├── main.py                 # FastAPI app
├── app/
│   ├── core/
│   │   ├── config.py       # Settings, env vars
│   │   ├── database.py     # SQLAlchemy session
│   │   └── security.py     # JWT, password utils
│   ├── models/
│   │   └── models.py       # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py      # Pydantic validation
│   ├── routes/
│   │   ├── auth.py         # /auth endpoints
│   │   ├── audio.py        # /audios endpoints
│   │   ├── chat.py         # /chat endpoints
│   │   └── history.py      # /history endpoints
│   └── services/
│       ├── transcriber.py  # Gemini transcription
│       ├── chat.py         # Gemini chat
│       └── opportunities.py # Opportunity extraction
├── requirements.txt
└── Dockerfile
```

### Frontend Structure
```
frontend/
├── streamlit_app.py        # Main Streamlit app
├── requirements.txt
└── Dockerfile
```

## 🚀 Scalability Considerations

### Current Architecture (Single Instance)
- Fits for ~100-1000 users
- Synchronous audio transcription

### Future: Scalable (Horizontal)
```
Load Balancer
    ├─► API Instance 1
    ├─► API Instance 2
    └─► API Instance N
         ↓
    PostgreSQL (read replicas)
         ↓
    Redis Cache (optional)
    Celery Workers (background tasks)
```

## 📈 Performance Optimization

### Already Implemented
- Connection pooling (SQLAlchemy)
- Query indexing on user_id, created_at
- JWT tokens reduce DB queries
- Caching: Supabase/Railway handle it

### To Implement
- Redis caching for transcriptions
- Celery for background tasks
- Database query optimization
- CDN for static files
- Audio compression/conversion

## 🔄 CI/CD Pipeline (Future)

```
Git Push → GitHub Actions
    ├─► Run tests
    ├─► Build Docker images
    ├─► Push to registry
    └─► Deploy to Railway/Render
         ├─► DB migrations
         └─► Health checks
```

## 📊 Monitoring & Logging

### Key Metrics
- API response time (target: <500ms)
- Transcription speed (depends on audio length)
- Error rate (target: <1%)
- Uptime (target: 99.5%)

### Logging Strategy
- INFO: Important events (login, uploads)
- WARNING: Issues that might need attention
- ERROR: Critical failures
- DEBUG: Development only

## 🔮 Future Enhancements

1. **Real-time Chat** - WebSocket instead of HTTP polling
2. **Audio Processing** - FFmpeg integration for compression
3. **Advanced Analytics** - Dashboard with insights
4. **Multi-language** - i18n support
5. **Mobile App** - React Native frontend
6. **Fine-tuning** - Custom Gemini model
7. **Integration** - Zapier, webhooks, third-party APIs
8. **RBAC** - Role-based access control

---

**Documentación Arquitectónica | iPrevencion | 2026**
