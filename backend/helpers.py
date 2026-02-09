"""helpers.py - Funciones auxiliares comunes (refactorizado a 150 líneas)"""
import streamlit as st
from functools import wraps
from pathlib import Path
from typing import Callable, Optional, Any, Dict, List, Tuple
from datetime import datetime
import json
from logger import get_logger

logger = get_logger(__name__)

# ============ DECORADORES ============

def db_operation(func: Callable) -> Callable:
    """Decorador para operaciones BD: maneja conexión, excepciones y logging"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            from database import init_supabase
            db = init_supabase()
            if not db: 
                logger.warning(f"{func.__name__}: BD no disponible")
                return None if 'get' in func.__name__ else False
            return func(db, *args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}: {type(e).__name__} - {str(e)}")
            return None if 'get' in func.__name__ else False
    return wrapper

def safe_call(default_value=None):
    """Decorador para capturar excepciones sin romper la app"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{func.__name__}: {type(e).__name__} - {str(e)}")
                return default_value
        return wrapper
    return decorator

# ============ VALIDACIONES ============

def validate_file(filepath: str, expected_ext: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Valida que un archivo existe y tiene tamaño > 0"""
    p = Path(filepath)
    if not p.exists(): 
        return False, f"Archivo no encontrado: {filepath}"
    if not p.is_file(): 
        return False, f"No es un archivo: {filepath}"
    if p.stat().st_size == 0: 
        return False, f"Archivo vacío: {filepath}"
    if expected_ext and not str(filepath).lower().endswith(expected_ext):
        return False, f"Formato inválido. Esperado: {expected_ext}"
    return True, None

def validate_keywords(keywords: Dict, max_keywords: int = 50, min_length: int = 2) -> Tuple[bool, str]:
    """Valida palabras clave"""
    if not keywords:
        return False, "Ingresa al menos una palabra clave"
    if len(keywords) > max_keywords:
        return False, f"Máximo {max_keywords} palabras clave"
    for kw in keywords.keys():
        if len(kw) < min_length:
            return False, f"'{kw}' debe tener al menos {min_length} caracteres"
    return True, ""

def validate_context(context: str, min_len: int = 100) -> Tuple[bool, str]:
    """Valida contexto de transcripción"""
    if not context or len(context.strip()) < min_len:
        return False, f"Contexto muy corto (mínimo {min_len} caracteres)"
    return True, ""

# ============ FORMATEO ============

def clean_filename(filename: str) -> str:
    """Limpia nombre de archivo eliminando extensiones"""
    extensions = [".wav", ".mp3", ".m4a", ".webm", ".ogg", ".flac"]
    result = filename
    for ext in extensions:
        result = result.replace(ext, "").replace("_", " ")
    return result

def format_enum(enum_dict: Dict[str, str], current_value: str) -> Tuple[List[str], int]:
    """Retorna (display_names, current_index) para selectboxes"""
    display_names = list(enum_dict.keys())
    current_label = [k for k, v in enum_dict.items() if v == current_value]
    current_index = display_names.index(current_label[0]) if current_label else 0
    return display_names, current_index

# ============ SESSION STATE ============

def init_session_defaults(defaults: Dict[str, Any]) -> None:
    """Inicializa múltiples valores de session_state de una vez"""
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_session(key: str, default: Any = None) -> Any:
    """Obtiene valor de session_state con default"""
    return st.session_state.get(key, default)

def set_session(key: str, value: Any) -> None:
    """Establece valor de session_state"""
    st.session_state[key] = value

# ============ DATABASE HELPERS ============

def table_query(db, table: str, method: str = "select", *args, **kwargs):
    """Query simple a Supabase"""
    try:
        query = getattr(db.table(table), method)(*args, **kwargs)
        result = query.execute()
        return result.data if result and result.data else ([] if method == "select" else result.data)
    except Exception as e:
        logger.debug(f"Query {method} en {table}: {str(e)}")
        return [] if method == "select" else None

def safe_json_dump(data: Dict, filename: str, dir_path: Path) -> bool:
    """Guarda JSON de forma segura"""
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(dir_path / filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"JSON save error: {str(e)}")
        return False

def safe_json_load(filepath: Path) -> Optional[Dict]:
    """Carga JSON de forma segura"""
    if not filepath.exists():
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"JSON load error: {str(e)}")
        return None

