"""
Funciones centralizadas para mostrar notificaciones
"""
import streamlit as st


# Configuración de estilos por tipo de notificación
NOTIFICATION_STYLES = {
    "success": {"icon": "✓", "class": "notification-icon-success"},
    "error": {"icon": "✕", "class": "notification-icon-error"},
    "warning": {"icon": "⚠", "class": "notification-icon-warning"},
    "info": {"icon": "ℹ", "class": "notification-icon-info"},
}

NOTIFICATION_EXPANDED_STYLES = {
    "success": "notification-expanded-success",
    "error": "notification-expanded-error",
    "info": "notification-expanded-info",
}


def _show_notification(message: str, notification_type: str) -> None:
    """
    Función interna para mostrar notificaciones compactas con tooltip.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'warning', 'info')
    """
    style = NOTIFICATION_STYLES.get(notification_type)
    if not style:
        return
    
    st.markdown(f"""
    <div class="notification-icon {style['class']}">
        {style['icon']}
        <span class="notification-tooltip">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def _show_notification_expanded(message: str, notification_type: str) -> None:
    """
    Función interna para mostrar notificaciones expandidas como toasts.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'info', 'warning')
    """
    icon = NOTIFICATION_STYLES.get(notification_type, {}).get("icon", "•")
    st.toast(f"{icon} {message}", icon=None)


# API pública - Notificaciones compactas
def show_success(message: str) -> None:
    """Muestra un icono de éxito con tooltip con el mensaje"""
    _show_notification(message, "success")


def show_error(message: str) -> None:
    """Muestra un icono de error con tooltip con el mensaje"""
    _show_notification(message, "error")


def show_warning(message: str) -> None:
    """Muestra un icono de advertencia con tooltip con el mensaje"""
    _show_notification(message, "warning")


def show_info(message: str) -> None:
    """Muestra un icono de información con tooltip con el mensaje"""
    _show_notification(message, "info")


# API pública - Notificaciones expandidas (para debug)
def show_success_expanded(message: str) -> None:
    """Muestra un mensaje de éxito visible completo (para debug)"""
    _show_notification_expanded(message, "success")


def show_error_expanded(message: str) -> None:
    """Muestra un mensaje de error visible completo (para debug)"""
    _show_notification_expanded(message, "error")


def show_info_expanded(message: str) -> None:
    """Muestra un mensaje de información visible completo (para debug)"""
    _show_notification_expanded(message, "info")


def show_warning_expanded(message: str) -> None:
    """Muestra un mensaje de advertencia en toast arriba a la derecha"""
    _show_notification_expanded(message, "warning")
