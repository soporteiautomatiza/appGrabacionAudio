import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")
genai.configure(api_key=GEMINI_API_KEY)

class Transcriber:
  def __init__(self):
    self.transcription = None

  def transcript_audio(self, audio_path):
    if self.transcription is None:
      # Lee el archivo de audio
      with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
      
      # Determina el tipo MIME basado en la extensión
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
      
      # Sube el archivo y obtén la URI
      audio_file_obj = genai.upload_file(audio_path, mime_type=mime_type)
      
      # Usa Gemini para transcribir el audio
      model = genai.GenerativeModel('gemini-2.0-flash')
      prompt = "Transcribe el siguiente audio en texto. Devuelve solo el texto transcrito sin explicaciones adicionales."
      
      response = model.generate_content([
        prompt,
        audio_file_obj
      ])
      
      # Crea un objeto simple con atributo 'text' para mantener compatibilidad
      class TranscriptionResult:
        def __init__(self, text):
          self.text = text
      
      self.transcription = TranscriptionResult(response.text)
    
    return self.transcription
