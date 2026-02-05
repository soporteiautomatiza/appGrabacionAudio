"""
Esquemas Pydantic para validación de datos en requests/responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    """Schema para registro de nuevo usuario"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=255)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "full_name": "Juan Pérez",
                "password": "SecurePass123"
            }
        }

class UserLogin(BaseModel):
    """Schema para login de usuario"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "SecurePass123"
            }
        }

class TokenResponse(BaseModel):
    """Schema de respuesta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    """Schema de respuesta de usuario"""
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "usuario@example.com",
                "full_name": "Juan Pérez",
                "is_active": True,
                "created_at": "2026-02-05T10:00:00"
            }
        }

class AudioResponse(BaseModel):
    """Schema de respuesta de audio"""
    id: int
    filename: str
    file_size: Optional[int]
    duration: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TranscriptionResponse(BaseModel):
    """Schema de respuesta de transcripción"""
    id: int
    audio_id: int
    text: str
    keywords: List[str]
    confidence: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class OpportunityResponse(BaseModel):
    """Schema de respuesta de oportunidad"""
    id: int
    audio_id: int
    keyword: str
    full_context: str
    status: str
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageRequest(BaseModel):
    """Schema para request de mensaje de chat"""
    content: str = Field(..., min_length=1, max_length=5000)
    audio_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "¿Cuáles fueron los temas principales mencionados?",
                "audio_id": 1
            }
        }

class ChatMessageResponse(BaseModel):
    """Schema de respuesta de mensaje de chat"""
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AudioWithTranscription(BaseModel):
    """Schema de audio con su transcripción"""
    id: int
    filename: str
    status: str
    created_at: datetime
    transcription: Optional[TranscriptionResponse] = None
    opportunities: List[OpportunityResponse] = []
    
    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    """Schema de respuesta del historial del usuario"""
    audios: List[AudioWithTranscription]
    chat_messages: List[ChatMessageResponse]
    
    class Config:
        from_attributes = True
