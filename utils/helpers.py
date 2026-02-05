"""
Módulo de utilidades de seguridad
Funciones auxiliares para operaciones seguras
"""

import hashlib
import hmac
import secrets
from pathlib import Path

def generate_secure_filename(original_filename):
    """
    Genera un nombre de archivo seguro
    Previene ataques de path traversal
    
    Args:
        original_filename: Nombre original del archivo
    
    Returns:
        str: Nombre seguro para el archivo
    """
    # Obtener solo el nombre base sin ruta
    safe_name = Path(original_filename).name
    
    # Remover caracteres peligrosos
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in ".-_")
    
    # Limitar longitud
    name, ext = Path(safe_name).stem, Path(safe_name).suffix
    name = name[:50]  # Máx 50 caracteres
    
    return f"{name}{ext}"


def hash_file_content(file_data):
    """
    Calcula hash SHA-256 del contenido del archivo
    Útil para detectar duplicados y verificar integridad
    
    Args:
        file_data: Datos binarios del archivo
    
    Returns:
        str: Hash SHA-256 en hexadecimal
    """
    return hashlib.sha256(file_data).hexdigest()


def verify_file_integrity(file_data, expected_hash):
    """
    Verifica que un archivo no haya sido modificado
    
    Args:
        file_data: Datos binarios del archivo
        expected_hash: Hash esperado
    
    Returns:
        bool: True si el archivo es íntegro
    """
    actual_hash = hash_file_content(file_data)
    return hmac.compare_digest(actual_hash, expected_hash)


def generate_secure_token(length=32):
    """
    Genera un token criptográficamente seguro
    
    Args:
        length: Longitud del token en bytes
    
    Returns:
        str: Token hexadecimal
    """
    return secrets.token_hex(length)


def sanitize_sql(input_string):
    """
    Sanitiza una string para prevenir SQL injection
    NOTA: Usar prepared statements en su lugar siempre que sea posible
    
    Args:
        input_string: String a sanitizar
    
    Returns:
        str: String sanitizada
    """
    # Caracteres peligrosos a escapar
    dangerous_chars = {
        "'": "''",
        '"': '""',
        '\\': '\\\\',
        ';': '',
        '--': '',
    }
    
    result = input_string
    for char, replacement in dangerous_chars.items():
        result = result.replace(char, replacement)
    
    return result


def is_safe_path(base_path, user_path):
    """
    Verifica que un path está dentro del base_path
    Previene path traversal attacks
    
    Args:
        base_path: Path base permitida
        user_path: Path proporcionada por usuario
    
    Returns:
        bool: True si es segura
    """
    base = Path(base_path).resolve()
    user = Path(user_path).resolve()
    
    try:
        user.relative_to(base)
        return True
    except ValueError:
        return False


def mask_api_key(api_key, show_chars=4):
    """
    Enmascara una API key para logging seguro
    Ej: "AIzaSyD6tyS3cxYnGm..." -> "AIza...****"
    
    Args:
        api_key: API key a enmascarar
        show_chars: Caracteres a mostrar al inicio
    
    Returns:
        str: API key enmascarada
    """
    if len(api_key) <= show_chars:
        return "****"
    return api_key[:show_chars] + "..." + "*" * (len(api_key) - show_chars)
