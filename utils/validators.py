"""
Módulo de validación de archivos
Valida tipo, tamaño y contenido de archivos
"""

import os
import mimetypes
from pathlib import Path

class FileValidator:
    """Validador de archivos de audio"""
    
    # Tipos MIME permitidos
    ALLOWED_MIME_TYPES = {
        'audio/mpeg': ['.mp3'],
        'audio/wav': ['.wav', '.wave'],
        'audio/mp4': ['.m4a'],
        'audio/flac': ['.flac'],
        'audio/webm': ['.webm'],
        'audio/ogg': ['.ogg', '.oga'],
        'audio/x-m4a': ['.m4a'],
    }
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {
        ext for exts in ALLOWED_MIME_TYPES.values() for ext in exts
    }
    
    def __init__(self, max_size_mb=100):
        self.max_size = max_size_mb * 1024 * 1024
    
    def validate(self, filename, file_data):
        """
        Valida un archivo antes de guardarlo
        
        Args:
            filename: Nombre del archivo
            file_data: Datos binarios del archivo
        
        Returns:
            bool: True si es válido
        
        Raises:
            ValueError: Si hay problemas de validación
        """
        
        # 1. Validar que no esté vacío
        if not file_data or len(file_data) == 0:
            raise ValueError("❌ El archivo está vacío")
        
        # 2. Validar extensión
        ext = Path(filename).suffix.lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            allowed = ", ".join(sorted(self.ALLOWED_EXTENSIONS))
            raise ValueError(
                f"❌ Extensión '{ext}' no permitida. Permitidas: {allowed}"
            )
        
        # 3. Validar tamaño
        file_size_mb = len(file_data) / (1024 * 1024)
        if len(file_data) > self.max_size:
            raise ValueError(
                f"❌ Archivo muy grande: {file_size_mb:.1f}MB (máx: {self.max_size/1024/1024:.0f}MB)"
            )
        
        # 4. Validar MIME type (detectado)
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type and mime_type not in self.ALLOWED_MIME_TYPES:
            raise ValueError(f"❌ Tipo de archivo no permitido: {mime_type}")
        
        # 5. Validar primeros bytes (magic numbers) para audio
        self._validate_magic_bytes(filename, file_data)
        
        return True
    
    def _validate_magic_bytes(self, filename, data):
        """Valida los primeros bytes del archivo para asegurar que es audio"""
        
        ext = Path(filename).suffix.lower()
        
        # Verificar magic bytes comunes de audio
        magic_numbers = {
            '.mp3': [b'ID3', b'\xff\xfb', b'\xff\xfa'],  # ID3, MPEG
            '.wav': [b'RIFF'],  # WAVE
            '.m4a': [b'\x00\x00\x00\x20\x66\x74\x79\x70'],  # ftyp
            '.flac': [b'fLaC'],  # FLAC
            '.webm': [b'\x1a\x45\xdf\xa3'],  # EBML
            '.ogg': [b'OggS'],  # OGG
        }
        
        if ext in magic_numbers:
            valid = False
            for magic in magic_numbers[ext]:
                if data.startswith(magic):
                    valid = True
                    break
            
            if not valid:
                raise ValueError(
                    f"❌ Archivo '{ext}' corrupto o no es un archivo de audio válido"
                )


def validate_upload(filename, file_data, max_size_mb=100):
    """
    Función de conveniencia para validar un archivo subido
    
    Args:
        filename: Nombre del archivo
        file_data: Datos binarios
        max_size_mb: Tamaño máximo en MB
    
    Returns:
        bool: True si es válido
    """
    validator = FileValidator(max_size_mb)
    return validator.validate(filename, file_data)
