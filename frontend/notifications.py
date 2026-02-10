"""
Funciones centralizadas para mostrar notificaciones con toast automático
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

# Iconos para toasts
TOAST_ICONS = {
    "success": "✓",
    "error": "✕",
    "warning": "⚠",
    "info": "ℹ",
}

# Colores para toasts
TOAST_COLORS = {
    "success": {"bg": "#10b981", "text": "white"},  # Verde
    "error": {"bg": "#ef4444", "text": "white"},    # Rojo
    "warning": {"bg": "#f59e0b", "text": "white"},  # Amarillo
    "info": {"bg": "#3b82f6", "text": "white"}      # Azul
}


def _initialize_toast_state() -> None:
    """Inicializar session_state para toasts si no existe"""
    if "toasts" not in st.session_state:
        st.session_state.toasts = []


def _show_toast(message: str, notification_type: str, duration: int = 3) -> None:
    """
    Mostrar notificación como toast en esquina superior derecha con auto-desvanecimiento.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'warning', 'info')
        duration: Segundos hasta desvanecerse (default: 3)
    """
    icon = TOAST_ICONS.get(notification_type, "•")
    color = TOAST_COLORS.get(notification_type, TOAST_COLORS["info"])
    
    # Usar HTML puro con CSS para posicionar en esquina superior derecha
    # Sin JavaScript para evitar conflictos con Streamlit
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
        
        .toast-notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: {color['bg']};
            color: {color['text']};
            padding: 16px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            z-index: 99999;
            max-width: 300px;
            word-wrap: break-word;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            animation: slideInRight 0.3s ease-out, fadeOut 0.3s ease-out {duration - 0.3}s forwards;
        }}
    </style>
    
    <div class="toast-notification">
        <span>{icon}</span> {message}
    </div>
    """, unsafe_allow_html=True)


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
    color = TOAST_COLORS.get(notification_type, TOAST_COLORS["info"])
    
    st.markdown(f"""
    <div style="
        background-color: {color['bg']};
        color: {color['text']};
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


def _create_notification_function(notification_type: str, style_variant: str):
    """Factory que crea funciones de notificación dinámicamente
    
    Args:
        notification_type: 'success', 'error', 'warning', 'info'
        style_variant: 'toast', 'compact', 'expanded', 'debug'
                      'toast' = esquina superior derecha con auto-desvanecimiento
                      'compact', 'expanded', 'debug' = en línea (legacy)
    """
    def notification_func(message: str, duration: int = 3) -> None:
        if style_variant == 'toast':
            # Toast en esquina superior derecha con auto-desvanecimiento
            _show_toast(message, notification_type, duration)
        elif style_variant == 'compact':
            _show_notification(message, notification_type)
        elif style_variant == 'expanded':
            _show_notification_expanded(message, notification_type)
        elif style_variant == 'debug':
            icon = NOTIFICATION_STYLES.get(notification_type, {}).get("icon", "•")
            st.markdown(f'<div class="notification-expanded notification-expanded-{notification_type}">{icon} {message}</div>', unsafe_allow_html=True)
    
    return notification_func

# API pública - TOASTS (RECOMENDADAS - esquina superior derecha con auto-desvanecimiento)
show_success = _create_notification_function("success", "toast")
show_error = _create_notification_function("error", "toast")
show_warning = _create_notification_function("warning", "toast")
show_info = _create_notification_function("info", "toast")

# API legacy - En línea (mantener compatibilidad)
show_success_expanded = _create_notification_function("success", "expanded")
show_error_expanded = _create_notification_function("error", "expanded")
show_info_expanded = _create_notification_function("info", "expanded")
show_warning_expanded = _create_notification_function("warning", "expanded")

show_success_debug = _create_notification_function("success", "debug")
show_error_debug = _create_notification_function("error", "debug")
show_info_debug = _create_notification_function("info", "debug")

