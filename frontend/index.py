import streamlit as st
import sys
import re
from pathlib import Path

# Agregar carpetas al path para importar módulos
app_root = Path(__file__).parent.parent
sys.path.insert(0, str(app_root / "backend"))
sys.path.insert(0, str(app_root / "frontend"))

# Importar configuración y logger
from config import APP_NAME, AUDIO_EXTENSIONS
from logger import get_logger

logger = get_logger(__name__)

# Importar de frontend (misma carpeta)
from AudioRecorder import AudioRecorder
import styles
from notifications import (
    show_success, show_error, show_warning, show_info,
    show_success_expanded, show_error_expanded, show_info_expanded, show_warning_expanded,
    show_success_debug, show_error_debug, show_info_debug
)
from utils import process_audio_file, delete_audio
from performance import get_transcription_cached, is_audio_transcribed, update_opportunity_local, delete_opportunity_local, delete_keyword_local, delete_recording_local, init_optimization_state
from helpers import format_recording_name

# Importar de backend
from Transcriber import Transcriber
from Model import Model
from OpportunitiesManager import OpportunitiesManager
import database as db_utils

from datetime import datetime
from config import CHAT_HISTORY_LIMIT

# ============================================================================
# FUNCIONES DE INICIALIZACIÓN
# ============================================================================

def initialize_session_state(recorder_obj: AudioRecorder) -> None:
    """Inicializa todos los valores del session_state de forma centralizada"""
    session_defaults = {
        "processed_audios": set(),
        "recordings": recorder_obj.get_recordings_from_supabase(),
        "selected_audio": None,
        "upload_key_counter": 0,
        "record_key_counter": 0,
        "keywords": {},
        "delete_confirmation": {},
        "transcription_cache": {},
        "chat_history_limit": CHAT_HISTORY_LIMIT,
        "opp_delete_confirmation": {},
        "debug_log": []  # Registro de eventos para el DEBUG
    }
    
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Función auxiliar para agregar eventos al debug log
def add_debug_event(message: str, event_type: str = "info") -> None:
    """Agrega un evento al registro de debug"""
    if "debug_log" not in st.session_state:
        st.session_state.debug_log = []
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.debug_log.append({
        "time": timestamp,
        "type": event_type,
        "message": message
    })

# ============================================================================
# CONFIGURACIÓN INICIAL DE LA INTERFAZ DE USUARIO
# ============================================================================

st.set_page_config(layout="wide", page_title=APP_NAME)

# Cargar estilos CSS desde archivo
st.markdown(styles.get_styles(), unsafe_allow_html=True)

# Inicializar objetos
recorder = AudioRecorder()
transcriber_model = Transcriber()
chat_model = Model()
opp_manager = OpportunitiesManager()

# Inicializar estado de sesión de forma centralizada
initialize_session_state(recorder)

# Inicializar optimizaciones de performance
init_optimization_state()

st.title(APP_NAME)

# Crear dos columnas principales para la carga
col1, col2 = st.columns([1, 1])

with col1:
    # GRABADORA DE AUDIO EN VIVO (nativa de Streamlit)
    st.markdown('<h3 style="color: white;">Grabadora en vivo</h3>', unsafe_allow_html=True)
    st.caption("Graba directamente desde tu micrófono (sin interrupciones)")
    
    audio_data = st.audio_input("Presiona el botón para grabar:", key=f"audio_recorder_{st.session_state.record_key_counter}")
    
    # Procesar audio grabado SOLO UNA VEZ por hash
    if audio_data is not None:
        audio_bytes = audio_data.getvalue()
        if len(audio_bytes) > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
            success, recording_id = process_audio_file(audio_bytes, filename, recorder, db_utils)
            
            if success:
                # Reset el widget para que no se procese nuevamente
                st.session_state.record_key_counter += 1
    
    # Opción de subir archivo
    st.markdown('<h3 style="color: white;">Sube un archivo de audio</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Selecciona un archivo de audio",
        type=list(AUDIO_EXTENSIONS),
        key=f"audio_uploader_{st.session_state.upload_key_counter}"
    )
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        if len(audio_bytes) > 0:
            filename = uploaded_file.name
            
            success, recording_id = process_audio_file(audio_bytes, filename, recorder, db_utils)
            
            if success:
                # Reset el widget para que no se procese nuevamente
                st.session_state.upload_key_counter += 1

