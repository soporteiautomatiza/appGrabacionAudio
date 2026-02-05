"""
Configuración centralizada del aplicativo
Carga variables de entorno y valida configuración
"""

import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # Aplicación
    APP_NAME: str = "iPrevencion API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Base de Datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/iprevencion"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    ALLOWED_AUDIO_FORMATS: list = ["mp3", "wav", "m4a", "flac", "webm", "ogg"]
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8501",  # Streamlit
        "*"  # En producción, especificar dominios reales
    ]
    
    # Seguridad
    PASSWORD_MIN_LENGTH: int = 8
    ENABLE_AUDIT_LOG: bool = os.getenv("ENABLE_AUDIT_LOG", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Obtiene la instancia de configuración (cached)"""
    return Settings()
