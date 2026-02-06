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
            supabase_url = Config.get_supabase_url()
            supabase_key = Config.get_supabase_key()
            
            print(f"[DEBUG] SUPABASE_URL: {supabase_url[:30] if supabase_url else 'VACIO'}...")
            print(f"[DEBUG] SUPABASE_KEY: {supabase_key[:30] if supabase_key else 'VACIO'}...")
            
            if supabase_url and supabase_key:
                client = create_client(
                    supabase_url.strip(),
                    supabase_key.strip()
                )
                print("[DEBUG] Cliente Supabase creado exitosamente")
                return client
            else:
                print("[ERROR] SUPABASE_URL o SUPABASE_KEY estan vacios")
        except Exception as e:
            print(f"[ERROR] Conectando a Supabase: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    @classmethod
    def is_connected(cls) -> bool:
        """Verifica si hay conexión a Supabase"""
        return cls.get_client() is not None


def get_db() -> Optional[Client]:
    """Helper function para obtener el cliente de BD"""
    return SupabaseClient.get_client()


def get_supabase_client() -> Optional[Client]:
    """Alias para get_db() - obtiene el cliente de Supabase"""
    return get_db()
