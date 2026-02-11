"""Model.py - Chat con Google Gemini con rate limiting y validación"""
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
        """Genera respuesta basada en pregunta y contexto
        
        Incluye:
        - Validación de entrada
        - Rate limiting
        - Manejo de errores
        """
        try:
            # ===== VALIDACIÓN DE ENTRADA =====
            valid, error = validator.validate_transcription_text(context)
            if not valid:
                logger.error(f"Context inválido: {error}")
                raise ValueError(f"Contexto inválido: {error}")
            
            valid, error = validator.validate_transcription_text(question)
            if not valid:
                logger.error(f"Question inválida: {error}")
                raise ValueError(f"Pregunta inválida: {error}")
            
            # ===== RATE LIMITING =====
            if not gemini_limiter.is_allowed("chat"):
                wait_time = gemini_limiter.get_wait_time("chat")
                error_msg = f"⚠️  Límite de API excedido. Intenta en {wait_time:.1f}s"
                logger.warning(error_msg)
                raise RuntimeError(error_msg)
            
            # ===== CONSTRUCCIÓN DE PROMPT =====
            keywords_section = ""
            if keywords:
                kw_list = list(keywords.keys()) if isinstance(keywords, dict) else keywords
                if kw_list:
                    # Validar cada keyword
                    valid_kw = []
                    for kw in kw_list:
                        valid, _ = validator.validate_keyword(kw)
                        if valid:
                            valid_kw.append(kw)
                    if valid_kw:
                        keywords_section = f"\n\n📌 KEYWORDS:\n{', '.join(valid_kw)}\nUsa estas keywords en tu respuesta si es relevante."
            
            prompt = f"""Eres un asistente que responde basado en el contexto:

{context}{keywords_section}

Si no lo sabes, responde 'No lo sé'. Sé preciso y conciso.

Pregunta: {question}"""
            
            logger.info(f"Generando respuesta para: {question[:50]}...")
            response = self.model.generate_content(prompt)
            return response.text
        
        except RuntimeError as e:
            # Rate limit exceed
            logger.error(f"call_model: {str(e)}")
            raise
        
        except ValueError as e:
            # Validación fallida
            logger.error(f"call_model: Validación - {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"call_model: {type(e).__name__} - {str(e)}")
            raise
