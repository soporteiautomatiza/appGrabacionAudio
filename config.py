"""config.py - Configuración centralizada de la aplicación"""
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# ============================================================================
# RUTAS Y DIRECTORIOS
# ============================================================================
APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"
RECORDINGS_DIR = DATA_DIR / "recordings"
OPPORTUNITIES_DIR = DATA_DIR / "opportunities"

# Crear directorios si no existen
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
OPPORTUNITIES_DIR.mkdir(parents=True, exist_ok=True)

# Validar que los directorios fueron creados correctamente
if not RECORDINGS_DIR.is_dir():
    logging.warning(f"⚠️  Directorio de grabaciones no existe: {RECORDINGS_DIR}")
if not OPPORTUNITIES_DIR.is_dir():
    logging.warning(f"⚠️  Directorio de oportunidades no existe: {OPPORTUNITIES_DIR}")

# ============================================================================
# CONFIGURACIÓN DE AUDIO
# ============================================================================
AUDIO_EXTENSIONS = ("mp3", "wav", "m4a", "ogg", "flac", "webm")

# Validar y parsear MAX_AUDIO_SIZE_MB
try:
    MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "100"))
    if MAX_AUDIO_SIZE_MB <= 0:
        raise ValueError("Debe ser positivo")
except ValueError as e:
    raise ValueError(f"MAX_AUDIO_SIZE_MB inválido: {e}") from None

MIME_TYPES = {
    'mp3': 'audio/mpeg',
    'wav': 'audio/wav',
    'm4a': 'audio/mp4',
    'flac': 'audio/flac',
    'webm': 'audio/webm',
    'ogg': 'audio/ogg',
}

# ============================================================================
# CREDENCIALES Y CONFIGURACIÓN EXTERNA
# ============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validar credenciales críticas
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Error de configuración: Faltan credenciales de Supabase.\n"
        "Asegúrate de que .env contiene:\n"
        "  - SUPABASE_URL\n"
        "  - SUPABASE_KEY\n"
        "Para Streamlit Cloud, configúralas en Settings > Secrets"
    )

# ============================================================================
# INFORMACIÓN DE LA APLICACIÓN
# ============================================================================
APP_NAME = "Sistema Control Reuniones"
APP_DESCRIPTION = "Sistema inteligente de análisis de audios con IA para gestión de oportunidades"
APP_VERSION = "1.0.0"

# ============================================================================
# MODELOS DE IA
# ============================================================================
TRANSCRIPTION_MODEL = "gemini-2.0-flash"
CHAT_MODEL = "gemini-2.0-flash"

# ============================================================================
# OPCIONES DE DATOS
# ============================================================================
STATUS_OPTIONS = ["new", "in_progress", "closed", "won"]
PRIORITY_OPTIONS = ["Low", "Medium", "High"]

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "app.log"

# Configuración de sesión y UI
CHAT_HISTORY_LIMIT = 50  # Límite máximo de mensajes en chat
MAX_SEARCH_RESULTS = 20  # Resultados máximos en búsqueda
SESSION_TIMEOUT_MINUTES = 30  # Timeout de sesión
REFRESH_INTERVAL_SECONDS = 5  # Intervalo de refresco de datos

# Configuración de cache
CACHE_TTL_MINUTES = 10  # Tiempo de vida del cache en minutos
