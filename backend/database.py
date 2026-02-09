import streamlit as st
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import sys

# Agregar ruta padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

# Importar solo lo necesario de Supabase (sin storage3)
try:
    from supabase import create_client, Client
except ImportError:
    # Si falla por storage3/pyiceberg, usamos postgrest directamente
    from postgrest import AsyncPostgrestClient
    create_client = None
    Client = None
    logger.warning("Supabase no instalado correctamente")

@st.cache_resource
def init_supabase() -> Client:
    """
    Inicializa conexión con Supabase.
    
    Returns:
        Client: Cliente de Supabase o None si falla la conexión
    """
    try:
        supabase_url = st.secrets.get("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            logger.error("Credenciales de Supabase no configuradas")
            return None
        
        # Limpiar espacios en blanco
        supabase_url = supabase_url.strip()
        supabase_key = supabase_key.strip()
        
        client = create_client(supabase_url, supabase_key)
        logger.info("Conexión a Supabase establecida exitosamente")
        return client
    except Exception as e:
        logger.error(f"Error al conectar a Supabase: {e}")
        return None

def upload_audio_to_storage(filename: str, filepath: str) -> bool:
    """
    Sube un archivo de audio a Supabase Storage.
    
    Args:
        filename (str): Nombre del archivo
        filepath (str): Ruta local del archivo
        
    Returns:
        bool: True si se subió exitosamente, False en caso contrario
    """
    try:
        # Verificar que el archivo existe antes de intentar subir
        file_path = Path(filepath)
        if not file_path.exists():
            logger.error(f"CRÍTICO: Archivo no encontrado para subir a Storage: {filepath}")
            return False
        
        if not file_path.is_file():
            logger.error(f"CRÍTICO: La ruta no es un archivo: {filepath}")
            return False
        
        # Verificar tamaño
        file_size = file_path.stat().st_size / (1024 * 1024)
        if file_size == 0:
            logger.error(f"CRÍTICO: El archivo está vacío: {filename}")
            return False
        
        logger.info(f"Iniciando upload a Storage: {filename} ({file_size:.2f}MB)")
        
        db = init_supabase()
        if db is None:
            logger.error("CRÍTICO: No se pudo conectar a Supabase para Storage")
            return False
        
        # Leer el archivo
        with open(filepath, "rb") as f:
            file_data = f.read()
        
        if len(file_data) == 0:
            logger.error(f"CRÍTICO: Datos leídos están vacíos: {filename}")
            return False
        
        # Subir a Storage bucket 'recordings'
        logger.info(f"Subiendo {filename} ({len(file_data) / 1024:.2f}KB) a Storage...")
        response = db.storage.from_("recordings").upload(
            path=filename,
            file=file_data,
            file_options={"upsert": "true"}  # "true" como string, no boolean
        )
        
        logger.info(f"✓ Audio subido a Storage exitosamente: {filename}")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"CRÍTICO - Archivo no encontrado: {filepath} - {str(e)}")
        return False
    except PermissionError as e:
        logger.error(f"CRÍTICO - Permiso denegado: {filepath} - {str(e)}")
        return False
    except ConnectionError as e:
        logger.error(f"CRÍTICO - Error de conexión a Supabase Storage: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"CRÍTICO - Error subiendo a Storage '{filename}': {str(e)}")
        return False


def download_audio_from_storage(filename: str, save_to: str) -> bool:
    """
    Descarga un archivo de audio desde Supabase Storage.
    
    Args:
        filename (str): Nombre del archivo en Storage
        save_to (str): Ruta donde guardar el archivo
        
    Returns:
        bool: True si se descargó exitosamente
    """
    try:
        db = init_supabase()
        if db is None:
            logger.warning("No se pudo descargar de Storage (sin conexión)")
            return False
        
        # Descargar de Storage
        response = db.storage.from_("recordings").download(filename)
        
        # Guardar localmente
        with open(save_to, "wb") as f:
            f.write(response)
        
        logger.info(f"Audio descargado de Storage: {filename}")
        return True
        
    except Exception as e:
        logger.warning(f"Error descargando de Storage: {str(e)}")
        return False


def delete_audio_from_storage(filename: str) -> bool:
    """
    Elimina un archivo de audio de Supabase Storage.
    
    Args:
        filename (str): Nombre del archivo en Storage
        
    Returns:
        bool: True si se eliminó exitosamente
    """
    try:
        db = init_supabase()
        if db is None:
            logger.warning("No se pudo eliminar de Storage (sin conexión)")
            return False
        
        # Eliminar de Storage
        db.storage.from_("recordings").remove([filename])
        logger.info(f"Audio eliminado de Storage: {filename}")
        return True
        
    except Exception as e:
        logger.warning(f"Error eliminando de Storage: {str(e)}")
        return False


def save_recording_to_db(filename: str, filepath: str, transcription: Optional[str] = None) -> Optional[str]:
    """
    Guarda grabación en la base de datos y en Storage.
    
    Args:
        filename (str): Nombre del archivo
        filepath (str): Ruta del archivo
        transcription (str, optional): Transcripción del audio
        
    Returns:
        str: ID del recording o None si falla
    """
    try:
        db = init_supabase()
        if db is None:
            logger.error("CRÍTICO: No se pudo conectar a Supabase")
            return None
        
        # Primero intentar subir a Storage ANTES de guardar en BD
        # Esto asegura que el archivo esté disponible antes de registrarlo
        logger.info(f"[1/2] Subiendo audio a Storage...")
        if not upload_audio_to_storage(filename, filepath):
            logger.error(f"[FALLO] No se pudo subir {filename} a Storage. Abortando guardado en BD.")
            return None
        
        # Si Storage fue exitoso, guardar en BD
        logger.info(f"[2/2] Guardando metadata en BD...")
        data = {
            "filename": filename,
            "filepath": filepath,
            "transcription": transcription,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.table("recordings").insert(data).execute()
        
        if response.data:
            recording_id = response.data[0]["id"]
            logger.info(f"✓ ÉXITO: Audio '{filename}' guardado en Supabase Storage + BD (ID: {recording_id})")
            return recording_id
        else:
            logger.warning(f"[FALLO] No se guardó en BD correctamente, pero está en Storage")
            return None
            
    except Exception as e:
        logger.error(f"[CRÍTICO] Error en save_recording_to_db: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error guardando: {str(e)}")
        return None

def get_all_recordings() -> List[Dict[str, Any]]:
    """Obtiene todas las grabaciones de la BD"""
    try:
        db = init_supabase()
        if db is None:
            return []
        
        response = db.table("recordings").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error obteniendo grabaciones: {e}")
        return []

def update_transcription(recording_id: str, transcription: str) -> bool:
    """Actualiza la transcripción de una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        response = db.table("recordings").update({
            "transcription": transcription,
            "updated_at": datetime.now().isoformat()
        }).eq("id", recording_id).execute()
        
        return True if response.data else False
    except Exception as e:
        logger.error(f"Error actualizando transcripción: {e}")
        return False

def save_opportunity(recording_id: str, title: str, description: str) -> bool:
    """Guarda una oportunidad asociada a una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        data = {
            "recording_id": recording_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.table("opportunities").insert(data).execute()
        return True if response.data else False
    except Exception as e:
        logger.error(f"Error guardando oportunidad: {e}")
        return False

def get_opportunities_by_recording(recording_id: str) -> List[Dict[str, Any]]:
    """Obtiene las oportunidades de una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return []
        
        response = db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error obteniendo oportunidades: {e}")
        return []
def delete_recording_from_db(recording_id: int) -> bool:
    """Elimina una grabación de la base de datos"""
    try:
        db = init_supabase()
        if db is None:
            logger.error("No se pudo conectar a Supabase")
            return False
        
        # Primero eliminar las oportunidades asociadas (por seguridad)
        try:
            delete_opportunities_by_recording(recording_id)
        except Exception as e:
            logger.warning(f"Error deleting opportunities for recording {recording_id}: {str(e)}")  # Si no hay oportunidades, ignorar
        
        # Luego eliminar la grabación
        response = db.table("recordings").delete().eq("id", recording_id).execute()
        
        return True
    except Exception as e:
        logger.error(f"Error eliminando grabación: {str(e)}")
        return False

def delete_opportunities_by_recording(recording_id: int) -> bool:
    """Elimina todas las oportunidades asociadas a una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        # Primero obtener los IDs de las oportunidades
        response = db.table("opportunities").select("id").eq("recording_id", recording_id).execute()
        
        if response.data and len(response.data) > 0:
            # Eliminar cada oportunidad
            for opp in response.data:
                db.table("opportunities").delete().eq("id", opp["id"]).execute()
        
        return True
    except Exception as e:
        return False

def delete_recording_by_filename(filename: str) -> bool:
    """Busca y elimina una grabación por nombre de archivo (BD + Storage)"""
    try:
        db = init_supabase()
        if db is None:
            logger.error("No se pudo conectar a Supabase")
            return False
        
        # Buscar el recording_id por filename
        try:
            response = db.table("recordings").select("id").eq("filename", filename).execute()
            
            if response.data and len(response.data) > 0:
                recording_id = response.data[0]["id"]
                
                # Eliminar de la BD
                result = delete_recording_from_db(recording_id)
                
                # Eliminar de Storage en paralelo
                delete_audio_from_storage(filename)
                
                if result:
                    logger.info(f"Grabación eliminada de Supabase y Storage")
                return result
            else:
                # No existe en BD (ya fue eliminado o nunca se guardó)
                return True
        except Exception as e:
            # Si no existe, retornar True (no es error)
            return True
    except Exception as e:
        logger.error(f"Error eliminando grabación: {str(e)}")
        return False

# ============================================================================
# FUNCIONES PARA TRANSCRIPCIONES
# ============================================================================

def save_transcription(recording_filename: str, content: str, language: str = "es") -> Optional[str]:
    """Guarda una transcripción en Supabase asociada a un recording"""
    try:
        db = init_supabase()
        if db is None:
            logger.warning("No se pudo guardar transcripción en Supabase (sin conexión)")
            return None
        
        # Obtener el recording_id por filename
        try:
            response = db.table("recordings").select("id").eq("filename", recording_filename).execute()
            
            if not response.data or len(response.data) == 0:
                logger.warning(f"No se encontró el audio '{recording_filename}' en la BD")
                return None
            
            recording_id = response.data[0]["id"]
            
            # Guardar la transcripción
            data = {
                "recording_id": recording_id,
                "content": content,
                "language": language,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            response = db.table("transcriptions").insert(data).execute()
            
            if response.data and len(response.data) > 0:
                logger.info("Transcripción guardada en Supabase")
                return response.data[0]["id"]
            else:
                logger.warning("No se guardó la transcripción")
                return None
        
        except Exception as e:
            logger.error(f"Error guardando transcripción: {str(e)}")
            return None
            
    except Exception as e:
        logger.error(f"Error en save_transcription: {str(e)}")
        return None


def get_transcription_by_filename(recording_filename: str) -> Optional[Dict[str, Any]]:
    """Obtiene la transcripción más reciente de un audio por filename"""
    try:
        db = init_supabase()
        if db is None:
            return None
        
        # Obtener el recording_id
        response = db.table("recordings").select("id").eq("filename", recording_filename).execute()
        
        if not response.data or len(response.data) == 0:
            return None
        
        recording_id = response.data[0]["id"]
        
        # Obtener la transcripción más reciente
        response = db.table("transcriptions")\
            .select("*")\
            .eq("recording_id", recording_id)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        return response.data[0] if response.data and len(response.data) > 0 else None
        
    except Exception as e:
        return None


def delete_transcription_by_id(transcription_id: str) -> bool:
    """Elimina una transcripción específica por ID"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        response = db.table("transcriptions").delete().eq("id", transcription_id).execute()
        return response is not None
        
    except Exception as e:
        return False