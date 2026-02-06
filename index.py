import streamlit as st
import os
import AudioRecorder
import Transcriber
import Model
# Force redeploy with updated credentials - 2026-02-05
import OpportunitiesManager
from datetime import datetime
import hashlib
import database as db_utils
import styles
from notifications import show_success, show_error, show_warning, show_info, show_success_expanded, show_error_expanded, show_info_expanded

# Configuración inicial de la interfaz de usuario
st.set_page_config(layout="wide", page_title="Sistema Control Audio Iprevencion")

# Cargar estilos CSS desde archivo
st.markdown(styles.get_styles(), unsafe_allow_html=True)

# Inicializar objetos
recorder = AudioRecorder.AudioRecorder()
transcriber_model = Transcriber.Transcriber()
chat_model = Model.Model()
opp_manager = OpportunitiesManager.OpportunitiesManager()

# Inicializar estado de sesión
if "processed_audios" not in st.session_state:
    st.session_state.processed_audios = set()  # Audios ya procesados
if "recordings" not in st.session_state:
    st.session_state.recordings = recorder.get_recordings_from_supabase()
if "is_deleting" not in st.session_state:
    st.session_state.is_deleting = False
if "selected_audio" not in st.session_state:
    st.session_state.selected_audio = None
if "upload_key_counter" not in st.session_state:
    st.session_state.upload_key_counter = 0
if "record_key_counter" not in st.session_state:
    st.session_state.record_key_counter = 0

