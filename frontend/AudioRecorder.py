import os
import json
from datetime import datetime
from pathlib import Path
import streamlit as st

# Obtener ruta a datos desde la carpeta parent/data
BASE_DIR = Path(__file__).parent.parent / "data"
RECORDINGS_DIR = BASE_DIR / "recordings"

class AudioRecorder:
    def __init__(self):
        # Crear directorio si no existe
        RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    
    def get_recordings_list(self):
        """Obtiene lista de audios grabados"""
        try:
            files = os.listdir(str(RECORDINGS_DIR))
            audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.m4a', '.webm'))]
            return sorted(audio_files, reverse=True)  # Más recientes primero
        except:
            return []
    
    def get_recordings_from_supabase(self):
        """Obtiene lista de audios desde Supabase (sin errores en UI)"""
        try:
            from supabase import create_client
            
            # Obtener credenciales desde st.secrets (disponible en Streamlit)
            supabase_url = st.secrets.get("SUPABASE_URL")
            supabase_key = st.secrets.get("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                return []
            
            # Crear cliente Supabase directamente aquí
            client = create_client(supabase_url.strip(), supabase_key.strip())
            
            # Query a tabla recordings
            response = client.table("recordings").select("filename").order("created_at", desc=True).execute()
            
            if response and response.data:
                return [record["filename"] for record in response.data]
            return []
            
        except ImportError:
            # Supabase no installado
            return []
        except Exception as e:
            # Error silencioso - retornar lista vacía
            return []
    
    def save_recording(self, audio_data, filename=None):
        """Guarda un archivo de audio grabado"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        
        filepath = RECORDINGS_DIR / filename
        
        # Guardar el archivo
        with open(filepath, "wb") as f:
            f.write(audio_data)
        
        return str(filepath)
    
    def delete_recording(self, filename):
        """Elimina un archivo de audio"""
        filepath = RECORDINGS_DIR / filename
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    def get_recording_path(self, filename):
        """Obtiene la ruta completa de un archivo"""
        return str(RECORDINGS_DIR / filename)
