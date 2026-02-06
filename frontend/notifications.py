"""
Funciones centralizadas para mostrar notificaciones
"""
import streamlit as st


def show_success(message: str):
    """Muestra un icono de éxito con tooltip con el mensaje"""
    st.markdown(f"""
    <div class="notification-icon notification-icon-success">
        ✓
        <span class="notification-tooltip">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def show_error(message: str):
    """Muestra un icono de error con tooltip con el mensaje"""
    st.markdown(f"""
    <div class="notification-icon notification-icon-error">
        ✕
        <span class="notification-tooltip">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def show_warning(message: str):
    """Muestra un icono de advertencia con tooltip con el mensaje"""
    st.markdown(f"""
    <div class="notification-icon notification-icon-warning">
        ⚠
        <span class="notification-tooltip">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def show_info(message: str):
    """Muestra un icono de información con tooltip con el mensaje"""
    st.markdown(f"""
    <div class="notification-icon notification-icon-info">
        ℹ
        <span class="notification-tooltip">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def show_success_expanded(message: str):
    """Muestra un mensaje de éxito visible completo (para debug)"""
    st.markdown(f"""
    <div class="notification-expanded notification-expanded-success">
        ✓ {message}
    </div>
    """, unsafe_allow_html=True)


def show_error_expanded(message: str):
    """Muestra un mensaje de error visible completo (para debug)"""
    st.markdown(f"""
    <div class="notification-expanded notification-expanded-error">
        ✕ {message}
    </div>
    """, unsafe_allow_html=True)


def show_info_expanded(message: str):
    """Muestra un mensaje de información visible completo (para debug)"""
    st.markdown(f"""
    <div class="notification-expanded notification-expanded-info">
        ℹ {message}
    </div>
    """, unsafe_allow_html=True)
