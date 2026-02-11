"""Transcriber.py - Transcribidor de audio con Gemini (~45 líneas)"""
import google.generativeai as genai
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, TRANSCRIPTION_MODEL, MIME_TYPES
from logger import get_logger

logger = get_logger(__name__)
genai.configure(api_key=GEMINI_API_KEY)

class Transcriber:
    def __init__(self):
        self.model = genai.GenerativeModel(TRANSCRIPTION_MODEL)
        logger.info("✓ Transcriber initialized")
    
    def transcript_audio(self, audio_path: str):
        """Transcribe un archivo de audio"""
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
            
            ext = audio_path.lower().split('.')[-1]
            mime_type = MIME_TYPES.get(ext, 'audio/mpeg')
            
            logger.info(f"Transcribiendo: {audio_path} ({mime_type})")
            audio_file = genai.upload_file(audio_path, mime_type=mime_type)
            
            prompt = "Transcribe el audio en texto. Solo devuelve el texto sin explicaciones."
            response = self.model.generate_content([prompt, audio_file])
            
            logger.info(f"✓ Transcripción: {len(response.text)} caracteres")
            
            class Result:
                def __init__(self, text):
                    self.text = text
            
            return Result(response.text)
        
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {audio_path}")
            raise
        
        except Exception as e:
            logger.error(f"transcript_audio: {type(e).__name__} - {str(e)}")
            raise

