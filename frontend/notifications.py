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


def show_delete_confirmation_modal(item_name: str, item_type: str = "elemento") -> tuple[bool, bool]:
    """
    Mostrar un modal bonito de confirmación para eliminar.
    
    Args:
        item_name: Nombre del elemento a eliminar
        item_type: Tipo de elemento (audio, ticket, palabra clave, etc.)
    
    Returns:
        Tupla (confirmed: bool, cancelled: bool)
    """
    
    # Crear modal con CSS personalizado
    modal_html = f"""
    <style>
        .delete-modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.2s ease-in-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .delete-modal-content {{
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 32px;
            max-width: 420px;
            width: 90%;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8), inset 1px 1px 0 rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            animation: slideUp 0.3s ease-out;
            text-align: center;
        }}
        
        .delete-modal-icon {{
            font-size: 48px;
            margin-bottom: 16px;
            display: inline-block;
        }}
        
        .delete-modal-title {{
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
        }}
        
        .delete-modal-message {{
            font-size: 14px;
            color: #9ca3af;
            margin-bottom: 24px;
            line-height: 1.6;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
        }}
        
        .delete-modal-item {{
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 24px;
            font-weight: 600;
            color: #fca5a5;
            word-break: break-word;
            font-family: monospace;
            font-size: 13px;
        }}
        
        .delete-modal-buttons {{
            display: flex;
            gap: 12px;
            justify-content: center;
        }}
    </style>
    
    <div class="delete-modal-overlay">
        <div class="delete-modal-content">
            <div class="delete-modal-icon">⚠️</div>
            <div class="delete-modal-title">¿Eliminar {item_type}?</div>
            <div class="delete-modal-message">Esta acción no se puede deshacer. Se eliminará permanentemente:</div>
            <div class="delete-modal-item">{item_name}</div>
        </div>
    </div>
    """
    
    st.markdown(modal_html, unsafe_allow_html=True)
    
    # Retornar False, False para que se maneje con st.columns y botones
    # El modal se muestra en el HTML pero necesitamos componentes Streamlit para la interacción
    return False, False


def show_delete_confirmation_buttons(item_name: str, item_type: str = "elemento", key_prefix: str = "") -> tuple[bool, bool]:
    """
    Mostrar modal de confirmación bonito con botones DENTRO del modal.
    
    Args:
        item_name: Nombre del elemento a eliminar
        item_type: Tipo de elemento
        key_prefix: Prefijo para las keys de los botones
    
    Returns:
        Tupla (confirmed: bool, cancelled: bool)
    """
    # CSS del modal con espacio para botones
    st.markdown(f"""
    <style>
        .delete-modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9998;
            animation: fadeIn 0.25s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(40px) scale(0.95);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        
        .delete-modal-content {{
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            padding-bottom: 120px;
            max-width: 450px;
            width: 92%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 
                        inset 1px 1px 0 rgba(255, 255, 255, 0.05),
                        0 0 40px rgba(239, 68, 68, 0.1);
            backdrop-filter: blur(10px);
            animation: slideUp 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
            position: relative;
        }}
        
        .delete-modal-icon {{
            font-size: 56px;
            margin-bottom: 20px;
            display: inline-block;
            animation: bounce 0.6s ease-out;
        }}
        
        @keyframes bounce {{
            0% {{ transform: scale(0); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        
        .delete-modal-title {{
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }}
        
        .delete-modal-message {{
            font-size: 14px;
            color: #d1d5db;
            margin-bottom: 28px;
            line-height: 1.7;
        }}
        
        .delete-modal-item {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
            border: 1.5px solid rgba(239, 68, 68, 0.4);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 28px;
            font-weight: 600;
            color: #fca5a5;
            word-break: break-word;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        
        .delete-modal-warning {{
            font-size: 12px;
            color: #9ca3af;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 32px;
        }}
        
        .delete-modal-buttons {{
            display: flex;
            gap: 12px;
            margin-bottom: 0;
        }}
        
        .delete-modal-buttons button {{
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s ease;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
        }}
        
        .delete-modal-buttons .btn-confirm {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }}
        
        .delete-modal-buttons .btn-confirm:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
        }}
        
        .delete-modal-buttons .btn-cancel {{
            background: rgba(255, 255, 255, 0.1);
            color: #d1d5db;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .delete-modal-buttons .btn-cancel:hover {{
            background: rgba(255, 255, 255, 0.15);
        }}
    </style>
    
    <div class="delete-modal-overlay">
        <div class="delete-modal-content">
            <div class="delete-modal-icon">⚠️</div>
            <div class="delete-modal-title">¿Eliminar {item_type}?</div>
            <div class="delete-modal-message">Esta acción no se puede deshacer</div>
            <div class="delete-modal-item">{item_name}</div>
            <div class="delete-modal-warning">
                <span>⚡ Eliminación permanente</span>
            </div>
            
            <div class="delete-modal-buttons">
                <button type="button" class="btn-confirm" id="delete-confirm-{key_prefix}">🗑️ Eliminar</button>
                <button type="button" class="btn-cancel" id="delete-cancel-{key_prefix}">✕ Cancelar</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Manejadores JavaScript para disparar botones Streamlit
    st.markdown(f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const confirmBtn = document.getElementById('delete-confirm-{key_prefix}');
        const cancelBtn = document.getElementById('delete-cancel-{key_prefix}');
        
        if (confirmBtn) {{
            confirmBtn.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                document.getElementById('streamlit-confirm-{key_prefix}').click();
            }});
        }}
        
        if (cancelBtn) {{
            cancelBtn.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                document.getElementById('streamlit-cancel-{key_prefix}').click();
            }});
        }}
    }});
    </script>
    """, unsafe_allow_html=True)
    
    # Botones Streamlit invisibles
    col1, col2 = st.columns(2, gap="small")
    confirmed = False
    cancelled = False
    
    with col1:
        # Botón invisible para confirmar
        st.markdown(f'<button id="streamlit-confirm-{key_prefix}" style="display:none;"></button>', unsafe_allow_html=True)
        if st.button("", key=f"confirm_{key_prefix}", help="", use_container_width=True):
            confirmed = True
    
    with col2:
        # Botón invisible para cancelar
        st.markdown(f'<button id="streamlit-cancel-{key_prefix}" style="display:none;"></button>', unsafe_allow_html=True)
        if st.button("", key=f"cancel_{key_prefix}", help="", use_container_width=True):
            cancelled = True
    
    return confirmed, cancelled

