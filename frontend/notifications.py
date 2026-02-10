"""
Funciones centralizadas para mostrar notificaciones con toasts.
Sistema de notificaciones minimalista usando HTML + CSS puro.
"""
import streamlit as st


# Configuración de colores por tipo
TOAST_COLORS = {
    "success": {"bg": "#1f2937", "text": "#10b981", "icon": "✓"},    # Fondo gris oscuro, texto verde
    "error": {"bg": "#1f2937", "text": "#ef4444", "icon": "✕"},       # Fondo gris oscuro, texto rojo
    "warning": {"bg": "#1f2937", "text": "#f59e0b", "icon": "⚠"},     # Fondo gris oscuro, texto amarillo
    "info": {"bg": "#1f2937", "text": "#3b82f6", "icon": "ℹ"},        # Fondo gris oscuro, texto azul
}


def show_success(message: str, duration: int = 3) -> None:
    """Mostrar notificación de éxito en esquina superior derecha"""
    _show_toast(message, "success", duration)


def show_error(message: str, duration: int = 3) -> None:
    """Mostrar notificación de error en esquina superior derecha"""
    _show_toast(message, "error", duration)


def show_warning(message: str, duration: int = 3) -> None:
    """Mostrar notificación de advertencia en esquina superior derecha"""
    _show_toast(message, "warning", duration)


def show_info(message: str, duration: int = 3) -> None:
    """Mostrar notificación de información en esquina superior derecha"""
    _show_toast(message, "info", duration)


def _show_toast(message: str, notification_type: str, duration: int = 3) -> None:
    """
    Mostrar notificación como toast en esquina superior derecha.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo ('success', 'error', 'warning', 'info')
        duration: Segundos hasta desvanecerse
    """
    config = TOAST_COLORS.get(notification_type, TOAST_COLORS["info"])
    icon = config["icon"]
    text = config["text"]
    
    # Generar ID único para el toast
    import uuid
    toast_id = str(uuid.uuid4())
    
    # CSS + HTML + JavaScript para toast interactivo
    st.markdown(f"""
    <style>
        @keyframes slideInRight {{
            from {{
                opacity: 0;
                transform: translateX(400px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        @keyframes fadeOut {{
            from {{ 
                opacity: 1;
                transform: translateX(0);
            }}
            to {{ 
                opacity: 0;
                transform: translateX(400px);
            }}
        }}
        
        .toast {{
            position: fixed;
            top: 100px;
            right: 20px;
            background: rgba(31, 41, 55, 0.95);
            color: {text};
            padding: 12px 16px;
            border-radius: 10px;
            border-left: 3px solid {text};
            font-weight: 600;
            font-size: 13px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 1px 1px 0 rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            z-index: 99999;
            max-width: 280px;
            word-wrap: break-word;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
            animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }}
        
        .toast-content {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
        }}
        
        .toast-close {{
            background: none;
            border: none;
            color: {text};
            cursor: pointer;
            font-size: 18px;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            opacity: 0.7;
            transition: opacity 0.2s;
        }}
        
        .toast-close:hover {{
            opacity: 1;
        }}
        
        .toast.fade-out {{
            animation: fadeOut 0.3s ease-out forwards;
        }}
    </style>
    
    <div class="toast" id="toast-{toast_id}">
        <div class="toast-content">
            <span>{icon}</span> {message}
        </div>
        <button class="toast-close" onclick="document.getElementById('toast-{toast_id}').classList.add('fade-out'); setTimeout(() => document.getElementById('toast-{toast_id}').remove(), 300);">✕</button>
    </div>
    
    <script>
        setTimeout(() => {{
            const toast = document.getElementById('toast-{toast_id}');
            if (toast && !toast.classList.contains('fade-out')) {{
                toast.classList.add('fade-out');
                setTimeout(() => toast.remove(), 300);
            }}
        }}, 2000);
    </script>
    """, unsafe_allow_html=True)


# API legacy (compatibilidad)
show_success_expanded = show_success
show_error_expanded = show_error
show_warning_expanded = show_warning
show_info_expanded = show_info

show_success_debug = show_success
show_error_debug = show_error
show_info_debug = show_info