st.title("Sistema Control Audio Iprevencion")

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
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            # Verificar: ¿Es un audio que ya procesamos?
            if audio_hash not in st.session_state.processed_audios:
                try:
                    # Guardar el audio grabado
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recording_{timestamp}.wav"
                    filepath = recorder.save_recording(audio_bytes, filename)
                    
                    # Guardar en Supabase
                    recording_id = db_utils.save_recording_to_db(filename, filepath)
                    
                    # CLAVE: Marcar como procesado ANTES de mostrar mensaje
                    st.session_state.processed_audios.add(audio_hash)
                    
                    # Actualizar lista desde Supabase
                    st.session_state.recordings = recorder.get_recordings_from_supabase()
                    
                    show_success(f"Audio '{filename}' grabado y guardado")
                    
                    # Reset el widget para que no se procese nuevamente
                    st.session_state.record_key_counter += 1
                    
                except Exception as e:
                    show_error(f"Error al grabar: {str(e)}")
    
    # Opción de subir archivo
    st.markdown('<h3 style="color: white;">Sube un archivo de audio</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3", "wav", "m4a", "ogg", "flac", "webm"], key=f"audio_uploader_{st.session_state.upload_key_counter}")
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        if len(audio_bytes) > 0:
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            # Verificar: ¿Es un archivo que ya procesamos?
            if audio_hash not in st.session_state.processed_audios:
                try:
                    filename = uploaded_file.name
                    filepath = recorder.save_recording(audio_bytes, filename)
                    
                    # Guardar en Supabase
                    recording_id = db_utils.save_recording_to_db(filename, filepath)
                    
                    # CLAVE: Marcar como procesado ANTES de mostrar mensaje
                    st.session_state.processed_audios.add(audio_hash)
                    
                    # Actualizar lista desde Supabase
                    st.session_state.recordings = recorder.get_recordings_from_supabase()
                    
                    show_success(f"Archivo '{filename}' cargado y guardado")
                    
                    # Reset el widget para que no se procese nuevamente
                    st.session_state.upload_key_counter += 1
                    
                except Exception as e:
                    show_error(f"Error al cargar: {str(e)}")

with col2:
    st.markdown('<h3 style="color: white;">Audios Guardados</h3>', unsafe_allow_html=True)
    
    # Refresh de la lista de audios desde Supabase cada vez que se renderiza (para sincronizar)
    recordings = recorder.get_recordings_from_supabase()
    st.session_state.recordings = recordings
    
    if recordings:
        show_info(f"Total: {len(recordings)} audio(s)")
        
        # Tabs para diferentes vistas
        tab1, tab2 = st.tabs(["Transcribir", "Gestión en lote"])
        
        with tab1:
            selected_audio = st.selectbox(
                "Selecciona un audio para transcribir",
                recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
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
                        try:
                            # Eliminar de Supabase
                            db_utils.delete_recording_by_filename(selected_audio)
                            # Eliminar localmente
                            recorder.delete_recording(selected_audio)
                            # Limpiar processed_audios para permitir re-agregar si es necesario
                            st.session_state.processed_audios.clear()
                            
                            st.session_state.recordings = recorder.get_recordings_from_supabase()
                            st.session_state.chat_enabled = False
                            st.session_state.loaded_audio = None
                            show_success("Audio eliminado correctamente")
                            st.rerun()
                        except Exception as e:
                            show_error(f"Error al eliminar: {str(e)}")
        
        with tab2:
            st.subheader("Eliminar múltiples audios")
            st.write("Selecciona uno o varios audios para eliminarlos")
            
            audios_to_delete = st.multiselect(
                "Audios a eliminar:",
                recordings,
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
                        
                        try:
                            for audio in audios_to_delete:
                                try:
                                    # Eliminar de Supabase
                                    db_utils.delete_recording_by_filename(audio)
                                    # Eliminar localmente
                                    recorder.delete_recording(audio)
                                    deleted_count += 1
                                except Exception as e:
                                    show_error(f"Error al eliminar {audio}: {e}")
                            
                            # Limpiar processed_audios para permitir re-agregar
                            st.session_state.processed_audios.clear()
                            st.session_state.recordings = recorder.get_recordings_from_supabase()
                            st.session_state.chat_enabled = False
                            show_success(f"{deleted_count} audio(s) eliminado(s) exitosamente")
                            st.rerun()
                        except Exception as e:
                            show_error(f"Error en eliminación: {str(e)}")
                
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
    st.subheader("Palabras Clave Contextualizadas")
    st.caption("Añade palabras clave para que la IA las entienda mejor")
    
    col_kw1, col_kw2, col_kw3 = st.columns([1.5, 1.5, 1])
    with col_kw1:
        new_keyword = st.text_input("Palabra clave:", placeholder="Ej: presupuesto")
    with col_kw2:
        keyword_context = st.text_input("Contexto/Descripción:", placeholder="Ej: total de $5000")
    with col_kw3:
        if st.button("➕ Añadir", use_container_width=True):
            if new_keyword:
                st.session_state.keywords[new_keyword] = keyword_context if keyword_context else "Sin descripción"
                show_success(f"'{new_keyword}' añadida")
                st.rerun()
    
    # Mostrar palabras clave
    if st.session_state.keywords:
        st.write("**📌 Palabras clave configuradas:**")
        for keyword, context in st.session_state.keywords.items():
            col_display = st.columns([0.5, 2, 2, 0.3])
            with col_display[0]:
                st.write("🏷️")
            with col_display[1]:
                st.write(f"**{keyword}**")
            with col_display[2]:
                st.write(f"_{context}_")
            with col_display[3]:
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
                    st.markdown("<div class='ticket-label' style='color: #ef4444; text-transform: none; margin-top: 0;'>Contexto encontrado en el audio</div>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="notification-container notification-info">
                        {opp['full_context']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    new_notes = st.text_area(
                        "Notas y resumen",
                        value=opp.get('notes', ''),
                        placeholder="Escribe el resumen de esta oportunidad de negocio...",
                        height=100,
                        key=f"notes_{idx}",
                        label_visibility="visible"
                    )
                
                with col_opp2:
                    st.markdown("<div class='ticket-label'>Estado</div>", unsafe_allow_html=True)
                    status_options = ["new", "in_progress", "closed", "won"]
                    new_status = st.selectbox(
                        "Estado",
                        status_options,
                        index=status_options.index(opp.get('status', 'new')),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    st.markdown("<div class='ticket-label' style='margin-top: 16px;'>Prioridad</div>", unsafe_allow_html=True)
                    priority_options = ["Low", "Medium", "High"]
                    new_priority = st.selectbox(
                        "Prioridad",
                        priority_options,
                        index=priority_options.index(opp.get('priority', 'Medium')),
                        key=f"priority_{idx}",
                        label_visibility="collapsed"
                    )
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("Guardar cambios", key=f"save_{idx}", use_container_width=True):
                        opp['notes'] = new_notes
                        opp['status'] = new_status
                        opp['priority'] = new_priority
                        if opp_manager.update_opportunity(opp, selected_audio):
                            show_success("Cambios guardados")
                            st.rerun()
                        else:
                            show_error("Error al guardar")
                
                with col_delete:
                    if st.button("Eliminar", key=f"delete_{idx}", use_container_width=True):
                        if opp_manager.delete_opportunity(opp['id'], selected_audio):
                            show_success("Oportunidad eliminada")
                            st.rerun()
                        else:
                            show_error("Error al eliminar")

# SECCIÓN DE CHAT

if st.session_state.get("chat_enabled", False):
    st.header("Asistente IA para Análisis de Reuniones")
    st.caption(f"Conversando sobre: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar palabras clave activas
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