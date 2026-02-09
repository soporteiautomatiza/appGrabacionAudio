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
from notifications import show_success, show_error, show_warning, show_info, show_success_expanded, show_error_expanded, show_info_expanded
from utils import process_audio_file, delete_audio

# Importar de backend
from Transcriber import Transcriber
from Model import Model
from OpportunitiesManager import OpportunitiesManager
import database as db_utils

from datetime import datetime

# Configuración inicial de la interfaz de usuario
st.set_page_config(layout="wide", page_title=APP_NAME)

# Cargar estilos CSS desde archivo
st.markdown(styles.get_styles(), unsafe_allow_html=True)

# Inicializar objetos
recorder = AudioRecorder()
transcriber_model = Transcriber()
chat_model = Model()
opp_manager = OpportunitiesManager()

# Inicializar estado de sesión
if "processed_audios" not in st.session_state:
    st.session_state.processed_audios = set()  # Audios ya procesados
if "recordings" not in st.session_state:
    st.session_state.recordings = recorder.get_recordings_from_supabase()
if "selected_audio" not in st.session_state:
    st.session_state.selected_audio = None
if "upload_key_counter" not in st.session_state:
    st.session_state.upload_key_counter = 0
if "record_key_counter" not in st.session_state:
    st.session_state.record_key_counter = 0
if "keywords" not in st.session_state:
    st.session_state.keywords = {}  # Palabras clave
if "delete_confirmation" not in st.session_state:
    st.session_state.delete_confirmation = {}  # Confirmacion de eliminacion
if "transcription_cache" not in st.session_state:
    st.session_state.transcription_cache = {}  # Caché de transcripciones
if "chat_history_limit" not in st.session_state:
    st.session_state.chat_history_limit = 50  # Límite máximo de mensajes en chat
