import google.generativeai as genai
from pathlib import Path
import sys

# Agregar ruta padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, TRANSCRIPTION_MODEL, MIME_TYPES
from logger import get_logger

logger = get_logger(__name__)

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

class Transcriber:
    """Transcribidor de audio usando Google Gemini"""
    
    def __init__(self):
        """Inicializa el transcribidor"""
        self.model = genai.GenerativeModel(TRANSCRIPTION_MODEL)
        logger.info("Transcriber inicializado")
    
    def transcript_audio(self, audio_path):
        """
        Transcribe un archivo de audio.
        
        Args:
            audio_path (str): Ruta al archivo de audio
            
        Returns:
            TranscriptionResult: Objeto con atributo 'text' conteniendo la transcripción
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado
        """
        try:
            # Validar que el archivo existe
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
            
            # Obtener extension y MIME type
            extension = audio_path.lower().split('.')[-1]
            mime_type = MIME_TYPES.get(extension, 'audio/mpeg')
            
            logger.info(f"Transcribiendo archivo: {audio_path} (tipo: {mime_type})")
            
            # Subir el archivo a Gemini
            audio_file_obj = genai.upload_file(audio_path, mime_type=mime_type)
            
            # Transcribir usando Gemini
            prompt = "Transcribe el siguiente audio en texto. Devuelve solo el texto transcrito sin explicaciones adicionales."
            response = self.model.generate_content([prompt, audio_file_obj])
            
            # Crear objeto con resultado
            class TranscriptionResult:
                def __init__(self, text):
                    self.text = text
            
            result = TranscriptionResult(response.text)
            logger.info(f"Transcripción completada: {len(response.text)} caracteres")
            return result
            
        except FileNotFoundError as e:
            logger.error(f"Error: Archivo no encontrado - {audio_path}")
            raise
        except Exception as e:
            logger.error(f"Error al transcribir: {str(e)}")
            raise