with col2:
    st.markdown('<h3 style="color: white;">🎵 Audios Guardados</h3>', unsafe_allow_html=True)
    
    # Refresh de la lista de audios desde Supabase cada vez que se renderiza (para sincronizar)
    recordings = recorder.get_recordings_from_supabase()
    st.session_state.recordings = recordings
    
    if recordings:
        st.markdown(f"<p style='color: #888; font-size: 0.9rem;'>{len(recordings)} archivo(s)</p>", unsafe_allow_html=True)
        
        # BÚSQUEDA Y FILTRO DE AUDIOS EN TIEMPO REAL
        search_query = st.text_input(
            "🔍 Buscar audio:",
            placeholder="Nombre del archivo...",
            key="audio_search"
        )
        
        # Filtrar audios EN TIEMPO REAL mientras escribe
        if search_query.strip():
            search_safe = re.escape(search_query.strip())
            filtered_recordings = [
                r for r in recordings 
                if search_safe.lower() in r.lower()
            ]
        else:
            filtered_recordings = recordings
        
        if filtered_recordings:
            # Mostrar audios en tarjetas visuales
            for idx, recording in enumerate(filtered_recordings):
                is_transcribed = is_audio_transcribed(recording, db_utils)
                display_name = format_recording_name(recording)
                
                # Tarjeta de audio con diseño mejorado
                card_html = f"""
                <div style="
                    background: rgba(30, 41, 56, 0.8);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 12px;
                    padding: 16px;
                    margin-bottom: 12px;
                    transition: all 0.3s ease;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div style="flex-grow: 1;">
                        <div style="color: white; font-weight: 500; margin-bottom: 4px;">
                            {display_name}
                        </div>
                        <div style="color: #888; font-size: 0.85rem;">
                            {recording.split('.')[-1].upper()} • {"Transcrito ✓" if is_transcribed else "Sin transcribir"}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Botones en fila debajo de la tarjeta
                col_play, col_trans, col_copy, col_delete = st.columns([1, 1, 1, 1], gap="small")
                
                with col_play:
                    if st.button("▶ Play", key=f"play_{idx}_{recording}", use_container_width=True):
                        audio_path = recorder.get_recording_path(recording)
                        extension = recording.split('.')[-1]
                        with open(audio_path, "rb") as f:
                            st.audio(f.read(), format=f"audio/{extension}")
                
                with col_trans:
                    if st.button("📝 Transcribir", key=f"trans_{idx}_{recording}", use_container_width=True):
                        with st.spinner("Transcribiendo..."):
                            try:
                                audio_path = recorder.get_recording_path(recording)
                                transcription = transcriber_model.transcript_audio(audio_path)
                                st.session_state.contexto = transcription.text
                                st.session_state.selected_audio = recording
                                st.session_state.loaded_audio = recording
                                st.session_state.chat_enabled = True
                                st.session_state.keywords = {}
                                
                                # Guardar la transcripción en Supabase
                                transcription_id = db_utils.save_transcription(
                                    recording_filename=recording,
                                    content=transcription.text,
                                    language="es"
                                )
                                
                                add_debug_event(f"Transcripción completada para '{recording}' (ID: {transcription_id})", "success")
                                st.rerun()
                            except Exception as e:
                                show_error_expanded(f"Error al transcribir: {e}")
                
                with col_copy:
                    if st.button("📋 Copiar", key=f"copy_{idx}_{recording}", use_container_width=True):
                        import pyperclip
                        try:
                            pyperclip.copy(recording)
                            show_success_expanded("✓ Nombre copiado")
                        except:
                            st.info("Nombre: " + recording)
                
                with col_delete:
                    if st.button("🗑 Eliminar", key=f"delete_{idx}_{recording}", use_container_width=True):
                        st.session_state.delete_confirmation[recording] = True
                
                # Confirmación de eliminación
                if st.session_state.delete_confirmation.get(recording):
                    st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar '{recording}'?")
                    col_confirm, col_cancel = st.columns(2)
                    
                    with col_confirm:
                        if st.button("✓ Sí, eliminar", key=f"confirm_yes_{idx}_{recording}"):
                            if delete_audio(recording, recorder, db_utils):
                                delete_recording_local(recording)
                                st.session_state.chat_enabled = False
                                st.session_state.loaded_audio = None
                                st.session_state.selected_audio = None
                                st.session_state.delete_confirmation.pop(recording, None)
                                add_debug_event(f"Audio '{recording}' eliminado", "success")
                                st.rerun()
                    
                    with col_cancel:
                        if st.button("✗ Cancelar", key=f"confirm_no_{idx}_{recording}"):
                            st.session_state.delete_confirmation.pop(recording, None)
                            st.rerun()
        else:
            show_warning_expanded(f"No se encontraron audios con '{search_query}'")
    else:
        show_info_expanded("No hay audios guardados. Sube un archivo.")

st.markdown("")
st.markdown("")
st.markdown("")

# SECCIÓN DE TRANSCRIPCIÓN

if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
    st.header("Transcripción del Audio")
    st.caption(f"De: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar transcripción en un contenedor
    with st.container(border=True):
        st.text_area("", st.session_state.contexto, height=200, disabled=True, label_visibility="collapsed")
                    
    
    # SECCIÓN DE PALABRAS CLAVE
    st.markdown('<h3 style="color: white;">Palabras Clave</h3>', unsafe_allow_html=True)
    st.caption("Añade palabras clave para el análisis de oportunidades")
    
    col_kw1, col_kw2 = st.columns([2, 1])
    with col_kw1:
        new_keyword = st.text_input("Palabra clave:", placeholder="Ej: presupuesto", label_visibility="collapsed")
    with col_kw2:
        if st.button("Añadir", use_container_width=True, type="secondary"):
            if new_keyword:
                # Limpiar espacios y convertir a minúsculas
                cleaned_keyword = new_keyword.strip().lower()
                
                # Validar que no esté vacío después de limpiar
                if not cleaned_keyword:
                    show_error_expanded("La palabra clave no puede estar vacía")
                # Validar que no sea duplicada
                elif cleaned_keyword in st.session_state.get("keywords", {}):
                    show_warning_expanded(f"'{cleaned_keyword}' ya fue añadida")
                else:
                    if "keywords" not in st.session_state:
                        st.session_state.keywords = {}
                    st.session_state.keywords[cleaned_keyword] = cleaned_keyword
                    show_success_expanded(f"'{cleaned_keyword}' añadida")
                    st.rerun()
            else:
                show_error_expanded("Ingresa una palabra clave")
    
    # Mostrar palabras clave
    keywords_dict = st.session_state.get("keywords", {})
    if keywords_dict:
        st.markdown('<h4 style="color: white; margin-top: 20px; margin-bottom: 16px;">Palabras clave configuradas</h4>', unsafe_allow_html=True)
        
        # Mostrar palabras clave con botones de eliminar al lado
        for keyword in list(keywords_dict.keys()):
            col_badge, col_delete = st.columns([4, 1])
            
            with col_badge:
                # Badge HTML con palabra
                badge_html = f'<div style="display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg, #0052CC 0%, #003d99 100%); padding: 8px 12px; border-radius: 6px; color: white; font-weight: 500; font-size: 14px;">{keyword}</div>'
                st.markdown(badge_html, unsafe_allow_html=True)
            
            with col_delete:
                if st.button("✕", key=f"del_{keyword}", use_container_width=True, help="Eliminar"):
                    delete_keyword_local(keyword)  # Actualización local instantánea
                    st.rerun()  # ACTUALIZAR UI inmediatamente
        
        # Separador visual
        st.markdown("")
        
        # Botón para generar oportunidades
        if st.button("Analizar y Generar Tickets de Oportunidades", use_container_width=True, type="primary"):
            with st.spinner("Analizando transcripción..."):
                keywords_list = list(st.session_state.keywords.keys())
                opportunities = opp_manager.extract_opportunities(
                    st.session_state.contexto,
                    keywords_list
                )
                
                saved_count = 0
                for opp in opportunities:
                    opp_manager.save_opportunity(opp, st.session_state.selected_audio)
                    saved_count += 1
                
                if saved_count > 0:
                    show_success_expanded(f"{saved_count} ticket(s) de oportunidad generado(s)")
                    add_debug_event(f"Generados {saved_count} ticket(s) de oportunidad", "success")
                    st.session_state.show_opportunities = True
                else:
                    show_warning_expanded("No se encontraron oportunidades con las palabras clave")

st.markdown("")
st.markdown("")
st.markdown("")

# SECCIÓN DE OPORTUNIDADES

if st.session_state.get("chat_enabled", False):
    selected_audio = st.session_state.get("selected_audio", "")
    opportunities = opp_manager.load_opportunities(selected_audio)
    
    if opportunities:
        st.markdown('<h2 style="color: white;">Tickets de Oportunidades de Negocio</h2>', unsafe_allow_html=True)
        
        for idx, opp in enumerate(opportunities):
            # Mostrar número de ocurrencia si hay múltiples
            occurrence_text = ""
            if opp.get('occurrence', 1) > 1:
                occurrence_text = f" (Ocurrencia #{opp['occurrence']})"
            
            with st.expander(f"{opp['keyword']} {occurrence_text} - {opp['created_at']}", expanded=False):
                col_opp1, col_opp2 = st.columns([2, 1])
                
                with col_opp1:
                    st.write("**Contexto encontrado en el audio:**")
                    # Resaltar la palabra clave en azul dentro del contexto
                    highlighted_context = opp['full_context'].replace(
                        opp['keyword'],
                        f'<span style="color: #0052CC; font-weight: 600;">{opp["keyword"]}</span>'
                    )
                    st.markdown(f"""
                    <div class="notification-container notification-info">
                        {highlighted_context}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    new_notes = st.text_area(
                        "Notas y resumen:",
                        value=opp.get('notes', ''),
                        placeholder="Escribe el resumen de esta oportunidad de negocio...",
                        height=100,
                        key=f"notes_{idx}"
                    )
                
                with col_opp2:
                    st.write("**Estado:**")
                    status_options = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
                    status_display_names = list(status_options.keys())
                    current_status = opp.get('status', 'new')
                    current_status_label = [k for k, v in status_options.items() if v == current_status][0]
                    selected_status_label = st.selectbox(
                        "Cambiar estado",
                        status_display_names,
                        index=status_display_names.index(current_status_label),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    new_status = status_options[selected_status_label]
                    
                    st.write("**Prioridad:**")
                    priority_options = {"Baja": "Low", "Media": "Medium", "Alta": "High"}
                    priority_display_names = list(priority_options.keys())
                    current_priority = opp.get('priority', 'Medium')
                    current_priority_label = [k for k, v in priority_options.items() if v == current_priority][0]
                    selected_priority_label = st.selectbox(
                        "Cambiar prioridad",
                        priority_display_names,
                        index=priority_display_names.index(current_priority_label),
                        key=f"priority_{idx}",
                        label_visibility="collapsed"
                    )
                    new_priority = priority_options[selected_priority_label]
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("Guardar cambios", key=f"save_{idx}", use_container_width=True):
                        updates = {
                            "notes": new_notes,
                            "status": new_status,
                            "priority": new_priority
                        }
                        if opp_manager.update_opportunity(opp['id'], updates):
                            # Actualización local instantánea
                            update_opportunity_local(idx, updates)
                            show_success_expanded("✓ Cambios guardados - Actualización instantánea")
                            st.rerun()  # ACTUALIZAR UI inmediatamente
                        else:
                            st.toast("⚠️ Error al guardar")
                
                with col_delete:
                    if st.button("Eliminar", key=f"delete_{idx}", use_container_width=True):
                        st.session_state.opp_delete_confirmation[idx] = True
                    
                    # Mostrar confirmación si está pendiente
                    if st.session_state.opp_delete_confirmation.get(idx):
                        st.warning(f"⚠️ ¿Eliminar '{opp['keyword']}'?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("✓ Sí, eliminar", key=f"opp_confirm_yes_{idx}", use_container_width=True):
                                if opp_manager.delete_opportunity(opp['id']):
                                    # Actualización local instantánea
                                    delete_opportunity_local(idx)
                                    st.session_state.opp_delete_confirmation.pop(idx, None)
                                    show_success_expanded("✓ Oportunidad eliminada - Actualización instantánea")
                                    st.rerun()  # ACTUALIZAR UI inmediatamente
                        with col_no:
                            if st.button("✗ Cancelar", key=f"opp_confirm_no_{idx}", use_container_width=True):
                                st.session_state.opp_delete_confirmation.pop(idx, None)
                                st.rerun()  # ACTUALIZAR UI inmediatamente

st.markdown("")
st.markdown("")
st.markdown("")

# SECCIÓN DE CHAT

if st.session_state.get("chat_enabled", False):
    st.header("Asistente IA para Análisis de Reuniones")
    st.caption(f"Conversando sobre: {st.session_state.get('selected_audio', 'audio')}")
    
    if st.session_state.get("keywords"):
        keywords_list = list(st.session_state.get("keywords", {}).keys())
        if keywords_list:
            show_info_debug(f"Palabras clave activas: {', '.join(keywords_list)}")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        # Mensaje de bienvenida inicial
        st.session_state.chat_history.append("🤖 **IA**: Hola, soy tu asistente de análisis. Estoy aquí para ayudarte a entender tu reunión y extraer información relevante. Cuéntame qué te gustaría analizar.")
    
    # Mostrar historial de chat con estilo profesional
    if st.session_state.chat_history:
        st.markdown("""
        <div class="chat-container">
        """, unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message.startswith("👤"):
                # Mensaje del usuario
                user_text = message.replace("👤 **Usuario**: ", "")
                st.markdown(f"""
                <div class="chat-message chat-message-user">
                    <div class="chat-avatar chat-avatar-user avatar-pulse">�</div>
                    <div class="chat-bubble chat-bubble-user">{user_text}</div>
                </div>
                """, unsafe_allow_html=True)
            elif message.startswith("🤖"):
                # Mensaje de la IA
                ai_text = message.replace("🤖 **IA**: ", "")
                st.markdown(f"""
                <div class="chat-message chat-message-ai">
                    <div class="chat-avatar chat-avatar-ai avatar-spin">✨</div>
                    <div class="chat-bubble chat-bubble-ai">{ai_text}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Campo de entrada centrado
    col_left, col_input, col_right = st.columns([1, 3, 1])
    with col_input:
        user_input = st.chat_input("Escribe tu pregunta o solicitud de análisis...")
    
    if user_input:
        st.session_state.chat_history.append(f"👤 **Usuario**: {user_input}")
        
        with st.spinner("Generando respuesta..."):
            try:
                # Pasar palabras clave al modelo
                keywords = st.session_state.get("keywords", {})
                response = chat_model.call_model(user_input, st.session_state.contexto, keywords)
                st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                
                # Limitar historial a últimos N mensajes para no sobrecargar memoria
                max_history = st.session_state.chat_history_limit
                if len(st.session_state.chat_history) > max_history:
                    st.session_state.chat_history = st.session_state.chat_history[-max_history:]
                
                st.rerun()
            except Exception as e:
                show_error(f"Error al generar respuesta: {e}")
else:
    show_info_expanded("Carga un audio y transcríbelo para habilitar el chat.")

st.markdown("")
st.markdown("")
st.markdown("")

# SECCIÓN DEBUG
with st.expander("🔧 DEBUG - Estado de Supabase"):
    show_info_debug("Probando conexión a Supabase...")
    
    try:
        # Usar el cliente que ya tenemos en database.py
        supabase = db_utils.init_supabase()
        
        if supabase:
            # Contar grabaciones
            test = supabase.table("recordings").select("*", count="exact").execute()
            record_count = len(test.data) if test.data else 0
            
            # Contar oportunidades
            test_opp = supabase.table("opportunities").select("*", count="exact").execute()
            opp_count = len(test_opp.data) if test_opp.data else 0
            
            # Contar transcripciones
            test_trans = supabase.table("transcriptions").select("*", count="exact").execute()
            trans_count = len(test_trans.data) if test_trans.data else 0
            
            show_success_debug("¡Conexión establecida correctamente!")
            show_success_debug(f"Grabaciones en BD: {record_count}")
            show_success_debug(f"Oportunidades en BD: {opp_count}")
            show_success_debug(f"Transcripciones en BD: {trans_count}")
        else:
            show_error_debug("Falta SUPABASE_URL o SUPABASE_KEY en Secrets")
            
    except Exception as e:
        show_error_debug(f"Error de conexión: {str(e)}")
        show_info_debug("Posibles soluciones:")
        st.write("1. Verifica que RLS esté DESHABILITADO en ambas tablas")
        st.write("2. Haz click en 'Reboot app' en el menú (3 puntos arriba)")
        st.write("3. Verifica que no haya espacios en blanco en los Secrets")
    
    # Mostrar registro de eventos
    st.markdown("---")
    st.markdown("**📋 Registro de Eventos:**")
    
    debug_log = st.session_state.get("debug_log", [])
    if debug_log:
        # Mostrar últimos 20 eventos
        for event in debug_log[-20:]:
            time = event.get("time", "??:??:??")
            event_type = event.get("type", "info")
            message = event.get("message", "")
            
            if event_type == "success":
                st.success(f"[{time}] ✓ {message}")
            elif event_type == "error":
                st.error(f"[{time}] ✗ {message}")
            else:
                st.info(f"[{time}] ℹ {message}")
    else:
        st.write("Sin eventos registrados aún")