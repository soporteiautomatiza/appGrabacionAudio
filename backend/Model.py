import google.generativeai as genai
from pathlib import Path
import sys

# Agregar ruta padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, CHAT_MODEL
from logger import get_logger

logger = get_logger(__name__)

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)


class Model:
    """Modelo de chat inteligente usando Google Gemini"""
    
    def __init__(self):
        """Inicializa el modelo de chat"""
        self.model = genai.GenerativeModel(CHAT_MODEL)
        logger.info("Modelo de chat inicializado")
    
    def call_model(self, question, context, keywords=None):
        """
        Genera una respuesta basada en una pregunta y contexto.
        
        Args:
            question (str): Pregunta del usuario
            context (str): Contexto (transcripción del audio)
            keywords (dict, optional): Palabras clave (dict o list)
            
        Returns:
            str: Respuesta generada por el modelo
        """
        try:
            # Construir sección de palabras clave
            keywords_section = ""
            if keywords:
                if isinstance(keywords, dict):
                    keywords_list = list(keywords.keys())
                else:
                    keywords_list = keywords
                
                if len(keywords_list) > 0:
                    keywords_section = f"\n\n📌 PALABRAS CLAVE IMPORTANTES:\n" + ", ".join(keywords_list)
                    keywords_section += "\nTen en cuenta estas palabras clave al responder y organizalas en tu respuesta si es relevante."
            
            prompt = f"""Eres un asistente inteligente que ayuda a responder preguntas basado en el siguiente contexto:

{context}{keywords_section}

Si no sabes la respuesta basándote en el contexto, responde 'No lo sé'. Sé preciso y conciso en tus respuestas.
Si es posible, destaca las palabras clave en tu respuesta.

Pregunta: {question}"""
            
            logger.info(f"Generando respuesta para pregunta: {question[:50]}...")
            response = self.model.generate_content(prompt)
            logger.info(f"Respuesta generada: {len(response.text)} caracteres")
            return response.text
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            raise
