"""
Configuración centralizada - Todas las credenciales y variables de entorno
"""
import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (solo en local)
load_dotenv()

def _get_secret(key: str, default: str = None) -> str:
    """Obtiene un secret desde st.secrets (Cloud) o variables de entorno (local)"""
    try:
        # Primero intenta desde st.secrets (Streamlit Cloud)
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    
    # Luego desde variables de entorno (local)
    return os.getenv(key, default or "")

class Config:
    """Clase para acceder a todas las configuraciones"""
    
    # Supabase
    SUPABASE_URL = _get_secret("SUPABASE_URL")
    SUPABASE_KEY = _get_secret("SUPABASE_KEY")
    
    # APIs de IA
    GEMINI_API_KEY = _get_secret("GEMINI_API_KEY")
    OPENAI_API_KEY = _get_secret("OPENAI_API_KEY")
    
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
