"""Model.py - Chat con Google Gemini (~50 líneas)"""
import google.generativeai as genai
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, CHAT_MODEL
from logger import get_logger

logger = get_logger(__name__)
genai.configure(api_key=GEMINI_API_KEY)

class Model:
    def __init__(self):
        self.model = genai.GenerativeModel(CHAT_MODEL)
        logger.info("✓ Chat model initialized")
    
    def call_model(self, question: str, context: str, keywords=None) -> str:
        """Genera respuesta basada en pregunta y contexto"""
        try:
            keywords_section = ""
            if keywords:
                kw_list = list(keywords.keys()) if isinstance(keywords, dict) else keywords
                if kw_list:
                    keywords_section = f"\n\n📌 KEYWORDS:\n{', '.join(kw_list)}\nUsa estas keywords en tu respuesta si es relevante."
            
            prompt = f"""Eres un asistente que responde basado en el contexto:

{context}{keywords_section}

Si no lo sabes, responde 'No lo sé'. Sé preciso y conciso.

Pregunta: {question}"""
            
            logger.info(f"Generando respuesta para: {question[:50]}...")
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            logger.error(f"call_model: {type(e).__name__} - {str(e)}")
            raise
