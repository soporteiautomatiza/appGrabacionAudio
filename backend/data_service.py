"""
data_service.py - Servicio de datos que separa lógica de negocio de conexión BD
Abstrae las operaciones CRUD sobre Supabase
"""
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import sys

# Agregar ruta padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from database import init_supabase

logger = get_logger(__name__)


class RecordingService:
    """Servicio para gestionar grabaciones"""
    
    @staticmethod
    def get_by_filename(filename: str) -> Optional[Dict[str, Any]]:
        """Obtiene un recording por nombre de archivo"""
        try:
            db = init_supabase()
            if not db:
                return None
            
            response = db.table("recordings").select("*").eq("filename", filename).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error al obtener recording {filename}: {type(e).__name__} - {str(e)}")
            return None
    
    @staticmethod
    def get_id(filename: str) -> Optional[str]:
        """Obtiene solo el ID de un recording por filename"""
        try:
            db = init_supabase()
            if not db:
                logger.warning(f"BD no disponible para obtener ID de {filename}")
                return None
            
            response = db.table("recordings").select("id").eq("filename", filename).execute()
            if response and response.data and len(response.data) > 0:
                return response.data[0]["id"]
            
            logger.warning(f"No se encontró recording para {filename}")
            return None
        except Exception as e:
            logger.error(f"Error al obtener recording ID: {type(e).__name__} - {str(e)}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Obtiene todas las grabaciones"""
        try:
            db = init_supabase()
            if not db:
                return []
            
            response = db.table("recordings").select("*").order("created_at", desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Error al obtener todas las grabaciones: {type(e).__name__} - {str(e)}")
            return []


class TranscriptionService:
    """Servicio para gestionar transcripciones"""
    
    @staticmethod
    def get_by_filename(recording_filename: str) -> Optional[Dict[str, Any]]:
        """Obtiene la transcripción más reciente de un audio por filename"""
        try:
            db = init_supabase()
            if not db:
                return None
            
            # Obtener el recording_id
            response = db.table("recordings").select("id").eq("filename", recording_filename).execute()
            if not response.data or len(response.data) == 0:
                logger.debug(f"Recording no encontrado para transcripción: {recording_filename}")
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
            logger.error(f"Error al obtener transcripción de {recording_filename}: {type(e).__name__} - {str(e)}")
            return None
    
    @staticmethod
    def save(recording_filename: str, content: str, language: str = "es") -> Optional[str]:
        """Guarda una transcripción en Supabase"""
        try:
            db = init_supabase()
            if not db:
                logger.warning("BD no disponible para guardar transcripción")
                return None
            
            # Obtener el recording_id
            recording_id = RecordingService.get_id(recording_filename)
            if not recording_id:
                logger.error(f"Recording no encontrado para guardar transcripción: {recording_filename}")
                return None
            
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
                transcription_id = response.data[0]["id"]
                logger.info(f"Transcripción guardada: {transcription_id} para {recording_filename}")
                return transcription_id
            else:
                logger.warning(f"Supabase no confirmó guardado de transcripción para {recording_filename}")
                return None
        
        except Exception as e:
            logger.error(f"Error al guardar transcripción: {type(e).__name__} - {str(e)}")
            return None
    
    @staticmethod
    def delete(transcription_id: str) -> bool:
        """Elimina una transcripción"""
        try:
            db = init_supabase()
            if not db:
                return False
            
            response = db.table("transcriptions").delete().eq("id", transcription_id).execute()
            if response:
                logger.info(f"Transcripción eliminada: {transcription_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al eliminar transcripción {transcription_id}: {type(e).__name__} - {str(e)}")
            return False


class OpportunityService:
    """Servicio para gestionar oportunidades"""
    
    @staticmethod
    def get_by_recording(recording_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las oportunidades de un recording"""
        try:
            db = init_supabase()
            if not db:
                logger.warning(f"BD no disponible para obtener oportunidades")
                return []
            
            response = db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
            if response and response.data:
                logger.debug(f"Cargadas {len(response.data)} oportunidades para recording {recording_id}")
                return response.data
            return []
        except Exception as e:
            logger.error(f"Error al obtener oportunidades: {type(e).__name__} - {str(e)}")
            return []
    
    @staticmethod
    def save(recording_id: str, opportunity_dict: Dict[str, Any]) -> Optional[str]:
        """Guarda una oportunidad"""
        try:
            db = init_supabase()
            if not db:
                logger.warning("BD no disponible para guardar oportunidad")
                return None
            
            data = {
                "recording_id": recording_id,
                "title": opportunity_dict.get("keyword", "Oportunidad"),
                "description": opportunity_dict.get("full_context", ""),
                "status": opportunity_dict.get("status", "new"),
                "priority": opportunity_dict.get("priority", "Medium"),
                "notes": opportunity_dict.get("notes", ""),
                "created_at": datetime.now().isoformat()
            }
            
            response = db.table("opportunities").insert(data).execute()
            
            if response and response.data and len(response.data) > 0:
                opportunity_id = response.data[0].get("id")
                logger.info(f"Oportunidad guardada: {opportunity_id}")
                return opportunity_id
            
            logger.warning("Supabase no confirmó guardado de oportunidad")
            return None
        except Exception as e:
            logger.error(f"Error al guardar oportunidad: {type(e).__name__} - {str(e)}")
            return None
    
    @staticmethod
    def update(opportunity_id: str, update_dict: Dict[str, Any]) -> bool:
        """Actualiza una oportunidad"""
        try:
            db = init_supabase()
            if not db:
                logger.warning("BD no disponible para actualizar oportunidad")
                return False
            
            response = db.table("opportunities").update(update_dict).eq("id", opportunity_id).execute()
            
            if response and len(response.data) > 0:
                logger.info(f"Oportunidad actualizada: {opportunity_id}")
                return True
            
            logger.warning(f"Supabase no confirmó actualización de oportunidad {opportunity_id}")
            return False
        except Exception as e:
            logger.error(f"Error al actualizar oportunidad {opportunity_id}: {type(e).__name__} - {str(e)}")
            return False
    
    @staticmethod
    def delete(opportunity_id: str) -> bool:
        """Elimina una oportunidad"""
        try:
            db = init_supabase()
            if not db:
                logger.warning("BD no disponible para eliminar oportunidad")
                return False
            
            response = db.table("opportunities").delete().eq("id", opportunity_id).execute()
            if response:
                logger.info(f"Oportunidad eliminada: {opportunity_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al eliminar oportunidad {opportunity_id}: {type(e).__name__} - {str(e)}")
            return False
