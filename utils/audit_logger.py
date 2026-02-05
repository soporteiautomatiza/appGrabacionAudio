"""
Módulo de logging de auditoría
Registra todas las operaciones de seguridad
"""

import logging
import json
from datetime import datetime
from pathlib import Path

class AuditLogger:
    """Logger de auditoría para operaciones sensibles"""
    
    def __init__(self, log_file="audit.log"):
        self.log_file = log_file
        self.logger = logging.getLogger("audit")
        
        # No agregar handlers múltiples
        if not self.logger.handlers:
            # Crear directorio si no existe
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            
            handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _format_size(self, size_bytes):
        """Convierte bytes a formato legible"""
        for unit in ['B', 'KB', 'MB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}GB"
    
    def log_upload(self, filename, size_bytes, user_ip=None):
        """Registra carga de archivo"""
        size_str = self._format_size(size_bytes)
        ip_str = f" | IP: {user_ip}" if user_ip else ""
        self.logger.info(f"UPLOAD | Archivo: {filename} | Tamaño: {size_str}{ip_str}")
    
    def log_transcription(self, filename, success=True, error=None, user_ip=None):
        """Registra transcripción"""
        status = "SUCCESS" if success else "FAILED"
        error_str = f" | Error: {error}" if error else ""
        ip_str = f" | IP: {user_ip}" if user_ip else ""
        self.logger.info(f"TRANSCRIPTION | {status} | Archivo: {filename}{error_str}{ip_str}")
    
    def log_deletion(self, filename, success=True, user_ip=None):
        """Registra eliminación"""
        status = "SUCCESS" if success else "FAILED"
        ip_str = f" | IP: {user_ip}" if user_ip else ""
        self.logger.info(f"DELETION | {status} | Archivo: {filename}{ip_str}")
    
    def log_error(self, error_type, error_msg, severity="WARNING", user_ip=None):
        """Registra errores de seguridad"""
        ip_str = f" | IP: {user_ip}" if user_ip else ""
        self.logger.warning(f"ERROR | {severity} | {error_type}: {error_msg}{ip_str}")
    
    def log_api_error(self, api_name, error_msg, user_ip=None):
        """Registra errores de API"""
        ip_str = f" | IP: {user_ip}" if user_ip else ""
        self.logger.warning(f"API_ERROR | {api_name}: {error_msg}{ip_str}")
    
    def log_validation_failed(self, filename, reason, user_ip=None):
        """Registra fallos de validación"""
        ip_str = f" | IP: {user_ip}" if user_ip else ""
        self.logger.warning(f"VALIDATION_FAILED | Archivo: {filename} | Razón: {reason}{ip_str}")
    
    def log_security_event(self, event_type, details, severity="WARNING"):
        """Registra eventos de seguridad"""
        self.logger.warning(f"SECURITY_EVENT | {severity} | {event_type}: {details}")


# Instancia global
audit_logger = AuditLogger()
