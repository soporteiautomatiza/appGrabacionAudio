"""utils.py - Utilidades frontales para procesamiento de audio

Este módulo proporciona funciones de utilidad para procesar y gestionar
archivos de audio en la interfaz de Streamlit.
"""
import hashlib
import streamlit as st
from pathlib import Path
from typing import Tuple, Optional, Any
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import MAX_AUDIO_SIZE_MB
from logger import get_logger
from frontend.notifications import show_success, show_error, show_success_debug
import streamlit as st

logger = get_logger(__name__)

def process_audio_file(
    audio_bytes: bytes,
    filename: str,
    recorder: Any,
    db_utils: Any
) -> Tuple[bool, Optional[str]]:
    """Procesa un archivo de audio (grabación o carga)
    
    Valida tamaño, verifica duplicados por hash, guarda en disco y BD,
    y actualiza el session_state.
    
    Args:
        audio_bytes: Contenido del archivo en bytes
        filename: Nombre del archivo de audio
        recorder: Instancia de AudioRecorder
        db_utils: Módulo de utilidades de BD
        
    Returns:
        Tupla (éxito: bool, recording_id: Optional[str])
        - (True, recording_id) si éxito
        - (False, None) si falla
    """
    try:
        # Validar tamaño
        size_mb = len(audio_bytes) / (1024 * 1024)
        if size_mb > MAX_AUDIO_SIZE_MB:
            show_error(f"Archivo > {MAX_AUDIO_SIZE_MB}MB ({size_mb:.1f}MB)")
            return False, None
        
        # Validar que no esté vacío
        if not audio_bytes:
            show_error("Audio vacío")
            return False, None
        
        # Detectar duplicados por hash MD5
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        if audio_hash in st.session_state.processed_audios:
            logger.info(f"Audio ya procesado: {audio_hash}")
            return False, None
        
        # Guardar archivo
        filepath = recorder.save_recording(audio_bytes, filename)
        recording_id = db_utils.save_recording_to_db(filename, filepath)
        
        if not recording_id:
            show_error("Error: No se guardó en Supabase")
            logger.error(f"BD falló: {filename}")
            return False, None
        
        # Actualizar session state
        st.session_state.processed_audios.add(audio_hash)
        st.session_state.recordings = recorder.get_recordings_from_supabase()
        
        logger.info(f"✓ Audio OK: {filename} (ID: {recording_id})")
        # Agregar al registro de debug
        if "debug_log" not in st.session_state:
            st.session_state.debug_log = []
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.debug_log.append({
            "time": timestamp,
            "type": "success",
            "message": f"Audio '{filename}' guardado en Supabase (ID: {recording_id})"
        })
        return True, recording_id
    
    except (ValueError, FileNotFoundError) as e:
        show_error(f"Error: {str(e)}")
        logger.warning(f"Validación falló: {filename} - {e}")
        return False, None
    
    except Exception as e:
        show_error(f"Error procesando: {str(e)}")
        logger.error(f"Error: {filename} - {e}")
        return False, None

def delete_audio(filename: str, recorder: Any, db_utils: Any) -> bool:
    """Elimina un archivo de audio de BD y almacenamiento local
    
    Args:
        filename: Nombre del archivo a eliminar
        recorder: Instancia de AudioRecorder
        db_utils: Módulo de utilidades de BD
        
    Returns:
        True si éxito, False si error
    """
    try:
        # Eliminar de BD y Storage
        db_utils.delete_recording_by_filename(filename)
        recorder.delete_recording(filename)
        
        # Limpiar session state
        st.session_state.processed_audios.clear()
        
        if filename in st.session_state.recordings:
            st.session_state.recordings.remove(filename)
        
        logger.info(f"✓ Eliminado: {filename}")
        return True
    
    except Exception as e:
        show_error(f"Error al eliminar: {str(e)}")
        logger.error(f"Delete error: {filename} - {e}")
        return False
