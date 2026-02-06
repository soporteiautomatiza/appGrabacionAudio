"""
Opportunity Service - Lógica de negocio para oportunidades
"""
from typing import List, Dict, Any, Optional
from backend.database.repositories import OpportunityRepository, RecordingRepository

class OpportunityService:
    """Servicio de lógica de negocio para oportunidades"""
    
    def __init__(self):
        self.opportunity_repo = OpportunityRepository()
        self.recording_repo = RecordingRepository()
    
    def create_opportunity(self, recording_id: int, title: str, description: str = "") -> Optional[int]:
        """
        Crea una oportunidad asociada a un recording
        Returns: ID de la oportunidad creada
        """
        try:
            # Validar que el recording existe
            recording = self.recording_repo.get_by_id(recording_id)
            if not recording:
                raise ValueError(f"Recording con ID {recording_id} no existe")
            
            opportunity_id = self.opportunity_repo.create(recording_id, title, description)
            return opportunity_id
        except Exception as e:
            print(f"Error en OpportunityService.create_opportunity: {e}")
            return None
    
    def get_opportunities_by_recording(self, recording_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las oportunidades de un recording"""
        try:
            return self.opportunity_repo.get_by_recording(recording_id)
        except Exception as e:
            print(f"Error en OpportunityService.get_opportunities_by_recording: {e}")
            return []
    
    def get_all_opportunities(self) -> List[Dict[str, Any]]:
        """Obtiene todas las oportunidades"""
        try:
            return self.opportunity_repo.get_all()
        except Exception as e:
            print(f"Error en OpportunityService.get_all_opportunities: {e}")
            return []
    
    def extract_opportunities_from_keywords(
        self, 
        recording_id: int, 
        transcription: str, 
        keywords: Dict[str, Any]
    ) -> List[int]:
        """
        Extrae oportunidades de una transcripción basadas en palabras clave
        Returns: Lista de IDs de oportunidades creadas
        """
        created_ids = []
        
        try:
            if not keywords:
                return created_ids
            
            words = transcription.lower().split()
            
            for keyword in keywords.keys():
                keyword_lower = keyword.lower()
                occurrence_count = 0
                
                for i, word in enumerate(words):
                    if keyword_lower in word:
                        occurrence_count += 1
                        
                        # Extraer contexto
                        context_window = 15
                        start = max(0, i - context_window)
                        end = min(len(words), i + context_window + 1)
                        
                        context = " ".join(words[start:end])
                        title = f"{keyword} (ocurrencia {occurrence_count})"
                        
                        # Crear oportunidad
                        opp_id = self.create_opportunity(
                            recording_id,
                            title,
                            context
                        )
                        
                        if opp_id:
                            created_ids.append(opp_id)
            
            return created_ids
        
        except Exception as e:
            print(f"Error en OpportunityService.extract_opportunities_from_keywords: {e}")
            return created_ids
