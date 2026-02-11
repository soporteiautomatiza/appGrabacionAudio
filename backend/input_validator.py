"""input_validator.py - Validación robusta de entrada de datos"""
import re
from typing import Tuple, Optional, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

class InputValidator:
    """Validador centralizado de inputs"""
    
    # Patrones permitidos
    SAFE_FILENAME_PATTERN = re.compile(r'^[\w\-. ]+$')
    SAFE_KEYWORD_PATTERN = re.compile(r'^[\w\s\-áéíóúñ]{1,100}$', re.IGNORECASE)
    SAFE_TEXT_PATTERN = re.compile(r'^[\w\s\-.,!?áéíóúñ]{1,5000}$', re.IGNORECASE)
    
    # Longitudes máximas
    MAX_FILENAME_LENGTH = 255
    MAX_KEYWORD_LENGTH = 100
    MAX_SEARCH_LENGTH = 200
    MAX_TEXT_LENGTH = 5000
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "flac", "webm"}
    
    # Caracteres/strings prohibidos
    FORBIDDEN_STRINGS = [
        "../", "..\\", "etc/passwd", "system32",
        "script>", "<iframe", "javascript:", "onclick", "onerror"
    ]
    
    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, Optional[str]]:
        """Valida nombre de archivo de audio
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Tupla (válido: bool, mensaje_error: Optional[str])
        """
        if not filename or not isinstance(filename, str):
            return False, "Nombre de archivo inválido"
        
        filename = filename.strip()
        
        if len(filename) > InputValidator.MAX_FILENAME_LENGTH:
            return False, f"Nombre muy largo (máx {InputValidator.MAX_FILENAME_LENGTH} caracteres)"
        
        if len(filename) == 0:
            return False, "Nombre de archivo vacío"
        
        # Verificar extensión
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if ext not in InputValidator.ALLOWED_EXTENSIONS:
            return False, f"Extensión no permitida. Usa: {', '.join(InputValidator.ALLOWED_EXTENSIONS)}"
        
        # Verificar caracteres peligrosos
        if not InputValidator.SAFE_FILENAME_PATTERN.match(filename):
            return False, "Nombre contiene caracteres no permitidos"
        
        # Verificar strings prohibidos
        if any(forbidden in filename.lower() for forbidden in InputValidator.FORBIDDEN_STRINGS):
            return False, "Nombre contiene caracteres/patrones sospechosos"
        
        logger.debug(f"✓ Filename validado: {filename}")
        return True, None
    
    @staticmethod
    def validate_keyword(keyword: str) -> Tuple[bool, Optional[str]]:
        """Valida palabra clave para búsqueda
        
        Args:
            keyword: Palabra clave a validar
            
        Returns:
            Tupla (válido: bool, mensaje_error: Optional[str])
        """
        if not keyword or not isinstance(keyword, str):
            return False, "Palabra clave inválida"
        
        keyword = keyword.strip()
        
        if len(keyword) == 0:
            return False, "Palabra clave vacía"
        
        if len(keyword) > InputValidator.MAX_KEYWORD_LENGTH:
            return False, f"Palabra clave muy larga (máx {InputValidator.MAX_KEYWORD_LENGTH} caracteres)"
        
        if not InputValidator.SAFE_KEYWORD_PATTERN.match(keyword):
            return False, "Palabra clave contiene caracteres no permitidos"
        
        logger.debug(f"✓ Keyword validado: {keyword}")
        return True, None
    
    @staticmethod
    def validate_search_query(query: str) -> Tuple[bool, Optional[str]]:
        """Valida búsqueda/query
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Tupla (válido: bool, mensaje_error: Optional[str])
        """
        if not isinstance(query, str):
            return False, "Búsqueda inválida"
        
        query = query.strip()
        
        if len(query) == 0:
            return True, None  # Búsqueda vacía es válida (sin filtro)
        
        if len(query) > InputValidator.MAX_SEARCH_LENGTH:
            return False, f"Búsqueda muy larga (máx {InputValidator.MAX_SEARCH_LENGTH} caracteres)"
        
        # Escapar caracteres especiales regex
        escaped = re.escape(query)
        
        logger.debug(f"✓ Search query validado: {query}")
        return True, None
    
    @staticmethod
    def validate_transcription_text(text: str) -> Tuple[bool, Optional[str]]:
        """Valida texto de transcripción
        
        Args:
            text: Texto de transcripción
            
        Returns:
            Tupla (válido: bool, mensaje_error: Optional[str])
        """
        if not text or not isinstance(text, str):
            return False, "Texto inválido"
        
        text = text.strip()
        
        if len(text) == 0:
            return False, "Transcripción vacía"
        
        logger.debug(f"✓ Transcription validado: {len(text)} caracteres")
        return True, None
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 500) -> str:
        """Limpia y sanitiza un string arbitrario
        
        Args:
            text: Texto a limpiar
            max_length: Longitud máxima permitida
            
        Returns:
            String limpio
        """
        if not isinstance(text, str):
            return ""
        
        # Remover caracteres de control
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        # Limitar longitud
        text = text[:max_length]
        
        return text.strip()
    
    @staticmethod
    def validate_audio_size(size_bytes: int, max_mb: int = 100) -> Tuple[bool, Optional[str]]:
        """Valida tamaño de archivo de audio
        
        Args:
            size_bytes: Tamaño en bytes
            max_mb: Tamaño máximo permitido en MB
            
        Returns:
            Tupla (válido: bool, mensaje_error: Optional[str])
        """
        if not isinstance(size_bytes, int) or size_bytes < 0:
            return False, "Tamaño de archivo inválido"
        
        if size_bytes == 0:
            return False, "Archivo vacío"
        
        size_mb = size_bytes / (1024 * 1024)
        if size_mb > max_mb:
            return False, f"Archivo demasiado grande ({size_mb:.1f}MB > {max_mb}MB)"
        
        logger.debug(f"✓ Audio size validado: {size_mb:.2f}MB")
        return True, None

# Instancia global
validator = InputValidator()
