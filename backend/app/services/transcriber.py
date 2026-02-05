"""
Servicio de Transcripción usando Google Gemini API
"""

import google.generativeai as genai
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Configurar Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    transcriber_model = genai.GenerativeModel("gemini-2.0-flash")
else:
    logger.warning("GEMINI_API_KEY no configurada")
    transcriber_model = None

class TranscriberService:
    """Servicio para transcribir audios usando Gemini"""
    
    @staticmethod
    async def transcribe_audio(audio_path: str) -> dict:
        """
        Transcribe un archivo de audio usando Google Gemini API
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            dict con transcripción y metadata
        """
        if not transcriber_model:
            raise ValueError("Gemini API no configurada. Verifique GEMINI_API_KEY")
        
        try:
            # Determinar tipo MIME según extensión
            extension = audio_path.lower().split('.')[-1]
            mime_types = {
                'mp3': 'audio/mpeg',
                'wav': 'audio/wav',
                'm4a': 'audio/mp4',
                'flac': 'audio/flac',
                'webm': 'audio/webm',
                'ogg': 'audio/ogg',
            }
            mime_type = mime_types.get(extension, 'audio/mpeg')
            
            # Subir archivo a Gemini
            logger.info(f"Subiendo archivo de audio: {audio_path}")
            audio_file = genai.upload_file(audio_path, mime_type=mime_type)
            
            # Transcribir usando Gemini
            logger.info(f"Transcribiendo audio con Gemini...")
            prompt = "Transcribe el siguiente audio en texto. Devuelve solo el texto transcrito sin explicaciones adicionales."
            
            response = transcriber_model.generate_content([prompt, audio_file])
            transcript_text = response.text
            
            # Limpiar archivo subido
            genai.delete_file(audio_file.name)
            
            logger.info(f"Transcripción completada exitosamente")
            
            return {
                "success": True,
                "text": transcript_text,
                "confidence": 95  # Gemini no proporciona confianza, default alto
            }
            
        except Exception as e:
            logger.error(f"Error en transcripción: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "text": ""
            }
    
    @staticmethod
    def extract_keywords(transcript: str) -> list:
        """
        Extrae palabras clave del texto transcrito
        
        Args:
            transcript: Texto transcrito
            
        Returns:
            Lista de palabras clave relevantes
        """
        try:
            if not transcriber_model:
                return []
            
            prompt = f"""Analiza el siguiente texto y extrae las 5-10 palabras clave más importantes.
            Devuelve solo las palabras clave separadas por comas, sin explicaciones adicionales.
            
            Texto:
            {transcript[:2000]}"""  # Limitar a 2000 caracteres
            
            response = transcriber_model.generate_content(prompt)
            keywords_text = response.text.strip()
            keywords = [k.strip() for k in keywords_text.split(',')]
            
            return [k for k in keywords if k]  # Filtrar vacíos
            
        except Exception as e:
            logger.error(f"Error extrayendo keywords: {str(e)}")
            return []
