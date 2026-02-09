"""
Funciones centralizadas para mostrar notificaciones
Sistema de cola con apilamiento vertical, auto-desaparición y botón X
"""
import streamlit as st
from datetime import datetime, timedelta
import uuid


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


# Inicializar notificaciones en session_state si no existen
if "notifications_queue" not in st.session_state:
    st.session_state.notifications_queue = []


def _add_notification_to_queue(message: str, notification_type: str, duration: int = 4) -> None:
    """
    Añade una notificación a la cola.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'info', 'warning')
        duration: Segundos que permanece visible (default: 4)
    """
    notification_id = str(uuid.uuid4())
    notification = {
        "id": notification_id,
        "message": message,
        "type": notification_type,
        "created_at": datetime.now(),
        "duration": duration
    }
    st.session_state.notifications_queue.append(notification)


def _display_notifications() -> None:
    """
    Muestra todas las notificaciones activas en la cola.
    Elimina las expiradas y renderiza las activas apiladas verticalmente.
    """
    # Limpiar notificaciones expiradas
    now = datetime.now()
    st.session_state.notifications_queue = [
        n for n in st.session_state.notifications_queue
        if now - n["created_at"] < timedelta(seconds=n["duration"])
    ]
    
    if not st.session_state.notifications_queue:
        return
    
    # Colores personalizados para cada tipo
    colors = {
        "success": {"bg": "#10b981", "text": "white"},
        "error": {"bg": "#ef4444", "text": "white"},
        "warning": {"bg": "#f59e0b", "text": "white"},
        "info": {"bg": "#3b82f6", "text": "white"}
    }
    
    # Mostrar todas las notificaciones apiladas
    notification_html = ""
    for idx, notification in enumerate(st.session_state.notifications_queue):
        color_style = colors.get(notification["type"], colors["info"])
        icon = NOTIFICATION_STYLES.get(notification["type"], {}).get("icon", "•")
        top_position = 80 + (idx * 70)  # Espaciar verticalmente 70px cada una
        
        notification_html += f"""
        <div id="notif_{notification['id']}" style="
            position: fixed;
            top: {top_position}px;
            right: 20px;
            background-color: {color_style['bg']};
            color: {color_style['text']};
            padding: 14px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            z-index: {9999 - idx};
            max-width: 350px;
            animation: slideInRight 0.4s ease-out;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        ">
            <span>{icon} {notification['message']}</span>
            <button onclick="document.getElementById('notif_{notification['id']}').style.display='none';" 
                    style="
                    background: none;
                    border: none;
                    color: {color_style['text']};
                    font-size: 18px;
                    cursor: pointer;
                    padding: 0;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0.8;
                    transition: opacity 0.2s;
                    " 
                    onmouseover="this.style.opacity='1'"
                    onmouseout="this.style.opacity='0.8'"
            >✕</button>
        </div>
        """
    
    st.markdown(f"""
    {notification_html}
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
    </style>
    """, unsafe_allow_html=True)




# API pública - Notificaciones en cola (arriba a la derecha)
def show_success(message: str) -> None:
    """Añade un mensaje de éxito a la cola"""
    _add_notification_to_queue(message, "success")


def show_error(message: str) -> None:
    """Añade un mensaje de error a la cola"""
    _add_notification_to_queue(message, "error")


def show_warning(message: str) -> None:
    """Añade un mensaje de advertencia a la cola"""
    _add_notification_to_queue(message, "warning")


def show_info(message: str) -> None:
    """Añade un mensaje de información a la cola"""
    _add_notification_to_queue(message, "info")


# Alias para compatibilidad con código existente
def show_success_expanded(message: str) -> None:
    """Alias de show_success para compatibilidad"""
    show_success(message)


def show_error_expanded(message: str) -> None:
    """Alias de show_error para compatibilidad"""
    show_error(message)


def show_warning_expanded(message: str) -> None:
    """Alias de show_warning para compatibilidad"""
    show_warning(message)


def show_info_expanded(message: str) -> None:
    """Alias de show_info para compatibilidad"""
    show_info(message)


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


# Función para renderizar todas las notificaciones (llamar al inicio de index.py)
def render_notifications() -> None:
    """Renderiza todas las notificaciones activas en la cola"""
    _display_notifications()
