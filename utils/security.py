"""
Módulo de configuración segura de credenciales
Carga y valida variables de entorno necesarias
"""

import os
from dotenv import load_dotenv

class SecureConfig:
    """Gestión segura de configuración y credenciales"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Cargar variables de entorno
        load_dotenv()
        
        # Validar variables obligatorias
        self.GEMINI_API_KEY = self._get_required("GEMINI_API_KEY")
        self.OPENAI_API_KEY = self._get_optional("OPENAI_API_KEY")
        
        # Configuración
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 100)) * 1024 * 1024
        self.ENABLE_AUDIT_LOG = os.getenv("ENABLE_AUDIT_LOG", "true").lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        
        self._initialized = True
    
    @staticmethod
    def _get_required(key):
        """Obtiene una variable obligatoria"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"❌ ERROR: {key} no está configurada en .env")
        return value
    
    @staticmethod
    def _get_optional(key, default=None):
        """Obtiene una variable opcional"""
        return os.getenv(key, default)
    
    def is_production(self):
        """Retorna True si está en producción"""
        return self.ENVIRONMENT == "production"
    
    def is_development(self):
        """Retorna True si está en desarrollo"""
        return self.ENVIRONMENT == "development"


# Instancia global
config = SecureConfig()
