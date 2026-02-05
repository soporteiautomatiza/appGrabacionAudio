"""
Servicio de Gestión de Oportunidades/Tickets
"""

from typing import List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OpportunitiesService:
    """Servicio para extraer y gestionar oportunidades de transcripciones"""
    
    @staticmethod
    def extract_opportunities(
        transcript: str,
        keywords: List[str]
    ) -> List[dict]:
        """
        Extrae oportunidades de un texto transcrito basado en palabras clave
        
        Args:
            transcript: Texto transcrito
            keywords: Lista de palabras clave a buscar
            
        Returns:
            Lista de oportunidades encontradas
        """
        opportunities = []
        
        if not keywords:
            logger.info("No hay palabras clave para extraer oportunidades")
            return opportunities
        
        try:
            # Dividir transcripción en palabras
            words = transcript.lower().split()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Buscar keyword en la transcripción
                if keyword_lower in transcript.lower():
                    # Encontrar índice de la palabra
                    for i, word in enumerate(words):
                        if keyword_lower in word:
                            # Extraer contexto: 5 palabras antes y después
                            start = max(0, i - 5)
                            end = min(len(words), i + 6)
                            
                            context_before = " ".join(words[start:i])
                            context_after = " ".join(words[i+1:end])
                            full_context = f"{context_before} **{keyword}** {context_after}"
                            
                            opportunity = {
                                "keyword": keyword,
                                "context_before": context_before,
                                "context_after": context_after,
                                "full_context": full_context,
                                "status": "new",
                                "notes": "",
                                "created_at": datetime.utcnow().isoformat()
                            }
                            
                            opportunities.append(opportunity)
                            logger.info(f"Oportunidad extraída: {keyword}")
                            break
            
            logger.info(f"Se extrajeron {len(opportunities)} oportunidades")
            return opportunities
            
        except Exception as e:
            logger.error(f"Error extrayendo oportunidades: {str(e)}")
            return []
    
    @staticmethod
    def update_opportunity_notes(
        opportunity_id: int,
        notes: str
    ) -> dict:
        """
        Actualiza las notas de una oportunidad
        
        Args:
            opportunity_id: ID de la oportunidad
            notes: Nuevas notas
            
        Returns:
            Oportunidad actualizada
        """
        try:
            logger.info(f"Actualizando notas de oportunidad {opportunity_id}")
            return {
                "id": opportunity_id,
                "notes": notes,
                "updated_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error actualizando oportunidad: {str(e)}")
            raise
