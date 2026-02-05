"""
Frontend Streamlit para iPrevencion
Interfaz de usuario que se comunica con la API FastAPI mediante requests
"""

import streamlit as st
import requests
import os
from datetime import datetime
import time
import json

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="iPrevencion - Chat de Audio",
    initial_sidebar_state="expanded"
)

# URL de la API (cambiar según el entorno)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# CSS personalizado
st.markdown("""
<style>
@keyframes pulse-glow {
    0% { 
        box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
    }
    70% { 
        box-shadow: 0 0 0 20px rgba(76, 175, 80, 0);
    }
    100% { 
        box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
    }
}

.success-pulse {
    animation: pulse-glow 1.5s infinite;
    padding: 12px 16px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
    border-left: 4px solid #4CAF50;
    font-weight: 500;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 6px;
    color: white;
    font-weight: 600;
    font-size: 14px;
    margin-right: 8px;
}

.badge-recording {
    background: linear-gradient(135deg, #FF6B6B, #FF5252);
}

.badge-upload {
    background: linear-gradient(135deg, #4ECDC4, #44A08D);
}

.badge-saved {
    background: linear-gradient(135deg, #95E77D, #4CAF50);
}

.api-status-ok {
    color: #4CAF50;
    font-weight: bold;
}

.api-status-error {
    color: #FF5252;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ============ INICIALIZACIÓN DE SESIÓN ============

if "access_token" not in st.session_state:
    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.page = "login"

# ============ FUNCIONES DE API ============

def check_api_connection():
    """Verifica que la API esté disponible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def api_call(method: str, endpoint: str, data=None, files=None, headers=None):
    """Helper para hacer llamadas a la API con headers de autorización"""
    url = f"{API_BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {}
    
    # Agregar token de autorización si existe
    if st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            if files:
                response = requests.post(url, data=data, files=files, headers=headers, timeout=60)
            else:
                headers["Content-Type"] = "application/json"
                response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return None, f"Método HTTP no soportado: {method}"
        
        if response.status_code == 401:
            st.session_state.access_token = None
            st.session_state.user = None
            return None, "Sesión expirada. Por favor, inicia sesión de nuevo."
        
        if response.status_code >= 400:
            try:
                error = response.json().get("detail", f"Error {response.status_code}")
            except:
                error = f"Error {response.status_code}: {response.text}"
            return None, error
        
        return response.json(), None
        
    except requests.exceptions.Timeout:
        return None, "Timeout: La API tardó demasiado en responder"
    except requests.exceptions.ConnectionError:
        return None, f"Error de conexión: No se puede conectar a {API_BASE_URL}"
    except Exception as e:
        return None, f"Error: {str(e)}"

# ============ PÁGINAS DE AUTENTICACIÓN ============

def page_login():
    """Página de login"""
    st.title("🔐 iPrevencion - Login")
    
    # Verificar conexión a API
    if not check_api_connection():
        st.error("⚠️ No se puede conectar a la API. Verifica que esté ejecutándose en " + API_BASE_URL)
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Inicia Sesión")
        email = st.text_input("📧 Email:", key="login_email")
        password = st.text_input("🔑 Contraseña:", type="password", key="login_password")
        
        if st.button("Entrar", use_container_width=True, type="primary"):
            if not email or not password:
                st.error("Por favor completa todos los campos")
            else:
                with st.spinner("Autenticando..."):
                    result, error = api_call("POST", "/auth/login", {
                        "email": email,
                        "password": password
                    })
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.session_state.access_token = result["access_token"]
                        st.session_state.user = {"email": email}
                        st.session_state.page = "main"
                        st.rerun()
    
    with col2:
        st.markdown("### Crear Nueva Cuenta")
        new_email = st.text_input("📧 Email:", key="register_email")
        full_name = st.text_input("👤 Nombre Completo:", key="register_name")
        new_password = st.text_input("🔑 Contraseña (mín. 8 caracteres):", type="password", key="register_password")
        confirm_password = st.text_input("🔑 Confirmar Contraseña:", type="password", key="confirm_password")
        
        if st.button("Registrarme", use_container_width=True):
            if not all([new_email, full_name, new_password, confirm_password]):
                st.error("Por favor completa todos los campos")
            elif new_password != confirm_password:
                st.error("Las contraseñas no coinciden")
            elif len(new_password) < 8:
                st.error("La contraseña debe tener al menos 8 caracteres")
            else:
                with st.spinner("Registrando..."):
                    result, error = api_call("POST", "/auth/register", {
                        "email": new_email,
                        "full_name": full_name,
                        "password": new_password
                    })
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.session_state.access_token = result["access_token"]
                        st.session_state.user = {"email": new_email}
                        st.session_state.page = "main"
                        st.success("¡Registrado exitosamente!")
                        time.sleep(1)
                        st.rerun()

def page_main():
    """Página principal de la aplicación"""
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">🎤 iPrevencion - Sistema de Audio Inteligente</h1>
        <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">Graba, transcribe y analiza audios con IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Perfil")
        if st.session_state.user:
            st.write(f"**{st.session_state.user.get('email')}**")
        
        # Resumen del historial
        result, error = api_call("GET", "/history/summary")
        if not error and result:
            st.markdown("### 📊 Resumen")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Audios", result.get("total_audios", 0))
                st.metric("Transcripciones", result.get("transcriptions", 0))
            with col2:
                st.metric("Oportunidades", result.get("opportunities", 0))
                st.metric("Mensajes Chat", result.get("chat_messages", 0))
        
        st.divider()
        
        # Selector de sección
        section = st.radio(
            "Secciones:",
            ["📁 Mis Audios", "💬 Chat", "📈 Historial"],
            key="section_selector"
        )
        
        st.divider()
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.access_token = None
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
    
    # Contenido principal
    if section == "📁 Mis Audios":
        page_audios()
    elif section == "💬 Chat":
        page_chat()
    elif section == "📈 Historial":
        page_historial()

