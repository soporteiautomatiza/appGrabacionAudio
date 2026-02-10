"""
Funciones centralizadas para mostrar notificaciones con toasts
"""
import streamlit as st


# Configuración de colores por tipo
TOAST_COLORS = {
    "success": {"bg": "#10b981", "text": "white", "icon": "✓"},
    "error": {"bg": "#ef4444", "text": "white", "icon": "✕"},
    "warning": {"bg": "#f59e0b", "text": "white", "icon": "⚠"},
    "info": {"bg": "#3b82f6", "text": "white", "icon": "ℹ"},
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
    bg = config["bg"]
    text = config["text"]
    
    # CSS + HTML puro para toast
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
            from {{ opacity: 1; }}
            to {{ opacity: 0; }}
        }}
        
        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: {bg};
            color: {text};
            padding: 16px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            z-index: 99999;
            max-width: 300px;
            word-wrap: break-word;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
            animation: slideInRight 0.3s ease-out;
        }}
    </style>
    
    <div class="toast">
        <span>{icon}</span> {message}
    </div>
    """, unsafe_allow_html=True)


# API legacy (compatibilidad)
show_success_expanded = show_success
show_error_expanded = show_error
show_warning_expanded = show_warning
show_info_expanded = show_info

show_success_debug = show_success
show_error_debug = show_error
show_info_debug = show_info

