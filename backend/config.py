"""
Configuración centralizada - Todas las credenciales y variables de entorno
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Clase para acceder a todas las configuraciones"""
    
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # APIs de IA
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Directorios
    RECORDINGS_DIR = os.getenv("RECORDINGS_DIR", "recordings")
    OPPORTUNITIES_DIR = os.getenv("OPPORTUNITIES_DIR", "opportunities")
    
    @staticmethod
    def validate():
        """Valida que todas las credenciales necesarias estén configuradas"""
        required = ["SUPABASE_URL", "SUPABASE_KEY", "GEMINI_API_KEY"]
        missing = [key for key in required if not getattr(Config, key)]
        
        if missing:
            raise ValueError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
        
        return True