def page_audios():
    """Página de gestión de audios"""
    st.markdown('<span class="badge badge-recording">GRABAR & SUBIR</span>', unsafe_allow_html=True)
    st.subheader("Mis Audios Grabados")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📥 Subir Archivo de Audio")
        uploaded_file = st.file_uploader(
            "Selecciona un archivo de audio:",
            type=["mp3", "wav", "m4a", "flac", "webm", "ogg"]
        )
        
        if uploaded_file is not None:
            if st.button("Subir y Transcribir", type="primary", use_container_width=True):
                with st.spinner("Subiendo y transcribiendo..."):
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    result, error = api_call("POST", "/audios/upload", files=files)
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success(f"✅ Audio '{uploaded_file.name}' subido exitosamente!")
                        st.info("La transcripción se está procesando en background...")
                        time.sleep(1)
                        st.rerun()
    
    with col2:
        st.markdown("### 🎙️ Grabar en Vivo")
        st.caption("(Próximamente: Grabación nativa en el navegador)")
        st.info("Usa el cargue de archivos o graba con tu dispositivo")
    
    st.divider()
    
    # Listar audios
    st.markdown("### 📋 Tus Audios")
    result, error = api_call("GET", "/audios/")
    
    if error:
        st.error(f"Error cargando audios: {error}")
    elif result:
        if not result:
            st.info("No hay audios subidos aún")
        else:
            for audio in result:
                with st.expander(f"🎵 {audio['filename']} - {audio['status'].upper()}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**ID:** {audio['id']}")
                        st.write(f"**Estado:** {audio['status']}")
                        st.write(f"**Fecha:** {audio['created_at']}")
                        if audio['file_size']:
                            size_mb = audio['file_size'] / (1024 * 1024)
                            st.write(f"**Tamaño:** {size_mb:.2f} MB")
                    
                    with col2:
                        if st.button("📝 Ver", key=f"view_{audio['id']}", use_container_width=True):
                            st.session_state.selected_audio_id = audio['id']
                    
                    with col3:
                        if st.button("🗑️ Eliminar", key=f"delete_{audio['id']}", use_container_width=True):
                            with st.spinner("Eliminando..."):
                                _, error = api_call("DELETE", f"/audios/{audio['id']}")
                                if error:
                                    st.error(f"Error: {error}")
                                else:
                                    st.success("Audio eliminado")
                                    time.sleep(1)
                                    st.rerun()
                    
                    # Mostrar transcripción si existe
                    if audio.get("transcription"):
                        st.markdown("#### 📄 Transcripción:")
                        st.text_area(
                            "Texto transcrito:",
                            value=audio["transcription"]["text"],
                            height=100,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                        
                        # Palabras clave
                        if audio["transcription"].get("keywords"):
                            st.markdown("**Palabras Clave:**")
                            keywords = audio["transcription"]["keywords"]
                            st.write(" • " + " • ".join(keywords))
                    
                    # Oportunidades
                    if audio.get("opportunities"):
                        st.markdown("#### 🎯 Oportunidades Identificadas:")
                        for opp in audio["opportunities"]:
                            st.write(f"- **{opp['keyword']}**: {opp['full_context']}")

def page_chat():
    """Página de chat con IA"""
    st.markdown('<span class="badge badge-upload">CHAT</span>', unsafe_allow_html=True)
    st.subheader("💬 Chat Inteligente con IA")
    
    # Obtener lista de audios para contexto
    audios_result, _ = api_call("GET", "/audios/")
    audio_options = {"Sin contexto específico": None}
    if audios_result:
        for audio in audios_result:
            if audio["status"] == "completed":
                audio_options[f"{audio['filename']} ({audio['id']})"] = audio["id"]
    
    # Selector de audio para contexto
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_audio_name = st.selectbox(
            "Usa un audio como contexto:",
            list(audio_options.keys()),
            key="chat_audio_context"
        )
        selected_audio_id = audio_options[selected_audio_name]
    
    with col2:
        if st.button("🔄 Refrescar", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Historial de conversación
    st.markdown("### 📚 Historial de Conversación")
    
    # Obtener historial
    endpoint = f"/chat/history?limit=50" + (f"&audio_id={selected_audio_id}" if selected_audio_id else "")
    history_result, error = api_call("GET", endpoint)
    
    if error:
        st.error(f"Error cargando historial: {error}")
    elif history_result:
        # Mostrar mensajes
        for msg in history_result:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])
    else:
        st.info("No hay mensajes en el historial aún")
    
    st.divider()
    
    # Input de nuevo mensaje
    st.markdown("### ✍️ Envía tu Pregunta")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_message = st.text_area(
            "Tu pregunta:",
            placeholder="Escribe tu pregunta aquí...",
            height=80,
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button(
            "📤 Enviar",
            use_container_width=True,
            type="primary"
        )
    
    if send_button:
        if not user_message.strip():
            st.error("Por favor escribe una pregunta")
        else:
            with st.spinner("Procesando tu pregunta..."):
                result, error = api_call("POST", "/chat/send", {
                    "content": user_message,
                    "audio_id": selected_audio_id
                })
                
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success("Mensaje enviado!")
                    time.sleep(1)
                    st.rerun()

def page_historial():
    """Página de historial completo"""
    st.markdown('<span class="badge badge-saved">HISTORIAL</span>', unsafe_allow_html=True)
    st.subheader("📈 Tu Historial Completo")
    
    # Obtener historial completo
    result, error = api_call("GET", "/history/")
    
    if error:
        st.error(f"Error cargando historial: {error}")
    elif result:
        # Resumen
        st.markdown("### 📊 Resumen del Historial")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total de Audios",
                len(result["audios"]) if result["audios"] else 0
            )
        
        with col2:
            transcriptions_count = sum(1 for a in result["audios"] if a.get("transcription"))
            st.metric("Audios Transcritos", transcriptions_count)
        
        with col3:
            opportunities_count = sum(len(a.get("opportunities", [])) for a in result["audios"])
            st.metric("Oportunidades Encontradas", opportunities_count)
        
        st.divider()
        
        # Timeline de audios
        st.markdown("### 🎤 Timeline de Audios")
        if result["audios"]:
            for audio in result["audios"]:
                with st.expander(f"📋 {audio['filename']} - {audio['created_at']}"):
                    st.write(f"Estado: **{audio['status']}**")
                    
                    if audio.get("transcription"):
                        st.markdown("**Transcripción (primeras 200 chars):**")
                        st.write(audio["transcription"]["text"][:200] + "...")
                    
                    if audio.get("opportunities"):
                        st.markdown("**Oportunidades:**")
                        for opp in audio["opportunities"]:
                            st.write(f"- {opp['keyword']}")
        else:
            st.info("No hay audios en tu historial")

# ============ MAIN ============

def main():
    """Función principal"""
    if st.session_state.page == "login":
        page_login()
    elif st.session_state.page == "main":
        if st.session_state.access_token:
            page_main()
        else:
            st.session_state.page = "login"
            st.rerun()

if __name__ == "__main__":
    main()
