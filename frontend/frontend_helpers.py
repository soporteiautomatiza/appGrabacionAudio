"""frontend_helpers.py - Helpers específicos del frontend para reducir código repetido"""
import streamlit as st
from typing import Dict, Tuple, Optional, Any, Callable
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from backend.helpers import clean_filename, format_enum, get_session, set_session, validate_keywords

logger = get_logger(__name__)

# ============ SESSION STATE INICIALIZACIÓN ============

DEFAULT_SESSION_STATE = {
    "processed_audios": set(),
    "recordings": [],
    "selected_audio": None,
    "upload_key_counter": 0,
    "record_key_counter": 0,
    "keywords": {},
    "delete_confirmation": {},
    "transcription_cache": {},
    "chat_history": [],
    "chat_history_limit": 50,
    "opp_delete_confirmation": {},
    "chat_enabled": False,
    "loaded_audio": None,
    "contexto": "",
    "show_opportunities": False
}

def init_session():
    """Inicializa TODO el session_state de una vez"""
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            if isinstance(value, set):
                st.session_state[key] = value.copy()
            elif isinstance(value, list):
                st.session_state[key] = value.copy()
            elif isinstance(value, dict):
                st.session_state[key] = value.copy()
            else:
                st.session_state[key] = value

# ============ UI HELPERS ============

def reset_audio_input(counter_key: str) -> None:
    """Resetea un input de audio para que no se procese duplicadamente"""
    st.session_state[counter_key] += 1

def confirmation_dialog(key: str, item_name: str, on_confirm: Callable, on_cancel: Callable = None) -> None:
    """Muestra diálogo de confirmación genérico"""
    if get_session(f"{key}_confirm", False):
        st.warning(f"⚠️ ¿{item_name}?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✓ Sí", key=f"{key}_yes"):
                on_confirm()
                st.session_state[f"{key}_confirm"] = False
                st.rerun()
        with col_no:
            if st.button("✗ No", key=f"{key}_no"):
                if on_cancel:
                    on_cancel()
                st.session_state[f"{key}_confirm"] = False
                st.rerun()

def selection_box(label: str, options: list, format_func: Callable = None, key: str = None) -> Optional[Any]:
    """Selectbox con limpieza de filename automática"""
    if not format_func:
        format_func = clean_filename
    return st.selectbox(label, options, format_func=format_func, key=key)

def enum_selectbox(label: str, enum_dict: Dict[str, str], current_value: str, key: str = None) -> str:
    """Selectbox que mapea display names a valores"""
    display_names, current_idx = format_enum(enum_dict, current_value)
    selected_label = st.selectbox(label, display_names, index=current_idx, key=key, label_visibility="collapsed")
    return enum_dict[selected_label]

# ============ FILTRADO Y BÚSQUEDA ============

def filter_recordings(recordings: list, search_query: str) -> list:
    """Filtra grabaciones por búsqueda"""
    if not search_query.strip():
        return recordings
    
    import re
    search_safe = re.escape(search_query.strip().lower())
    return [r for r in recordings if search_safe in r.lower()]

def get_transcription_status(filename: str, db_utils: Any) -> str:
    """Retorna string de estado de transcripción con caché"""
    if filename in get_session("transcription_cache", {}):
        cached = get_session("transcription_cache", {})[filename]
        return " ✓ Transcrito" if cached else ""
    
    result = db_utils.get_transcription_by_filename(filename)
    st.session_state.transcription_cache[filename] = result
    return " ✓ Transcrito" if result else ""

# ============ FORMATO DE CONTEXTO ============

def highlight_keyword_in_context(context: str, keyword: str) -> str:
    """Resalta keyword en contexto con HTML"""
    return context.replace(
        keyword,
        f'<span style="color: #0052CC; font-weight: 600;">{keyword}</span>'
    )

def format_context_display(context: str) -> str:
    """Formatea contexto para mostrar en UI"""
    return f"""
    <div class="notification-container notification-info">
        {context}
    </div>
    """

# ============ MANEJO DE PALABRAS CLAVE ============

def add_keyword(new_keyword: str, show_notifications: bool = True) -> bool:
    """Añade una palabra clave con validación"""
    if not new_keyword:
        if show_notifications:
            from frontend.notifications import show_error
            show_error("Ingresa una palabra clave")
        return False
    
    cleaned = new_keyword.strip().lower()
    
    if not cleaned:
        if show_notifications:
            from frontend.notifications import show_error
            show_error("La palabra clave no puede estar vacía")
        return False
    
    if cleaned in get_session("keywords", {}):
        if show_notifications:
            from frontend.notifications import show_warning
            show_warning(f"'{cleaned}' ya fue añadida")
        return False
    
    set_session("keywords", {**get_session("keywords", {}), cleaned: cleaned})
    
    if show_notifications:
        from frontend.notifications import show_success
        show_success(f"'{cleaned}' añadida")
    
    return True

def remove_keyword(keyword: str) -> None:
    """Elimina una palabra clave"""
    keywords = get_session("keywords", {}).copy()
    keywords.pop(keyword, None)
    set_session("keywords", keywords)

# ============ CHAT HELPERS ============

def add_to_chat_history(role: str, message: str) -> None:
    """Añade mensaje al historial de chat"""
    emoji = "👤" if role == "user" else "🤖"
    role_text = "**Usuario**" if role == "user" else "**IA**"
    st.session_state.chat_history.append(f"{emoji} {role_text}: {message}")
    
    # Limitar historial
    max_history = get_session("chat_history_limit", 50)
    if len(st.session_state.chat_history) > max_history:
        st.session_state.chat_history = st.session_state.chat_history[-max_history:]

def render_chat_message(message: str) -> None:
    """Renderiza un mensaje de chat"""
    if message.startswith("👤"):
        user_text = message.replace("👤 **Usuario**: ", "")
        st.markdown(f"""
        <div class="chat-message chat-message-user">
            <div class="chat-avatar chat-avatar-user avatar-pulse">👤</div>
            <div class="chat-bubble chat-bubble-user">{user_text}</div>
        </div>
        """, unsafe_allow_html=True)
    elif message.startswith("🤖"):
        ai_text = message.replace("🤖 **IA**: ", "")
        st.markdown(f"""
        <div class="chat-message chat-message-ai">
            <div class="chat-avatar chat-avatar-ai avatar-spin">✨</div>
            <div class="chat-bubble chat-bubble-ai">{ai_text}</div>
        </div>
        """, unsafe_allow_html=True)
