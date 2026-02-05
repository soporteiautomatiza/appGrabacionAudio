"""
Rutas de Chat: enviar mensaje, obtener historial de chat
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, ChatMessage, Audio, Transcription
from app.schemas.schemas import ChatMessageRequest, ChatMessageResponse
from app.services.chat import ChatService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send", response_model=ChatMessageResponse)
async def send_message(
    message: ChatMessageRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía una pregunta y recibe respuesta de Gemini
    
    - **content**: Pregunta del usuario
    - **audio_id** (opcional): ID del audio a usar como contexto
    """
    try:
        user_id = int(current_user["user_id"])
        
        # Verificar que el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        # Guardar mensaje del usuario
        user_message = ChatMessage(
            user_id=user_id,
            role="user",
            content=message.content,
            context_audio_id=message.audio_id
        )
        
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        logger.info(f"Mensaje de usuario guardado: {user_message.id}")
        
        # Generar contexto si hay audio
        context = ""
        keywords = []
        
        if message.audio_id:
            # Obtener transcripción del audio
            audio = db.query(Audio).filter(
                Audio.id == message.audio_id,
                Audio.user_id == user_id
            ).first()
            
            if audio and audio.transcription:
                context = audio.transcription.text
                keywords = audio.transcription.keywords or []
                
                # Guardar fragmento de contexto en el mensaje
                user_message.context_text = context[:500]
                db.commit()
        else:
            # Si no hay audio específico, usar el contexto de todos los audios del usuario
            audios = db.query(Audio).filter(Audio.user_id == user_id).all()
            context_parts = []
            
            for audio in audios:
                if audio.transcription:
                    context_parts.append(audio.transcription.text)
                    if not keywords and audio.transcription.keywords:
                        keywords = audio.transcription.keywords[:5]
            
            context = " ".join(context_parts)[:10000]  # Limitar contexto total
        
        if not context:
            context = "No hay transcripciones disponibles como contexto."
        
        # Llamar al servicio de chat
        logger.info(f"Generando respuesta del asistente...")
        response_text = await ChatService.get_response(
            question=message.content,
            context=context,
            keywords=keywords
        )
        
        # Guardar respuesta del asistente
        assistant_message = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=response_text,
            context_audio_id=message.audio_id
        )
        
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        logger.info(f"Respuesta guardada: {assistant_message.id}")
        
        # Retornar el mensaje del usuario (el frontend manejará mostrar ambos)
        return user_message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al enviar mensaje: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el mensaje"
        )

@router.get("/history", response_model=list[ChatMessageResponse])
async def get_chat_history(
    audio_id: int = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de chat del usuario
    
    - **audio_id** (opcional): Filtrar por audio específico
    - **limit**: Número máximo de mensajes (default 100)
    """
    try:
        user_id = int(current_user["user_id"])
        
        query = db.query(ChatMessage).filter(ChatMessage.user_id == user_id)
        
        if audio_id:
            query = query.filter(ChatMessage.context_audio_id == audio_id)
        
        messages = query.order_by(ChatMessage.created_at.desc()).limit(limit).all()
        messages.reverse()  # Orden cronológico
        
        logger.info(f"Historial {len(messages)} mensajes obtenido para usuario {user_id}")
        
        return messages
        
    except Exception as e:
        logger.error(f"Error obteniendo historial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener historial de chat"
        )

@router.get("/response/{message_id}", response_model=ChatMessageResponse)
async def get_assistant_response(
    message_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la respuesta del asistente para un mensaje específico
    (usado para polls/continuación de conversación)
    """
    try:
        user_id = int(current_user["user_id"])
        
        # Obtener el siguiente mensaje del asistente después del mensaje especificado
        user_message = db.query(ChatMessage).filter(
            ChatMessage.id == message_id,
            ChatMessage.user_id == user_id
        ).first()
        
        if not user_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Buscar respuesta del asistente (siguiente mensaje)
        assistant_response = db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id,
            ChatMessage.role == "assistant",
            ChatMessage.created_at > user_message.created_at
        ).order_by(ChatMessage.created_at).first()
        
        if not assistant_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Respuesta no encontrada"
            )
        
        return assistant_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo respuesta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener respuesta"
        )
