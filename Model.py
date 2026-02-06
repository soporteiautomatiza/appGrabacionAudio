import google.generativeai as genai
import os
from dotenv import load_dotenv
from backend.config import Config

# Carga las variables de entorno desde .env
load_dotenv()

class Model:
  def __init__(self):
    # Lee dinámicamente la API key (desde st.secrets o .env)
    GEMINI_API_KEY = Config.get_gemini_api_key()
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY no esta configurada en st.secrets ni en .env")
    genai.configure(api_key=GEMINI_API_KEY)
    self.model = genai.GenerativeModel('gemini-2.0-flash')
  
  def call_model(self, question, context, keywords=None):
    # Construir sección de palabras clave
    keywords_section = ""
    if keywords and len(keywords) > 0:
      keywords_section = f"\n\n📌 PALABRAS CLAVE IMPORTANTES: {', '.join(keywords)}\nTen en cuenta estas palabras clave al responder y organizalas en tu respuesta si es relevante."
    
    prompt = f"""Eres un asistente inteligente que ayuda a responder preguntas basado en el siguiente contexto:

{context}{keywords_section}

Si no sabes la respuesta basándote en el contexto, responde 'No lo sé'. Sé preciso y conciso en tus respuestas.
Si es posible, destaca las palabras clave en tu respuesta.

Pregunta: {question}"""
    
    response = self.model.generate_content(prompt)
    return response.text
