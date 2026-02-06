"""
Cliente único de Supabase - Punto centralizado para todas las conexiones
"""
import streamlit as st
from typing import Optional
from supabase import create_client, Client
from backend.config import Config

class SupabaseClient:
    """Cliente singleton para Supabase"""
    _instance: Optional[Client] = None
    
    @classmethod
    @st.cache_resource
    def get_client(cls) -> Optional[Client]:
        """
        Obtiene la instancia del cliente Supabase.
        Usa cache de Streamlit para evitar reconexiones.
        """
        try:
            if Config.SUPABASE_URL and Config.SUPABASE_KEY:
                return create_client(
                    Config.SUPABASE_URL.strip(),
                    Config.SUPABASE_KEY.strip()
                )
        except Exception as e:
            print(f"Error conectando a Supabase: {e}")
        
        return None
    
    @classmethod
    def is_connected(cls) -> bool:
        """Verifica si hay conexión a Supabase"""
        return cls.get_client() is not None


def get_db() -> Optional[Client]:
    """Helper function para obtener el cliente de BD"""
    return SupabaseClient.get_client()
