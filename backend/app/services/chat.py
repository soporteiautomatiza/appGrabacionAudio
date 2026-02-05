"""
Servicio de Chat usando Google Gemini API
"""

import google.generativeai as genai
from app.core.config import get_settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)
settings = get_settings()

# Configurar Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    chat_model = genai.GenerativeModel("gemini-2.0-flash")
else:
    logger.warning("GEMINI_API_KEY no configurada")
    chat_model = None

class ChatService:
    """Servicio para generar respuestas de chat usando Gemini"""
    
    @staticmethod
    async def get_response(
        question: str,
        context: str,
        keywords: Optional[list] = None
    ) -> str:
        """
        Genera una respuesta a una pregunta usando el contexto de transcripciones
        
        Args:
            question: Pregunta del usuario
            context: Contexto (texto de transcripción)
            keywords: Lista de palabras clave relevantes
            
        Returns:
            Respuesta generada por Gemini
        """
        if not chat_model:
            raise ValueError("Gemini API no configurada. Verifique GEMINI_API_KEY")
        
        try:
            # Construir prompt con contexto
            keywords_section = ""
            if keywords and len(keywords) > 0:
                keywords_section = f"\n\n📌 PALABRAS CLAVE IMPORTANTES: {', '.join(keywords[:10])}\nTen en cuenta estas palabras clave al responder y resáltalas si es relevante."
            
            prompt = f"""Eres un asistente inteligente que ayuda a responder preguntas basado en el siguiente contexto de grabaciones de audio:

CONTEXTO:
{context[:5000]}  # Limitar contexto a 5000 caracteres

{keywords_section}

Si la pregunta no está relacionada con el contexto, responde educadamente que necesitas información más relevante.
Sé preciso, conciso y profesional en tus respuestas.

PREGUNTA DEL USUARIO: {question}"""
            
            logger.info(f"Generando respuesta para pregunta: {question[:50]}...")
            response = chat_model.generate_content(prompt)
            
            logger.info("Respuesta generada exitosamente")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {str(e)}")
            return f"Error al procesar su pregunta: {str(e)}"
