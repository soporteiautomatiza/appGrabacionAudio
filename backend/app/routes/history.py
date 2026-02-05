"""
Rutas de Historial: obtener todo el historial del usuario
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Audio, ChatMessage
from app.schemas.schemas import HistoryResponse, AudioWithTranscription, ChatMessageResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=HistoryResponse)
async def get_user_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todo el historial del usuario:
    - Todos los audios con sus transcripciones y oportunidades
    - Historial de chat completo
    """
    try:
        user_id = int(current_user["user_id"])
        
        # Verificar que el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Obtener todos los audios del usuario
        audios = db.query(Audio).filter(
            Audio.user_id == user_id
        ).order_by(Audio.created_at.desc()).all()
        
        # Obtener historial de chat
        chat_messages = db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(ChatMessage.created_at.desc()).limit(100).all()
        
        chat_messages.reverse()  # Orden cronológico
        
        logger.info(f"Historial obtenido para usuario {user_id}: {len(audios)} audios, {len(chat_messages)} mensajes")
        
        return HistoryResponse(
            audios=audios,
            chat_messages=chat_messages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo historial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener historial"
        )

@router.get("/summary", response_model=dict)
async def get_history_summary(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un resumen del historial del usuario:
    - Número total de audios
    - Número de transcripciones completadas
    - Número de oportunidades identificadas
    - Últimos mensajes de chat
    """
    try:
        user_id = int(current_user["user_id"])
        
        # Contar audios
        total_audios = db.query(Audio).filter(Audio.user_id == user_id).count()
        completed_audios = db.query(Audio).filter(
            Audio.user_id == user_id,
            Audio.status == "completed"
        ).count()
        
        # Contar transcripciones
        transcriptions = db.query(Audio).filter(
            Audio.user_id == user_id,
            Audio.transcription != None
        ).count()
        
        # Contar oportunidades
        from app.models.models import Opportunity
        opportunities = db.query(Opportunity).join(Audio).filter(
            Audio.user_id == user_id
        ).count()
        
        # Contar mensajes de chat
        chat_messages = db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).count()
        
        logger.info(f"Resumen de historial para usuario {user_id}")
        
        return {
            "total_audios": total_audios,
            "completed_audios": completed_audios,
            "transcriptions": transcriptions,
            "opportunities": opportunities,
            "chat_messages": chat_messages
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo resumen: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener resumen"
        )
