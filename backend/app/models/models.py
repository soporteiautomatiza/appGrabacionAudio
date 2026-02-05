"""
Modelos SQLAlchemy para la base de datos
Define la estructura de datos y relaciones
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    """Modelo de Usuario"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    audios = relationship("Audio", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"

class Audio(Base):
    """Modelo de Audio grabado"""
    __tablename__ = "audios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # en bytes
    duration = Column(Integer)  # en segundos
    status = Column(String(50), default="uploaded")  # uploaded, transcribing, completed, error
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="audios")
    transcription = relationship("Transcription", back_populates="audio", uselist=False, cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="audio", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Audio {self.filename}>"

class Transcription(Base):
    """Modelo de Transcripción de Audio"""
    __tablename__ = "transcriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    audio_id = Column(Integer, ForeignKey("audios.id", ondelete="CASCADE"), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    keywords = Column(JSON, default=[])  # Lista de palabras clave extraídas
    confidence = Column(Integer, default=0)  # 0-100
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    audio = relationship("Audio", back_populates="transcription")
    
    def __repr__(self):
        return f"<Transcription audio_id={self.audio_id}>"

class Opportunity(Base):
    """Modelo de Oportunidad/Ticket extraído de transcripciones"""
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    audio_id = Column(Integer, ForeignKey("audios.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String(255), nullable=False)
    context_before = Column(Text)
    context_after = Column(Text)
    full_context = Column(Text)
    status = Column(String(50), default="new")  # new, reviewed, closed
    notes = Column(Text)
    data = Column(JSON, default={})  # Datos adicionales en JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    audio = relationship("Audio", back_populates="opportunities")
    
    def __repr__(self):
        return f"<Opportunity {self.keyword}>"

class ChatMessage(Base):
    """Modelo de Mensaje de Chat"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)  # "user" o "assistant"
    content = Column(Text, nullable=False)
    context_audio_id = Column(Integer, ForeignKey("audios.id"), nullable=True)  # Audio usado como contexto
    context_text = Column(Text)  # Fragmento de transcripción usado como contexto
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="chat_messages")
    
    def __repr__(self):
        return f"<ChatMessage user_id={self.user_id} role={self.role}>"