if "opp_delete_confirmation" not in st.session_state:
    st.session_state.opp_delete_confirmation = {}  # Confirmación de eliminación de oportunidades

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
    st.markdown('<h3 style="color: white;">Audios Guardados</h3>', unsafe_allow_html=True)
    
    # Refresh de la lista de audios desde Supabase cada vez que se renderiza (para sincronizar)
    recordings = recorder.get_recordings_from_supabase()
    st.session_state.recordings = recordings
    
    if recordings:
        show_info(f"Total: {len(recordings)} audio(s)")
        
        # BÚSQUEDA Y FILTRO DE AUDIOS EN TIEMPO REAL
        search_query = st.text_input(
            "🔍 Buscar audio:",
            placeholder="Nombre del archivo...",
            key="audio_search"
        )
        
        # Filtrar audios EN TIEMPO REAL mientras escribe
        if search_query.strip():
            # Escapar caracteres especiales para evitar problemas con regex
            search_safe = re.escape(search_query.strip())
            filtered_recordings = [
                r for r in recordings 
                if search_safe.lower() in r.lower()
            ]
            
            # Mostrar resultados en tiempo real
            if filtered_recordings:
                st.markdown(f"**📌 {len(filtered_recordings)} resultado(s):**")
                for recording in filtered_recordings:
                    display_name = recording.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
                    # Usar caché para evitar múltiples queries a Supabase
                    if recording not in st.session_state.transcription_cache:
                        st.session_state.transcription_cache[recording] = db_utils.get_transcription_by_filename(recording)
                    is_transcribed = " ✓ Transcrito" if st.session_state.transcription_cache[recording] else ""
                    st.caption(f"🎵 {display_name}{is_transcribed}")
            else:
                show_warning(f"No se encontraron audios con '{search_query}'")
        else:
            filtered_recordings = recordings
        
        # Tabs para diferentes vistas
        tab1, tab2 = st.tabs(["Transcribir", "Gestión en lote"])
        
        with tab1:
            selected_audio = st.selectbox(
                "Selecciona un audio para transcribir",
                filtered_recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "") + (
                    " ✓ Transcrito" if st.session_state.transcription_cache.get(x) or db_utils.get_transcription_by_filename(x) else ""
                )
            )
            
            if selected_audio:
                # Cargar transcripción existente automáticamente si existe
                if selected_audio != st.session_state.get("loaded_audio"):
                    existing_transcription = db_utils.get_transcription_by_filename(selected_audio)
                    if existing_transcription:
                        st.session_state.contexto = existing_transcription["content"]
                        st.session_state.selected_audio = selected_audio
                        st.session_state.loaded_audio = selected_audio
                        st.session_state.chat_enabled = True
                        st.session_state.keywords = {}
                        show_info("Transcripción cargada desde Supabase")
                
                col_play, col_transcribe, col_delete = st.columns([1, 1, 1])
                
                with col_play:
                    if st.button("Reproducir"):
                        audio_path = recorder.get_recording_path(selected_audio)
                        extension = selected_audio.split('.')[-1]
                        with open(audio_path, "rb") as f:
                            st.audio(f.read(), format=f"audio/{extension}")
                
                with col_transcribe:
                    if st.button("Transcribir"):
                        with st.spinner("Transcribiendo..."):
                            try:
                                audio_path = recorder.get_recording_path(selected_audio)
                                transcription = transcriber_model.transcript_audio(audio_path)
                                st.session_state.contexto = transcription.text
                                st.session_state.selected_audio = selected_audio
                                st.session_state.loaded_audio = selected_audio
                                st.session_state.chat_enabled = True
                                st.session_state.keywords = {}
                                
                                # Guardar la transcripción en Supabase
                                transcription_id = db_utils.save_transcription(
                                    recording_filename=selected_audio,
                                    content=transcription.text,
                                    language="es"
                                )
                                
                                show_success("Transcripción completada y guardada en Supabase")
                            except Exception as e:
                                show_error(f"Error al transcribir: {e}")
                
                with col_delete:
                    if st.button("Eliminar", key=f"delete_{selected_audio}"):
                        # Pedir confirmación
                        st.session_state.delete_confirmation[selected_audio] = True
                        st.rerun()
                    
                    # Mostrar confirmación si está pendiente
                    if st.session_state.delete_confirmation.get(selected_audio):
                        st.warning(f"⚠️ ¿Eliminar '{selected_audio}'?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("✓ Sí, eliminar", key=f"confirm_yes_{selected_audio}"):
                                if delete_audio(selected_audio, recorder, db_utils):
                                    st.session_state.chat_enabled = False
                                    st.session_state.loaded_audio = None
                                    st.session_state.selected_audio = None
                                    st.session_state.delete_confirmation.pop(selected_audio, None)
                                    st.toast(f"✓ '{selected_audio}' eliminado")
                                    st.rerun()  # Actualizar UI inmediatamente
                        with col_no:
                            if st.button("✗ Cancelar", key=f"confirm_no_{selected_audio}"):
                                st.session_state.delete_confirmation.pop(selected_audio, None)
                                st.toast("Cancelado")
                                st.rerun()  # Limpiar UI de confirmación
        
        with tab2:
            st.subheader("Eliminar múltiples audios")
            st.write("Selecciona uno o varios audios para eliminarlos")
            
            audios_to_delete = st.multiselect(
                "Audios a eliminar:",
                filtered_recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
            )
            
            if audios_to_delete:
                show_warning(f"Vas a eliminar {len(audios_to_delete)} audio(s)")
                
                st.write("**Audios seleccionados:**")
                for audio in audios_to_delete:
                    st.write(f"  • {audio}")
                
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("Eliminar seleccionados", type="primary", use_container_width=True, key="delete_batch"):
                        deleted_count = 0
                        
                        # Eliminar todos localmente primero para respuesta inmediata
                        for audio in audios_to_delete:
                            if delete_audio(audio, recorder, db_utils):
                                deleted_count += 1
                        
                        # Limpiar estado de sesión
                        st.session_state.chat_enabled = False
                        st.session_state.selected_audio = None
                        
                        if deleted_count > 0:
                            st.toast(f"✓ {deleted_count} audio(s) eliminado(s)")
                            st.rerun()  # Actualizar UI inmediatamente
                
                with col_cancel:
                    st.write("")
    else:
        show_info("No hay audios guardados. Sube un archivo.")

# SECCIÓN DE TRANSCRIPCIÓN

if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
    st.header("Transcripción del Audio")
    st.caption(f"De: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar transcripción en un contenedor
    with st.container(border=True):
        st.text_area("", st.session_state.contexto, height=200, disabled=True, label_visibility="collapsed")
    
    # SECCIÓN DE PALABRAS CLAVE
    st.subheader("Palabras Clave")
    st.caption("Añade palabras clave para el análisis de oportunidades")
    
    col_kw1, col_kw2 = st.columns([2, 1])
    with col_kw1:
        new_keyword = st.text_input("Palabra clave:", placeholder="Ej: presupuesto")
    with col_kw2:
        if st.button("➕ Añadir", use_container_width=True):
            if new_keyword:
                # Limpiar espacios y convertir a minúsculas
                cleaned_keyword = new_keyword.strip().lower()
                
                # Validar que no esté vacío después de limpiar
                if not cleaned_keyword:
                    show_error("La palabra clave no puede estar vacía")
                # Validar que no sea duplicada
                elif cleaned_keyword in st.session_state.keywords:
                    show_warning(f"'{cleaned_keyword}' ya fue añadida")
                else:
                    st.session_state.keywords[cleaned_keyword] = cleaned_keyword
                    show_success(f"'{cleaned_keyword}' añadida")
                    st.rerun()
            else:
                show_error("Ingresa una palabra clave")
    
    # Mostrar palabras clave
    if st.session_state.keywords:
        st.write("**📌 Palabras clave configuradas:**")
        for keyword in st.session_state.keywords.keys():
            col_display = st.columns([0.5, 2.5, 0.3])
            with col_display[0]:
                st.write("🏷️")
            with col_display[1]:
                st.write(f"**{keyword}**")
            with col_display[2]:
                if st.button("✖️", key=f"del_{keyword}"):
                    del st.session_state.keywords[keyword]
                    st.rerun()
        
        # Botón para generar oportunidades
        if st.button("🎯 Analizar y Generar Tickets de Oportunidades", use_container_width=True, type="primary"):
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
                    show_success(f"{saved_count} ticket(s) de oportunidad generado(s)")
                    st.session_state.show_opportunities = True
                    st.rerun()
                else:
                    show_warning("No se encontraron oportunidades con las palabras clave")

# SECCIÓN DE OPORTUNIDADES

if st.session_state.get("chat_enabled", False):
    selected_audio = st.session_state.get("selected_audio", "")
    opportunities = opp_manager.load_opportunities(selected_audio)
    
    if opportunities:
        st.header("🎟️ Tickets de Oportunidades de Negocio")
        
        for idx, opp in enumerate(opportunities):
            # Mostrar número de ocurrencia si hay múltiples
            occurrence_text = ""
            if opp.get('occurrence', 1) > 1:
                occurrence_text = f" (Ocurrencia #{opp['occurrence']})"
            
            with st.expander(f"📌 {opp['keyword']}{occurrence_text} - {opp['created_at']}", expanded=False):
                col_opp1, col_opp2 = st.columns([2, 1])
                
                with col_opp1:
                    st.write("**Contexto encontrado en el audio:**")
                    st.markdown(f"""
                    <div class="notification-container notification-info">
                        {opp['full_context']}
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
                    status_options = ["new", "in_progress", "closed", "won"]
                    new_status = st.selectbox(
                        "Cambiar estado",
                        status_options,
                        index=status_options.index(opp.get('status', 'new')),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    st.write("**Prioridad:**")
                    priority_options = ["Low", "Medium", "High"]
                    new_priority = st.selectbox(
                        "Cambiar prioridad",
                        priority_options,
                        index=priority_options.index(opp.get('priority', 'Medium')),
                        key=f"priority_{idx}",
                        label_visibility="collapsed"
                    )
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar cambios", key=f"save_{idx}", use_container_width=True):
                        opp['notes'] = new_notes
                        opp['status'] = new_status
                        opp['priority'] = new_priority
                        if opp_manager.update_opportunity(opp, selected_audio):
                            st.toast("✓ Cambios guardados")
                            st.rerun()  # Actualizar cambios inmediatamente
                        else:
                            st.toast("⚠️ Error al guardar")
                
                with col_delete:
                    if st.button("🗑️ Eliminar", key=f"delete_{idx}", use_container_width=True):
                        st.session_state.opp_delete_confirmation[idx] = True
                        st.rerun()
                    
                    # Mostrar confirmación si está pendiente
                    if st.session_state.opp_delete_confirmation.get(idx):
                        st.warning(f"⚠️ ¿Eliminar '{opp['keyword']}'?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("✓ Sí, eliminar", key=f"opp_confirm_yes_{idx}", use_container_width=True):
                                if opp_manager.delete_opportunity(opp['id'], selected_audio):
                                    st.session_state.opp_delete_confirmation.pop(idx, None)
                                    st.toast("✓ Oportunidad eliminada")
                                    st.rerun()  # Actualizar UI inmediatamente
                                else:
                                    st.toast("⚠️ Error al eliminar")
                        with col_no:
                            if st.button("✗ Cancelar", key=f"opp_confirm_no_{idx}", use_container_width=True):
                                st.session_state.opp_delete_confirmation.pop(idx, None)
                                st.toast("Cancelado")
                                st.rerun()  # Limpiar UI de confirmación

# SECCIÓN DE CHAT

if st.session_state.get("chat_enabled", False):
    st.header("Asistente IA para Análisis de Reuniones")
    st.caption(f"Conversando sobre: {st.session_state.get('selected_audio', 'audio')}")
    
    if st.session_state.get("keywords"):
        show_info(f"Palabras clave activas: {', '.join(st.session_state.keywords.keys())}")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
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
    show_info("Carga un audio y transcríbelo para habilitar el chat.")

# SECCIÓN DEBUG
with st.expander("🔧 DEBUG - Estado de Supabase"):
    show_info_expanded("Probando conexión a Supabase...")
    
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
            
            show_success_expanded("¡Conexión establecida correctamente!")
            show_success_expanded(f"Grabaciones en BD: {record_count}")
            show_success_expanded(f"Oportunidades en BD: {opp_count}")
            show_success_expanded(f"Transcripciones en BD: {trans_count}")
        else:
            show_error_expanded("Falta SUPABASE_URL o SUPABASE_KEY en Secrets")
            
    except Exception as e:
        show_error_expanded(f"Error de conexión: {str(e)}")
        show_info_expanded("Posibles soluciones:")
        st.write("1. Verifica que RLS esté DESHABILITADO en ambas tablas")
        st.write("2. Haz click en 'Reboot app' en el menú (3 puntos arriba)")
        st.write("3. Verifica que no haya espacios en blanco en los Secrets")