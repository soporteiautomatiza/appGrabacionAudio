"""database.py - Acceso a BD con retry y manejo de errores mejorado"""
import streamlit as st
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
import sys
import time

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from helpers import db_operation, validate_file

logger = get_logger(__name__)

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    logger.warning("⚠️  Supabase no instalado")

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
MAX_RETRIES = 3
RETRY_DELAY = 1  # segundos

# ============================================================================
# UTILIDADES
# ============================================================================

def retry_operation(
    func: Callable,
    *args,
    retries: int = MAX_RETRIES,
    delay: float = RETRY_DELAY,
    **kwargs
) -> Any:
    """Reintenta una operación BD con backoff exponencial
    
    Args:
        func: Función a ejecutar
        retries: Número máximo de reintentos
        delay: Tiempo inicial entre reintentos (se duplica cada intento)
        *args, **kwargs: Argumentos para la función
        
    Returns:
        Resultado de la función o None si falla
    """
    last_exception = None
    
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < retries - 1:
                wait_time = delay * (2 ** attempt)
                logger.warning(f"Intento {attempt + 1}/{retries} falló. Reintentando en {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Operación falló después de {retries} intentos: {type(e).__name__}")
    
    return None

# ============================================================================
# CONEXIÓN A SUPABASE
# ============================================================================

# ============================================================================
# CONEXIÓN A SUPABASE
# ============================================================================

@st.cache_resource
def init_supabase() -> Optional[Client]:
    """Inicializa cliente de Supabase con manejo de errores"""
    try:
        url = st.secrets.get("SUPABASE_URL", "").strip()
        key = st.secrets.get("SUPABASE_KEY", "").strip()
        if not url or not key:
            logger.error("❌ Credentials no configuradas")
            return None
        client = create_client(url, key)
        logger.info("✓ Conexión Supabase OK")
        return client
    except Exception as e:
        logger.error(f"❌ Init Supabase: {e}")
        return None

# ============================================================================
# OPERACIONES DE TABLA GENÉRICAS
# ============================================================================

def _execute_table_operation(
    db,
    table: str,
    method: str,
    filters: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    desc: bool = False
) -> Optional[List[Dict]]:
    """Ejecuta una operación genérica en tabla con manejo de errores
    
    Args:
        db: Cliente Supabase
        table: Nombre de tabla
        method: 'select', 'insert', 'update', 'delete'
        filters: Dict de filtros {column: value}
        data: Datos para insert/update
        order_by: Columna para ordenar
        desc: Si es descendente
    """
    try:
        query = db.table(table)
        
        if method == "select":
            query = query.select("*")
        elif method == "insert":
            query = query.insert(data or {})
        elif method == "update":
            query = query.update(data or {})
        elif method == "delete":
            query = query.delete()
        
        # Aplicar filtros
        if filters:
            for col, val in filters.items():
                query = query.eq(col, val)
        
        # Aplicar ordering
        if order_by:
            query = query.order(order_by, desc=desc)
        
        result = query.execute()
        return result.data if result and result.data else []
    except Exception as e:
        logger.error(f"DB {method} {table}: {type(e).__name__}")
        return [] if method == "select" else None



@db_operation
def upload_audio_to_storage(db, filename: str, filepath: str) -> bool:
    """Sube audio a Supabase Storage"""
    valid, err = validate_file(filepath)
    if not valid:
        logger.error(f"❌ {err}")
        return False
    try:
        with open(filepath, "rb") as f:
            db.storage.from_("recordings").upload(filename, f.read(), {"upsert": "true"})
        logger.info(f"✓ {filename} subido a Storage")
        return True
    except Exception as e:
        logger.error(f"❌ Storage upload: {type(e).__name__}")
        return False

@db_operation
def download_audio_from_storage(db, filename: str, save_to: str) -> bool:
    """Descarga audio de Storage"""
    try:
        response = db.storage.from_("recordings").download(filename)
        Path(save_to).write_bytes(response)
        return True
    except Exception as e:
        logger.warning(f"Download: {str(e)}")
        return False

