import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import streamlit as st
import sys

# Agregar ruta padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import RECORDINGS_DIR, AUDIO_EXTENSIONS, MAX_AUDIO_SIZE_MB
from logger import get_logger

logger = get_logger(__name__)


class AudioRecorder:
    """Gestor de grabaciones de audio"""
    
    def __init__(self) -> None:
        """Inicializa el grabador de audio"""
        # Crear directorio si no existe
        RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("AudioRecorder inicializado")
    
    def get_recordings_list(self) -> List[str]:
        """
        Obtiene lista de audios grabados localmente.
        
        Returns:
            list: Lista de nombres de archivo ordenados por recencia
        """
        try:
            files = os.listdir(str(RECORDINGS_DIR))
            audio_files = [f for f in files if f.endswith(AUDIO_EXTENSIONS)]
            return sorted(audio_files, reverse=True)  # Más recientes primero
        except OSError as e:
            logger.error(f"Error al leer directorio de grabaciones: {e}")
            return []
    
    def get_recordings_from_supabase(self) -> List[str]:
        """
        Obtiene lista de audios desde Supabase.
        
        Returns:
            list: Lista de nombres de archivo desde Supabase o lista vacía si falla
        """
        try:
            from supabase import create_client
            
            # Obtener credenciales desde st.secrets
            supabase_url = st.secrets.get("SUPABASE_URL")
            supabase_key = st.secrets.get("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                logger.warning("Credenciales de Supabase no configuradas")
                return []
            
            # Crear cliente Supabase
            client = create_client(supabase_url.strip(), supabase_key.strip())
            
            # Query a tabla recordings
            response = client.table("recordings").select("filename").order("created_at", desc=True).execute()
            
            if response and response.data:
                return [record["filename"] for record in response.data]
            return []
            
        except ImportError:
            logger.warning("Supabase no instalado")
            return []
        except Exception as e:
            logger.error(f"Error obteniendo grabaciones de Supabase: {e}")
            return []
    
    def validate_audio_file(self, audio_data: bytes, filename: str) -> None:
        """
        Valida un archivo de audio antes de guardarlo.
        
        Args:
            audio_data (bytes): Datos del audio
            filename (str): Nombre del archivo
            
        Raises:
            ValueError: Si el archivo no es válido
        """
        # Validar tamaño
        size_mb = len(audio_data) / (1024 * 1024)
        if size_mb > MAX_AUDIO_SIZE_MB:
            raise ValueError(f"Archivo demasiado grande ({size_mb:.1f}MB). Máximo: {MAX_AUDIO_SIZE_MB}MB")
        
        # Validar extensión
        ext = filename.lower().split('.')[-1]
        if ext not in AUDIO_EXTENSIONS:
            raise ValueError(f"Formato no soportado. Soportados: {', '.join(AUDIO_EXTENSIONS)}")
        
        # Validar que no esté vacío
        if len(audio_data) == 0:
            raise ValueError("El archivo de audio está vacío")
        
        logger.info(f"Validación exitosa para: {filename} ({size_mb:.1f}MB)")
    
    def save_recording(self, audio_data: bytes, filename: Optional[str] = None) -> str:
        """
        Guarda un archivo de audio grabado.
        
        Args:
            audio_data (bytes): Datos del audio
            filename (str, optional): Nombre del archivo. Si no se proporciona, se genera uno.
            
        Returns:
            str: Ruta completa al archivo guardado
            
        Raises:
            ValueError: Si el archivo no es válido
            IOError: Si hay error al guardar
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.wav"
            
            # Validar archivo
            self.validate_audio_file(audio_data, filename)
            
            filepath = RECORDINGS_DIR / filename
            
            # Guardar el archivo
            with open(filepath, "wb") as f:
                f.write(audio_data)
            
            logger.info(f"Audio guardado: {filename}")
            return str(filepath)
            
        except ValueError as e:
            logger.warning(f"Validación falló para {filename}: {e}")
            raise
        except IOError as e:
            logger.error(f"Error al guardar archivo: {e}")
            raise
    
    def delete_recording(self, filename: str) -> bool:
        """
        Elimina un archivo de audio.
        
        Args:
            filename (str): Nombre del archivo a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            filepath = RECORDINGS_DIR / filename
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Audio eliminado: {filename}")
                return True
            logger.warning(f"Archivo no encontrado para eliminar: {filename}")
            return False
        except OSError as e:
            logger.error(f"Error al eliminar archivo {filename}: {e}")
            return False
    
    def get_recording_path(self, filename: str) -> str:
        """
        Obtiene la ruta completa de un archivo de audio.
        Si el archivo local no existe, intenta descargarlo de Supabase Storage.
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            str: Ruta completa al archivo
        """
        filepath = RECORDINGS_DIR / filename
        
        # Si el archivo ya existe localmente, retornar la ruta
        if filepath.exists():
            return str(filepath)
        
        # Si no existe, intentar descargar de Supabase Storage
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from backend.database import download_audio_from_storage
            
            logger.info(f"Archivo local no encontrado: {filename}. Descargando de Storage...")
            if download_audio_from_storage(filename, str(filepath)):
                logger.info(f"Archivo descargado exitosamente: {filename}")
                return str(filepath)
            else:
                logger.error(f"No se pudo descargar {filename} de Storage")
                return str(filepath)  # Retornar la ruta de todos modos (para otros manejos de error)
        except Exception as e:
            logger.warning(f"Error intentando descargar de Storage: {e}")
            return str(filepath)

