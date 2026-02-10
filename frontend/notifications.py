"""
Funciones centralizadas para mostrar notificaciones con toasts.
Sistema de notificaciones minimalista usando HTML + CSS puro.
"""
import streamlit as st


# Configuración de colores por tipo
TOAST_COLORS = {
    "success": {"border": "#10b981", "icon": "✓"},
    "error": {"border": "#ef4444", "icon": "✕"},
    "warning": {"border": "#f59e0b", "icon": "⚠"},
    "info": {"border": "#2563eb", "icon": "ℹ"},
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
    accent = config["border"]
    
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
        
        .toast {
            position: fixed;
            top: 32px;
            right: 32px;
            background: var(--surface, #ffffff);
            color: var(--text-primary, #0f172a);
            padding: 14px 18px;
            border-radius: 16px;
            border: 1px solid var(--border, #e4e7f4);
            border-left: 4px solid {accent};
            font-weight: 600;
            font-size: 13px;
            box-shadow: 0 25px 60px rgba(15, 23, 42, 0.15);
            z-index: 99999;
            max-width: 360px;
            word-wrap: break-word;
            font-family: 'Manrope', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
            display: flex;
            align-items: center;
            gap: 12px;
            animation: toastAnimation 4s ease-in-out forwards;
        }

        .toast span {
            font-size: 16px;
            flex-shrink: 0;
        }
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
    accent = config["border"]
    
    # Mostrar en línea sin animación de desvanecimiento
    st.markdown(f"""
    <div style="
        background: var(--surface, #ffffff);
        color: var(--text-primary, #0f172a);
        padding: 12px 16px;
        border-radius: 14px;
        border-left: 4px solid {accent};
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        max-width: 100%;
        word-wrap: break-word;
        font-family: 'Manrope', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
        border: 1px solid var(--border, #e4e7f4);
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    ">
        <span style="font-size: 16px; flex-shrink: 0;">{icon}</span> 
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)

