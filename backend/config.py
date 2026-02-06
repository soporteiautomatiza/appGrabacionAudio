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
    """Clase para acceder a todas las configuraciones - LECTURA DINÁMICA"""
    
    # Directorios (estáticos, no cambian)
    RECORDINGS_DIR = os.getenv("RECORDINGS_DIR", "recordings")
    OPPORTUNITIES_DIR = os.getenv("OPPORTUNITIES_DIR", "opportunities")
    
    @classmethod
    def get_supabase_url(cls):
        """Lee dinámicamente desde st.secrets o .env"""
        return _get_secret("SUPABASE_URL")
    
    @classmethod
    def get_supabase_key(cls):
        """Lee dinámicamente desde st.secrets o .env"""
        return _get_secret("SUPABASE_KEY")
    
    @classmethod
    def get_gemini_api_key(cls):
        """Lee dinámicamente desde st.secrets o .env"""
        return _get_secret("GEMINI_API_KEY")
    
    @classmethod
    def get_openai_api_key(cls):
        """Lee dinámicamente desde st.secrets o .env"""
        return _get_secret("OPENAI_API_KEY")
    
    # Propiedades para acceso directo (compatibility)
    @property
    def SUPABASE_URL(self):
        return _get_secret("SUPABASE_URL")
    
    @property
    def SUPABASE_KEY(self):
        return _get_secret("SUPABASE_KEY")
    
    @property
    def GEMINI_API_KEY(self):
        return _get_secret("GEMINI_API_KEY")
    
    @property
    def OPENAI_API_KEY(self):
        return _get_secret("OPENAI_API_KEY")
    
    @staticmethod
    def validate():
        """Valida que todas las credenciales necesarias estén configuradas"""
        required = {
            "SUPABASE_URL": _get_secret("SUPABASE_URL"),
            "SUPABASE_KEY": _get_secret("SUPABASE_KEY"),
            "GEMINI_API_KEY": _get_secret("GEMINI_API_KEY")
        }
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
        
        return True