@db_operation
def delete_audio_from_storage(db, filename: str) -> bool:
    """Elimina audio de Storage"""
    try:
        db.storage.from_("recordings").remove([filename])
        return True
    except:
        return False

@db_operation
def save_recording_to_db(db, filename: str, filepath: str, transcription: Optional[str] = None) -> Optional[str]:
    """Sube a Storage + guarda en BD"""
    logger.info(f"[1/2] Storage: {filename}")
    if not upload_audio_to_storage(filename, filepath):
        logger.error(f"[FAIL] Storage")
        return None
    
    logger.info(f"[2/2] BD metadata")
    try:
        result = db.table("recordings").insert({
            "filename": filename,
            "filepath": filepath,
            "transcription": transcription,
            "created_at": datetime.now().isoformat()
        }).execute()
        recording_id = result.data[0]["id"] if result.data else None
        if recording_id:
            logger.info(f"✓ Recording ID: {recording_id}")
        return recording_id
    except:
        return None

@db_operation
def get_all_recordings(db) -> List[Dict]:
    """Obtiene todas las grabaciones"""
    return _execute_table_operation(db, "recordings", "select")

@db_operation
def update_transcription(db, recording_id: str, transcription: str) -> bool:
    """Actualiza transcripción"""
    return bool(_execute_table_operation(
        db, "recordings", "update",
        filters={"id": recording_id},
        data={"transcription": transcription, "updated_at": datetime.now().isoformat()}
    ))

@db_operation
def save_opportunity(db, recording_id: str, title: str, description: str) -> bool:
    """Guarda oportunidad"""
    return bool(_execute_table_operation(
        db, "opportunities", "insert",
        data={"recording_id": recording_id, "title": title, "description": description, "created_at": datetime.now().isoformat()}
    ))

@db_operation
def get_opportunities_by_recording(db, recording_id: str) -> List[Dict]:
    """Obtiene oportunidades"""
    return _execute_table_operation(db, "opportunities", "select", filters={"recording_id": recording_id})

@db_operation
def delete_recording_from_db(db, recording_id: int) -> bool:
    """Elimina recording + sus oportunidades"""
    try:
        result = db.table("recordings").select("filename").eq("id", recording_id).execute()
        filename = result.data[0]["filename"] if result.data else None
        
        db.table("opportunities").delete().eq("recording_id", recording_id).execute()
        db.table("recordings").delete().eq("id", recording_id).execute()
        
        if filename:
            delete_audio_from_storage(filename)
        return True
    except:
        return False

@db_operation
def delete_recording_by_filename(db, filename: str) -> bool:
    """Busca y elimina por filename"""
    try:
        result = db.table("recordings").select("id").eq("filename", filename).execute()
        if result.data:
            return delete_recording_from_db(result.data[0]["id"])
        return True
    except:
        return False

@db_operation
def save_transcription(db, recording_filename: str, content: str, language: str = "es") -> Optional[str]:
    """Guarda transcripción"""
    try:
        result = db.table("recordings").select("id").eq("filename", recording_filename).execute()
        if not result.data:
            return None
        
        recording_id = result.data[0]["id"]
        trans_result = db.table("transcriptions").insert({
            "recording_id": recording_id,
            "content": content,
            "language": language,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }).execute()
        return trans_result.data[0]["id"] if trans_result.data else None
    except:
        return None

@db_operation
def get_transcription_by_filename(db, recording_filename: str) -> Optional[Dict]:
    """Obtiene transcripción por filename"""
    try:
        result = db.table("recordings").select("id").eq("filename", recording_filename).execute()
        if not result.data:
            return None
        
        trans = db.table("transcriptions").select("*").eq("recording_id", result.data[0]["id"]).order("created_at", desc=True).limit(1).execute()
        return trans.data[0] if trans.data else None
    except:
        return None

@db_operation
def delete_transcription_by_id(db, transcription_id: str) -> bool:
    """Elimina una transcripción"""
    try:
        db.table("transcriptions").delete().eq("id", transcription_id).execute()
        return True
    except:
        return False
