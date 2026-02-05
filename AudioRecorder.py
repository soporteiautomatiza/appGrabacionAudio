import os
import json
from datetime import datetime
from pathlib import Path

RECORDINGS_DIR = "recordings"

class AudioRecorder:
    def __init__(self):
        # Crear directorio si no existe
        Path(RECORDINGS_DIR).mkdir(exist_ok=True)
    
    def get_recordings_list(self):
        """Obtiene lista de audios grabados"""
        try:
            files = os.listdir(RECORDINGS_DIR)
            audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.m4a', '.webm'))]
            return sorted(audio_files, reverse=True)  # Más recientes primero
        except:
            return []
    
    def save_recording(self, audio_data, filename=None):
        """Guarda un archivo de audio grabado"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        
        filepath = os.path.join(RECORDINGS_DIR, filename)
        
        # Guardar el archivo
        with open(filepath, "wb") as f:
            f.write(audio_data)
        
        return filepath
    
    def delete_recording(self, filename):
        """Elimina un archivo de audio"""
        filepath = os.path.join(RECORDINGS_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def get_recording_path(self, filename):
        """Obtiene la ruta completa de un archivo"""
        return os.path.join(RECORDINGS_DIR, filename)
