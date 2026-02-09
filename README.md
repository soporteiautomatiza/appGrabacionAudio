# 🎵 Sistema Control Audio Iprevencion

> Sistema inteligente de análisis de audios con IA para gestión de oportunidades de negocio

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://appgrabacionaudio.streamlit.app/)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Tabla de contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## ✨ Características

### 🎙️ **Grabación y Carga de Audio**
- Grabación de audio en vivo directamente desde el navegador
- Carga de archivos de audio (MP3, WAV, M4A, OGG, FLAC, WebM)
- Deduplicación automática de audios
- Soporta archivos hasta 100MB

### 🎯 **Transcripción Inteligente**
- Transcripción automática usando Google Gemini 2.0-flash
- Caché de transcripciones para mejor performance
- Indicador visual "✓ Transcrito" para audios procesados
- Búsqueda en tiempo real mientras escribes

### 🤖 **Análisis con IA**
- Chat inteligente basado en contexto de transcripción
- Palabras clave configurables para análisis específico
- Soporte para análisis en múltiples idiomas
- Historial de conversación con límite de memoria

### 🎟️ **Gestión de Oportunidades**
- Extracción automática de oportunidades basada en palabras clave
- Estados configurables: new, in_progress, closed, won
- Prioridades: Low, Medium, High
- Notas y contexto para cada oportunidad
- Almacenamiento en Supabase con fallback local

### 🔍 **Herramientas de Búsqueda**
- Búsqueda en tiempo real mientras escribes
- Filtrado de audios por nombre
- Visualización de resultados instantánea
- Información de transcripción en resultados

### 💾 **Gestión de Datos**
- Almacenamiento en PostgreSQL/Supabase
- Fallback local en JSON para trabajar sin conexión
- Eliminación segura con confirmación
- Gestión en lote de archivos

---

## 🚀 Instalación

### Prerequisitos
- Python 3.9+
- Git
- pip o conda

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/devIautomatiza1/appGrabacionAudio.git
cd appGrabacionAudio
```

2. **Crear entorno virtual**
```bash
# Con venv
python -m venv .venv

# O con conda
conda create -n audio-app python=3.9
conda activate audio-app
```

3. **Activar entorno virtual**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales reales
```

---

## ⚙️ Configuración

### Variables de entorno (`.env`)

```ini
# Google Gemini API
GEMINI_API_KEY=tu_clave_gemini

# Supabase Database
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_clave_supabase_publica

# Logging (optional)
LOG_LEVEL=INFO
```

### Obtener credenciales

#### Google Gemini API
1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un proyecto nuevo
3. Habilita "Generative AI API"
4. Crea una API key en "Credenciales"
5. Copia la key a `GEMINI_API_KEY`

