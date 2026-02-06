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

# 🎨 DISEÑO MODERNO - IMPORTAR
from modern_ui import (
    inject_modern_css,
    section_header,
    stat_card,
    opportunity_card_modern,
    badge,
    audio_player_modern,
    create_metric_row
)

# Configuración inicial de la interfaz de usuario
st.set_page_config(layout="wide", page_title="🎙️ AudioPro Intelligence")

# ✅ INYECTAR CSS MODERNO PRIMERO (MUY IMPORTANTE)
inject_modern_css()

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

# ============================================================================
# ENCABEZADO CON ESTILO MODERNO
# ============================================================================

st.markdown("""
<div style="text-align: center; margin: 2rem 0; padding: 2rem;">
    <h1 style="font-size: 3rem; margin: 0;">🎙️ AudioPro</h1>
    <p style="color: #B0B8C1; font-size: 1.1rem; margin-top: 0.5rem;">
        Plataforma de IA para Transcripción y Análisis de Audios
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================================
# SECCIÓN 1: GRABACIÓN Y CARGA DE AUDIOS
# ============================================================================

section_header("🎵 Grabación & Carga de Audios", "Sube o graba nuevos audios para analizar")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**📻 Opción 1: Grabar desde Micrófono**")
    st.caption("Graba directamente desde tu micrófono")
    
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
                    
                    st.success(f"✅ Audio '{filename}' grabado y guardado")
                    
                    # Reset el widget para que no se procese nuevamente
                    st.session_state.record_key_counter += 1
                    
                except Exception as e:
                    st.error(f"❌ Error al grabar: {str(e)}")

with col2:
    st.markdown("**📤 Opción 2: Cargar Archivo**")
    st.caption("Sube un archivo de audio existente")
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo de audio",
        type=["mp3", "wav", "m4a", "ogg", "flac", "webm"],
        key=f"audio_uploader_{st.session_state.upload_key_counter}"
    )
    
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
                    
                    st.success(f"✅ Archivo '{filename}' cargado y guardado")
                    
                    # Reset el widget para que no se procese nuevamente
                    st.session_state.upload_key_counter += 1
                    
                except Exception as e:
                    st.error(f"❌ Error al cargar: {str(e)}")

st.divider()

# ============================================================================
# SECCIÓN 2: LISTADO DE AUDIOS CON ESTADÍSTICAS
# ============================================================================

section_header("📂 Audios Disponibles", "Selecciona un audio para analizar")

recordings = recorder.get_recordings_from_supabase()
st.session_state.recordings = recordings

if recordings:
    # Métricas superiores
    all_opportunities = []
    try:
        for rec in recordings:
            opps = opp_manager.load_opportunities(rec)
            all_opportunities.extend(opps)
    except:
        pass
    
    create_metric_row({
        "Total Grabaciones": str(len(recordings)),
        "Oportunidades": str(len(all_opportunities)),
        "Transcripciones": str(len([r for r in recordings if r.get('transcription')]))
    }, cols=3)
    
    st.divider()
    
    # Tabs para diferentes vistas
    tab1, tab2 = st.tabs(["🎙️ Transcribir", "🗑️ Gestión Batch"])
    
    with tab1:
        selected_audio = st.selectbox(
            "Selecciona un audio",
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
                    st.info("✅ Transcripción cargada desde Supabase")
            
            col_play, col_transcribe, col_delete = st.columns([1, 1, 1])
            
            with col_play:
                if st.button("▶️ Reproducir", use_container_width=True):
                    try:
                        audio_path = recorder.get_recording_path(selected_audio)
                        extension = selected_audio.split('.')[-1]
                        with open(audio_path, "rb") as f:
                            st.audio(f.read(), format=f"audio/{extension}")
                    except Exception as e:
                        st.error(f"Error al reproducir: {e}")
            
            with col_transcribe:
                if st.button("🎙️ Transcribir", use_container_width=True):
                    with st.spinner("Transcribiendo audio..."):
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
                            
                            st.success("✅ Transcripción completada y guardada")
                        except Exception as e:
                            st.error(f"Error al transcribir: {e}")
            
            with col_delete:
                if st.button("🗑️ Eliminar", use_container_width=True):
                    try:
                        db_utils.delete_recording_by_filename(selected_audio)
                        recorder.delete_recording(selected_audio)
                        st.session_state.processed_audios.clear()
                        st.session_state.recordings = recorder.get_recordings_from_supabase()
                        st.session_state.chat_enabled = False
                        st.session_state.loaded_audio = None
                        st.success("✅ Audio eliminado correctamente")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al eliminar: {str(e)}")
    
    with tab2:
        st.subheader("🗑️ Eliminar Múltiples Audios")
        st.write("Selecciona uno o varios audios para eliminarlos")
        
        audios_to_delete = st.multiselect(
            "Audios a eliminar:",
            recordings,
            format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
        )
        
        if audios_to_delete:
            st.warning(f"⚠️ Vas a eliminar {len(audios_to_delete)} audio(s)")
            
            st.write("**Audios seleccionados:**")
            for audio in audios_to_delete:
                badge(audio, "info")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirmar Eliminación", use_container_width=True):
                    deleted_count = 0
                    
                    try:
                        for audio in audios_to_delete:
                            try:
                                db_utils.delete_recording_by_filename(audio)
                                recorder.delete_recording(audio)
                                deleted_count += 1
                            except Exception as e:
                                st.error(f"Error al eliminar {audio}: {e}")
                        
                        st.session_state.processed_audios.clear()
                        st.session_state.recordings = recorder.get_recordings_from_supabase()
                        st.session_state.chat_enabled = False
                        st.success(f"✅ {deleted_count} audio(s) eliminado(s)")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

else:
    st.info("📭 No hay audios guardados. Carga uno para comenzar.")

st.divider()

# ============================================================================
# SECCIÓN 3: TRANSCRIPCIÓN
# ============================================================================

if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
    section_header("📝 Transcripción del Audio", f"De: {st.session_state.get('selected_audio', 'audio')}")
    
    st.text_area("", st.session_state.contexto, height=180, disabled=True, label_visibility="collapsed")
    
    st.divider()
    
    # ========================================================================
    # SECCIÓN 4: PALABRAS CLAVE
    # ========================================================================
    
    section_header("🔑 Palabras Clave Contextualizadas", "Define palabras clave para buscar oportunidades")
    
    col_kw1, col_kw2, col_kw3 = st.columns([1.5, 1.5, 1])
    with col_kw1:
        new_keyword = st.text_input(
            "Palabra clave:",
            placeholder="Ej: presupuesto, reunión, contrato...",
            label_visibility="collapsed"
        )
    with col_kw2:
        keyword_context = st.text_input(
            "Contexto/Descripción:",
            placeholder="Ej: total de $5000",
            label_visibility="collapsed"
        )
    with col_kw3:
        st.write("")
        if st.button("➕ Agregar Palabra", use_container_width=True):
            if new_keyword:
                st.session_state.keywords[new_keyword] = keyword_context if keyword_context else "Sin descripción"
                st.success(f"✅ '{new_keyword}' agregada")
                st.rerun()
    
    # Mostrar palabras clave
    if st.session_state.keywords:
        st.write("**📌 Palabras clave configuradas:**")
        kw_cols = st.columns(3)
        for idx, (keyword, context) in enumerate(st.session_state.keywords.items()):
            with kw_cols[idx % 3]:
                badge(keyword, "status-new")
                st.caption(f"_{context}_")
                
                if st.button("✖️ Eliminar", key=f"del_{keyword}", use_container_width=True):
                    del st.session_state.keywords[keyword]
                    st.rerun()
        
        st.divider()
        
        # Botón para generar oportunidades
        if st.button("🎯 Analizar y Generar Tickets", use_container_width=True):
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
                    st.success(f"✅ {saved_count} ticket(s) generado(s)")
                    st.session_state.show_opportunities = True
                    st.rerun()
                else:
                    st.warning("⚠️ No se encontraron oportunidades")
    
    st.divider()
    
    # ========================================================================
    # SECCIÓN 5: OPORTUNIDADES CON TARJETAS MODERNAS
    # ========================================================================
    
    selected_audio = st.session_state.get("selected_audio", "")
    opportunities = opp_manager.load_opportunities(selected_audio)
    
    if opportunities:
        section_header("🎯 Tickets de Oportunidades", "Gestiona las oportunidades identificadas")
        
        for idx, opp in enumerate(opportunities):
            # Encabezado del ticket
            col_title, col_buttons = st.columns([3, 1])
            
            with col_title:
                opportunity_card_modern(
                    ticket_number=opp.get('ticket_number', idx + 1),
                    title=opp.get('keyword', 'Sin título'),
                    description=opp.get('full_context', opp.get('description', 'Sin descripción')),
                    status=opp.get('status', 'new'),
                    priority=opp.get('priority', 'Medium'),
                    notes=opp.get('notes', ''),
                    created_at=opp.get('created_at', 'N/A')
                )
            
            with st.expander("✏️ Editar Detalles", expanded=False):
                col_edit1, col_edit2 = st.columns(2)
                
                with col_edit1:
                    st.write("**Estado:**")
                    status_options = ["new", "in_progress", "closed", "won"]
                    new_status = st.selectbox(
                        "Cambiar estado",
                        status_options,
                        index=status_options.index(opp.get('status', 'new')),
                        key=f"status_{idx}",
                        label_visibility="collapsed"
                    )
                
                with col_edit2:
                    st.write("**Prioridad:**")
                    priority_options = ["Low", "Medium", "High"]
                    new_priority = st.selectbox(
                        "Cambiar prioridad",
                        priority_options,
                        index=priority_options.index(opp.get('priority', 'Medium')),
                        key=f"priority_{idx}",
                        label_visibility="collapsed"
                    )
                
                st.write("**Notas:**")
                new_notes = st.text_area(
                    "Notas del ticket",
                    value=opp.get('notes', ''),
                    placeholder="Escribe observaciones...",
                    height=100,
                    key=f"notes_{idx}",
                    label_visibility="collapsed"
                )
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar Cambios", key=f"save_{idx}", use_container_width=True):
                        opp['notes'] = new_notes
                        opp['status'] = new_status
                        opp['priority'] = new_priority
                        if opp_manager.update_opportunity(opp, selected_audio):
                            st.success("✅ Cambios guardados")
                            st.rerun()
                        else:
                            st.error("❌ Error al guardar")
                
                with col_delete:
                    if st.button("🗑️ Eliminar Ticket", key=f"delete_{idx}", use_container_width=True):
                        if opp_manager.delete_opportunity(opp['id'], selected_audio):
                            st.success("✅ Eliminado")
                            st.rerun()
                        else:
                            st.error("❌ Error al eliminar")
    
    st.divider()
    
    # ========================================================================
    # SECCIÓN 6: CHAT CON IA
    # ========================================================================
    
    section_header("💬 Chat Inteligente", "Realiza preguntas sobre tu audio")
    
    if st.session_state.get("keywords"):
        keywords_text = ", ".join(st.session_state.keywords.keys())
        st.info(f"🏷️ Palabras clave activas: {keywords_text}")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        st.write(message)
    
    # Campo de entrada
    user_input = st.chat_input("Escribe tu pregunta sobre el audio:")
    
    if user_input:
        st.session_state.chat_history.append(f"👤 **Tú**: {user_input}")
        
        with st.spinner("🤖 Generando respuesta..."):
            try:
                keywords = st.session_state.get("keywords", {})
                response = chat_model.call_model(user_input, st.session_state.contexto, keywords)
                st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.info("👆 Carga un audio, transcríbelo y agrega palabras clave para activar todas las funciones.")

st.divider()

# ============================================================================
# SECCIÓN 7: DEBUG Y MONITOR
# ============================================================================

with st.expander("🔧 Monitor del Sistema", expanded=False):
    st.info("📊 Estado de Supabase y estadísticas generales")
    
    try:
        supabase = db_utils.init_supabase()
        
        if supabase:
            test = supabase.table("recordings").select("*", count="exact").execute()
            record_count = len(test.data) if test.data else 0
            
            test_opp = supabase.table("opportunities").select("*", count="exact").execute()
            opp_count = len(test_opp.data) if test_opp.data else 0
            
            test_trans = supabase.table("transcriptions").select("*", count="exact").execute()
            trans_count = len(test_trans.data) if test_trans.data else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                stat_card("Grabaciones", str(record_count), "🎵", "cyan")
            with col2:
                stat_card("Oportunidades", str(opp_count), "📋", "purple")
            with col3:
                stat_card("Transcripciones", str(trans_count), "📝", "low")
            
            st.success("✅ Conexión a Supabase establecida")
        else:
            st.error("❌ Falta configuración en Secrets")
            
    except Exception as e:
        st.error(f"❌ Error de conexión: {str(e)}")
