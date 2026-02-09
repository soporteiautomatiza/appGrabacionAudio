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
    Función interna para mostrar notificaciones expandidas con colores personalizados.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'info', 'warning')
    """
    icon = NOTIFICATION_STYLES.get(notification_type, {}).get("icon", "•")
    
    # Colores personalizados para cada tipo
    colors = {
        "success": {"bg": "#10b981", "text": "white"},  # Verde
        "error": {"bg": "#ef4444", "text": "white"},    # Rojo
        "warning": {"bg": "#f59e0b", "text": "white"},  # Amarillo
        "info": {"bg": "#3b82f6", "text": "white"}      # Azul
    }
    
    color_style = colors.get(notification_type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background-color: {color_style['bg']};
        color: {color_style['text']};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideInRight 0.3s ease-out;
        display: inline-block;
    ">
        {icon} {message}
    </div>
    <style>
        @keyframes slideInRight {{
            from {{
                opacity: 0;
                transform: translateX(20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


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


# Funciones de DEBUG - Para cuadros expandidos abajo
def show_success_debug(message: str) -> None:
    """Muestra un mensaje de éxito en cuadro expandido (para debug)"""
    icon = NOTIFICATION_STYLES.get("success", {}).get("icon", "•")
    st.markdown(f"""
    <div class="notification-expanded notification-expanded-success">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)


def show_error_debug(message: str) -> None:
    """Muestra un mensaje de error en cuadro expandido (para debug)"""
    icon = NOTIFICATION_STYLES.get("error", {}).get("icon", "•")
    st.markdown(f"""
    <div class="notification-expanded notification-expanded-error">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)


def show_info_debug(message: str) -> None:
    """Muestra un mensaje de información en cuadro expandido (para debug)"""
    icon = NOTIFICATION_STYLES.get("info", {}).get("icon", "•")
    st.markdown(f"""
    <div class="notification-expanded notification-expanded-info">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)