#### Supabase
1. Ve a [Supabase.com](https://supabase.com)
2. Crea un proyecto nuevo
3. Ve a Settings → API
4. Copia Project URL → `SUPABASE_URL`
5. Copia "anon" key → `SUPABASE_KEY`

### Inicializar Base de Datos

```bash
# En Supabase SQL Editor, ejecuta:
# contenido de basedatos.sql
```

O la app creará las tablas automáticamente en el primer uso.

---

## 💻 Uso

### Local

```bash
streamlit run streamlit_app.py
```

La app se abrirá en `http://localhost:8501`

### Streamlit Cloud

Ver [STREAMLIT_SETUP.md](STREAMLIT_SETUP.md) para instrucciones completas de deployment.

### Flujo de trabajo típico

1. **Grabar o subir audio**
   - Usa la grabadora en vivo O sube un archivo

2. **Ver audios guardados**
   - Busca por nombre en tiempo real
   - Haz click en el audio para seleccionarlo

3. **Transcribir**
   - Haz click en "Transcribir"
   - Espera a que Google Gemini procese el audio

4. **Analizar con IA**
   - Agrega palabras clave (ej: "presupuesto", "cliente")
   - Haz click en "Analizar y Generar Tickets"

5. **Gestionar oportunidades**
   - Revisa el contexto donde apareció la palabra clave
   - Cambia estado y prioridad
   - Agrega notas
   - Guarda o elimina

6. **Chat inteligente (opcional)**
   - Haz preguntas sobre la transcripción
   - La IA responde considerando las palabras clave

---

## 🏗️ Arquitectura

```
appGrabacionAudio/
├── frontend/                    # Interfaz Streamlit
│   ├── index.py                # App principal
│   ├── AudioRecorder.py        # Gestión de grabaciones
│   ├── styles.py               # CSS personalizado
│   ├── notifications.py        # Notificaciones UI
│   └── utils.py                # Funciones auxiliares
│
├── backend/                     # Lógica de negocio
│   ├── Transcriber.py          # Google Gemini transcripción
│   ├── Model.py                # AI chat (Gemini)
│   ├── OpportunitiesManager.py # Gestión de oportunidades
│   └── database.py             # Conexión Supabase
│
├── config.py                    # Configuración centralizada
├── logger.py                    # Sistema de logging
├── streamlit_app.py            # Punto de entrada
├── requirements.txt            # Dependencias
├── basedatos.sql               # Schema SQL
├── .env.example                # Template variables entorno
└── STREAMLIT_SETUP.md          # Guía de deployment

data/
├── recordings/                 # Audios guardados localmente
├── opportunities/              # Oportunidades en JSON
└── app.log                      # Logs de la aplicación
```

### Stack tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Frontend** | Streamlit 1.32.0 |
| **Backend** | Python 3.9+ |
| **IA** | Google Generative AI (Gemini 2.0-flash) |
| **Database** | PostgreSQL/Supabase |
| **Logging** | Python logging |
| **Config** | python-dotenv |

---

## 📦 Dependencias principales

```
streamlit==1.32.0              # Framework web
google-generativeai==0.8.6     # API Gemini
supabase>=2.0.0                # Cliente Supabase
postgrest>=0.15.0              # ORM PostgreSQL
python-dotenv==1.0.0           # Variables de entorno
psycopg2-binary                # Driver PostgreSQL
```

Ver `requirements.txt` para versiones exactas.

---

## 🌐 Deployment

### Streamlit Cloud (Recomendado)

1. **Push a GitHub**
```bash
git push origin main
```

2. **Conectar en Streamlit Cloud**
   - Ve a https://share.streamlit.io
   - Conecta tu repositorio de GitHub
   - Configura Secrets en Settings
   - Deploy

Ver [STREAMLIT_SETUP.md](STREAMLIT_SETUP.md) para detalles.

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Heroku

```bash
# Requiere Procfile y setup.sh
git push heroku main
```

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY no está configurada"
- Copia `.env.example` a `.env`
- Obtén tu key en [Google Cloud Console](https://console.cloud.google.com)
- Verifica que `.env` esté en .gitignore

### "No se pudo conectar a Supabase"
- Verifica `SUPABASE_URL` y `SUPABASE_KEY` en `.env`
- Asegúrate de que Supabase project no esté paused
- Verifica que RLS esté deshabilitado en tablas

### "Error al transcribir: timeout"
- El archivo es muy grande (máx 100MB)
- Intenta con un archivo más pequeño
- Verifica conexión a internet

### "Base de datos no inicializada"
- Ejecuta el SQL desde `basedatos.sql` en Supabase
- O usa la app - creará las tablas automáticamente

### Logs no aparecen
- Verifica que `LOG_LEVEL=INFO` en `.env`
- Logs se guardan en `data/app.log`
- En Streamlit Cloud, ve a Settings → Logs

---

## 📝 Logs y Debugging

### Ver logs locales
```bash
tail -f data/app.log
```

### Niveles de log
```
DEBUG   - Información detallada para debugging
INFO    - Información general de la app
WARNING - Advertencias (defecto)
ERROR   - Errores importantes
CRITICAL - Errores críticos
```

Configura en `.env`:
```ini
LOG_LEVEL=DEBUG  # Para más detalle
```

---

## 🔐 Seguridad

### Buenas prácticas

✅ **HACER:**
- Mantener `.env` en `.gitignore`
- Usar credenciales diferentes para dev/prod
- Habilitar RLS en Supabase
- Rotar API keys periódicamente
- Usar HTTPS en producción

❌ **NO HACER:**
- Commitar `.env` a Git
- Compartir `.env` con otros
- Usar mismas credenciales en dev y prod
- Publicar API keys en issues

---

## 📊 Estadísticas del proyecto

- **Versión**: 1.0.0
- **Lenguaje**: Python 3.9+
- **Líneas de código**: ~1500
- **Módulos**: 7 (frontend, backend, config, logger)
- **Dependencias**: 6 principales

---

## 🤝 Contribuciones

Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para detalles.

---

## 👨‍💻 Autor

Desarrollado como solución para análisis inteligente de audios con IA.

---

## 📞 Soporte

- 📖 [Documentación Streamlit](https://docs.streamlit.io)
- 🤖 [API Gemini](https://ai.google.dev)
- 🗄️ [Supabase Docs](https://supabase.com/docs)
- 🐛 [Issues](https://github.com/devIautomatiza1/appGrabacionAudio/issues)

---

## ✨ Mejoras Recientes

- ✅ Búsqueda en tiempo real
- ✅ Caché de transcripciones
- ✅ Validación de credenciales
- ✅ Type hints en todas las funciones
- ✅ Confirmación de eliminación segura
- ✅ Límite inteligente de historial de chat

---

**Última actualización:** Febrero 2026
