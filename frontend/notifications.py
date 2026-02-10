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
    
    # CSS + HTML puro para toast sin JavaScript
    st.markdown(f"""
    <style>
        @keyframes toastAnimation {{
            0% {{
                opacity: 0;
                transform: translateX(400px);
            }}
            15% {{
                opacity: 1;
                transform: translateX(0);
            }}
            85% {{
                opacity: 1;
                transform: translateX(0);
            }}
            100% {{
                opacity: 0;
                transform: translateX(400px);
                visibility: hidden;
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
            border-right: 3px solid {text};
            font-weight: 600;
            font-size: 13px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 1px 1px 0 rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            z-index: 99999;
            max-width: 350px;
            word-wrap: break-word;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 10px;
            animation: toastAnimation 4s ease-in-out forwards;
        }}
        
        .toast span {{
            font-size: 16px;
            flex-shrink: 0;
        }}
    </style>
    
    <div class="toast">
        <span>{icon}</span> 
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


# API legacy (compatibilidad)
show_success_expanded = show_success
show_error_expanded = show_error
show_warning_expanded = show_warning
show_info_expanded = show_info


def show_success_debug(message: str) -> None:
    """Mostrar notificación de éxito permanente (debug)"""
    _show_debug_notification(message, "success")


def show_error_debug(message: str) -> None:
    """Mostrar notificación de error permanente (debug)"""
    _show_debug_notification(message, "error")


def show_info_debug(message: str) -> None:
    """Mostrar notificación de información permanente (debug)"""
    _show_debug_notification(message, "info")


def _show_debug_notification(message: str, notification_type: str) -> None:
    """
    Mostrar notificación permanente en línea sin desvanecimiento (debug).
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo ('success', 'error', 'info')
    """
    config = TOAST_COLORS.get(notification_type, TOAST_COLORS["info"])
    icon = config["icon"]
    text = config["text"]
    
    # Mostrar en línea sin animación de desvanecimiento
    st.markdown(f"""
    <div style="
        background: rgba(31, 41, 55, 0.95);
        color: {text};
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 3px solid {text};
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), inset 1px 1px 0 rgba(255, 255, 255, 0.1);
        max-width: 100%;
        word-wrap: break-word;
        font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    ">
        <span style="font-size: 16px; flex-shrink: 0;">{icon}</span> 
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)

