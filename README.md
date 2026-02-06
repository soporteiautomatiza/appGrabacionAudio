# 🎙️ Sistema Control Audio Iprevencion

## Estructura de Proyecto (Backend/Frontend)

```
appGrabacionAudio/
├── frontend/                 # Interfaz de usuario Streamlit
│   ├── index.py             # Aplicación principal
│   ├── styles.py            # Estilos CSS personalizados
│   ├── notifications.py     # Sistema de notificaciones
│   └── AudioRecorder.py     # Grabador de audio
│
├── backend/                 # Lógica de negocio y procesamiento
│   ├── database.py          # Conexión y operaciones en Supabase
│   ├── Transcriber.py       # Transcripción de audio (Google Generative AI)
│   ├── Model.py             # Modelo IA para análisis (Gemini)
│   └── OpportunitiesManager.py  # Gestión de oportunidades
│
├── data/                    # Almacenamiento local de audios (gitignore)
│   └── recordings/          # Grabaciones de audio
│
├── run.py                   # Script para ejecutar la aplicación
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno (gitignore)
├── .gitignore              # Archivos a ignorar en git
└── .streamlit/             # Configuración de Streamlit
    └── config.toml         # Configuración de rutas y tema
```

## 🚀 Cómo Ejecutar

### Opción 1: Usando el script run.py
```bash
python run.py
```

### Opción 2: Directamente con Streamlit
```bash
streamlit run frontend/index.py
```

## 🔒 Seguridad

### Variables de Entorno Necesarias (.env)
```
GEMINI_API_KEY=tu_clave_api_aqui
SUPABASE_URL=tu_url_supabase
SUPABASE_KEY=tu_clave_supabase
```

### Secretos en Streamlit (.streamlit/secrets.toml)
```toml
GEMINI_API_KEY = "tu_clave_api_aqui"
SUPABASE_URL = "tu_url_supabase"
SUPABASE_KEY = "tu_clave_supabase"
```

## 📦 Dependencias

- **streamlit** - Framework web
- **google-generativeai** - API de Gemini
- **supabase** - Cliente Supabase
- **python-dotenv** - Manejo de variables de entorno
- **openai** - Integraciones OpenAI
- **psycopg2-binary** - Driver PostgreSQL

## 🆕 Cambios en la Estructura

### Ventajas de esta organización:

1. **Separación de Responsabilidades**
   - Frontend: Todo lo relacionado con UI
   - Backend: Lógica de negocio, APIs, BDD

2. **Mantenibilidad**
   - Código más organizado y fácil de encontrar
   - Mejor gestión de dependencias

3. **Seguridad**
   - Secretos separados por ambiente
   - Imports claros y trazables

4. **Escalabilidad**
   - Fácil agregar nuevas características
   - Preparado para microservicios en el futuro

## 📝 Notas Importantes

- La carpeta `data/` debe existir para almacenar grabaciones locales
- Los archivos `.env` y `.streamlit/secrets.toml` están en `.gitignore` por seguridad
- Las grabaciones se guardan localmente y se sincronizan con Supabase
- Las credenciales de APIs no deben estarse en el repositorio
