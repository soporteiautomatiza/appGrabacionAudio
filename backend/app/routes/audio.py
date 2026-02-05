"""
Rutas de Gestión de Audios: upload, listado, eliminación
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import get_settings
from app.models.models import User, Audio, Transcription
from app.schemas.schemas import AudioResponse, AudioWithTranscription
from app.services.transcriber import TranscriberService
from app.services.opportunities import OpportunitiesService
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audios", tags=["audios"])
settings = get_settings()

# Crear directorio de uploads si no existe
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)

@router.post("/upload", response_model=AudioResponse, status_code=status.HTTP_201_CREATED)
async def upload_audio(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sube un archivo de audio y dispara la transcripción automática
    
    - **file**: Archivo de audio (mp3, wav, m4a, flac, webm, ogg)
    
    El archivo se procesa y transcribe automáticamente en background
    """
    try:
        user_id = int(current_user["user_id"])
        
        # Validar que el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        # Validar formato de archivo
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in settings.ALLOWED_AUDIO_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato no permitido. Formatos válidos: {', '.join(settings.ALLOWED_AUDIO_FORMATS)}"
            )
        
        # Leer archivo
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validar tamaño de archivo
        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
                detail=f"Archivo demasiado grande. Máximo: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Guardar archivo con nombre único
        from datetime import datetime
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_{user_id}_{timestamp}.{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Crear registro de audio en BD
        audio = Audio(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            status="uploaded"
        )
        
        db.add(audio)
        db.commit()
        db.refresh(audio)
        
        logger.info(f"Audio guardado: {filename} para usuario {user_id}")
        
        # Transcribir audio (asincrónico en un background task real)
        await transcribe_audio_background(audio.id, file_path, db)
        
        return AudioResponse(
            id=audio.id,
            filename=audio.filename,
            file_size=audio.file_size,
            duration=audio.duration,
            status=audio.status,
            created_at=audio.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al subir audio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el archivo de audio"
        )

async def transcribe_audio_background(audio_id: int, file_path: str, db: Session):
    """Transcribe un audio en background"""
    try:
        # Buscar audio
        audio = db.query(Audio).filter(Audio.id == audio_id).first()
        if not audio:
            logger.error(f"Audio no encontrado: {audio_id}")
            return
        
        # Actualizar estado a transcribiendo
        audio.status = "transcribing"
        db.commit()
        
        logger.info(f"Iniciando transcripción de audio: {audio_id}")
        
        # Transcribir
        result = await TranscriberService.transcribe_audio(file_path)
        
        if result["success"]:
            # Extraer keywords
            keywords = TranscriberService.extract_keywords(result["text"])
            
            # Crear transcripción
            transcription = Transcription(
                audio_id=audio_id,
                text=result["text"],
                keywords=keywords,
                confidence=result.get("confidence", 95)
            )
            
            # Extraer oportunidades
            opportunities = OpportunitiesService.extract_opportunities(
                result["text"],
                keywords
            )
            
            # Guardar todo en BD
            from app.models.models import Opportunity
            audio.status = "completed"
            audio.transcription = transcription
            
            for opp_data in opportunities:
                opportunity = Opportunity(
                    audio_id=audio_id,
                    keyword=opp_data["keyword"],
                    context_before=opp_data["context_before"],
                    context_after=opp_data["context_after"],
                    full_context=opp_data["full_context"],
                    status=opp_data["status"],
                    notes=opp_data["notes"]
                )
                db.add(opportunity)
            
            db.commit()
            logger.info(f"Transcripción completada para audio: {audio_id}")
            
        else:
            audio.status = "error"
            audio.error_message = result.get("error", "Error desconocido")
            db.commit()
            logger.error(f"Error transcribiendo audio {audio_id}: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Error en transcripción de background: {str(e)}")
        audio.status = "error"
        audio.error_message = str(e)
        db.commit()

@router.get("/", response_model=list[AudioWithTranscription])
async def get_user_audios(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene todos los audios del usuario actual"""
    try:
        user_id = int(current_user["user_id"])
        
        audios = db.query(Audio).filter(Audio.user_id == user_id).order_by(Audio.created_at.desc()).all()
        
        return audios
        
    except Exception as e:
        logger.error(f"Error obteniendo audios: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener audios"
        )

@router.get("/{audio_id}", response_model=AudioWithTranscription)
async def get_audio(
    audio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene un audio específico con su transcripción y oportunidades"""
    try:
        user_id = int(current_user["user_id"])
        
        audio = db.query(Audio).filter(
            Audio.id == audio_id,
            Audio.user_id == user_id
        ).first()
        
        if not audio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audio no encontrado"
            )
        
        return audio
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo audio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener audio"
        )

@router.delete("/{audio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audio(
    audio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina un audio y todos sus registros asociados"""
    try:
        user_id = int(current_user["user_id"])
        
        audio = db.query(Audio).filter(
            Audio.id == audio_id,
            Audio.user_id == user_id
        ).first()
        
        if not audio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audio no encontrado"
            )
        
        # Eliminar archivo físico
        if os.path.exists(audio.file_path):
            os.remove(audio.file_path)
            logger.info(f"Archivo eliminado: {audio.file_path}")
        
        # Eliminar registro de BD (cascade eliminará transcripciones y oportunidades)
        db.delete(audio)
        db.commit()
        
        logger.info(f"Audio {audio_id} eliminado por usuario {user_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando audio: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar audio"
        )
