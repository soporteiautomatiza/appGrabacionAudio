"""
Audio Service - Lógica de negocio para grabaciones
"""
from typing import List, Optional, Dict, Any
from backend.database.repositories import RecordingRepository

class AudioService:
    """Servicio de lógica de negocio para audios"""
    
    def __init__(self):
        self.repository = RecordingRepository()
    
    def save_recording(self, filename: str, filepath: str) -> Optional[int]:
        """
        Guarda una grabación en la BD
        Returns: ID del recording creado, None si falla
        """
        try:
            # Validar que el repository esté conectado
            if self.repository.db is None:
                print("ERROR: No hay conexión a Supabase")
                return None
            
            recording_id = self.repository.create(filename, filepath)
            if recording_id is None:
                print(f"ERROR: El repository.create() retornó None para {filename}")
            else:
                print(f"SUCCESS: Recording guardado con ID {recording_id}")
            return recording_id
        except Exception as e:
            print(f"ERROR en AudioService.save_recording: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_all_recordings(self) -> List[Dict[str, Any]]:
        """Obtiene todas las grabaciones"""
        try:
            if self.repository.db is None:
                print("ERROR: No hay conexión a Supabase en get_all_recordings")
                return []
            recordings = self.repository.get_all()
            print(f"SUCCESS: Se obtuvieron {len(recordings) if recordings else 0} grabaciones")
            return recordings or []
        except Exception as e:
            print(f"ERROR en AudioService.get_all_recordings: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_recording(self, recording_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una grabación específica"""
        try:
            return self.repository.get_by_id(recording_id)
        except Exception as e:
            print(f"Error en AudioService.get_recording: {e}")
            return None
    
    def get_recording_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """Obtiene una grabación por nombre de archivo"""
        try:
            return self.repository.get_by_filename(filename)
        except Exception as e:
            print(f"Error en AudioService.get_recording_by_filename: {e}")
            return None
    
    def delete_recording(self, recording_id: int) -> bool:
        """
        Elimina una grabación y todas sus dependencias
        (transcripciones, oportunidades)
        """
        try:
            success = self.repository.delete(recording_id)
            return success
        except Exception as e:
            print(f"Error en AudioService.delete_recording: {e}")
            return False
