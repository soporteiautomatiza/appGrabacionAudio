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
        "debug_log": []
    }
    
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

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
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    layout="wide", 
    page_title=APP_NAME,
    page_icon="🎙️",
    initial_sidebar_state="collapsed"
)

# Cargar estilos CSS desde archivo
st.markdown(styles.get_styles(), unsafe_allow_html=True)

# Inicializar objetos
recorder = AudioRecorder()
transcriber_model = Transcriber()
chat_model = Model()
opp_manager = OpportunitiesManager()

# Inicializar estado de sesión
initialize_session_state(recorder)
init_optimization_state()

# ============================================================================
# HEADER Y SIDEBAR
# ============================================================================

# Sidebar para navegación
with st.sidebar:
    st.title("🔧 Navegación")
    st.markdown("---")
    
    # Secciones de la aplicación
    sections = {
        "🎙️ Grabación y Subida": "record",
        "📁 Audios Guardados": "audios",
        "📝 Transcripción": "transcription",
        "🏷️ Palabras Clave": "keywords",
        "🎯 Oportunidades": "opportunities",
        "💬 Chat IA": "chat",
        "🔍 Debug": "debug"
    }
    
    selected_section = st.radio(
        "Ir a sección:",
        list(sections.keys()),
        label_visibility="collapsed"
    )
    
    # Stats en sidebar
    st.markdown("---")
    st.markdown("### 📊 Estadísticas")
    
    recordings = st.session_state.get("recordings", [])
    opportunities = opp_manager.load_opportunities(st.session_state.get("selected_audio", ""))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Audios", len(recordings))
    with col2:
        st.metric("Oportunidades", len(opportunities) if opportunities else 0)
    
    st.markdown("---")
    
    # Botón para limpiar estado (solo desarrollo)
    if st.button("🔄 Limpiar cache local"):
        for key in ["keywords", "delete_confirmation", "opp_delete_confirmation"]:
            if key in st.session_state:
                st.session_state[key] = {}
        st.rerun()

# ============================================================================
# HEADER PRINCIPAL
# ============================================================================

st.markdown(f"<h1 style='text-align: center; margin-bottom: 10px;'>{APP_NAME}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 40px;'>Transcripción inteligente y análisis de oportunidades en reuniones</p>", unsafe_allow_html=True)

# ============================================================================
# SECCIÓN 1: GRABACIÓN Y SUBIDA
# ============================================================================

if sections[selected_section] == "record":
    st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">🎙️ Grabación y Subida</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # Tarjeta de grabadora
        with st.container(border=True):
            st.markdown('<h3 style="color: #3B82F6; margin-bottom: 15px;">🎤 Grabación en Vivo</h3>', unsafe_allow_html=True)
            st.caption("Graba audio directamente desde tu micrófono")
            
            audio_data = st.audio_input(
                "Presiona para grabar:",
                key=f"audio_recorder_{st.session_state.record_key_counter}",
                help="La grabación comenzará inmediatamente al presionar el botón"
            )
            
            if audio_data is not None:
                audio_bytes = audio_data.getvalue()
                if len(audio_bytes) > 0:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"grabacion_{timestamp}.wav"
                    
                    with st.spinner("Guardando grabación..."):
                        success, recording_id = process_audio_file(audio_bytes, filename, recorder, db_utils)
                        
                        if success:
                            st.session_state.record_key_counter += 1
                            st.success(f"✅ Grabación '{filename}' guardada exitosamente")
                            st.balloons()

    with col2:
        # Tarjeta de subida
        with st.container(border=True):
            st.markdown('<h3 style="color: #3B82F6; margin-bottom: 15px;">📁 Subir Archivo</h3>', unsafe_allow_html=True)
            st.caption(f"Formatos soportados: {', '.join(AUDIO_EXTENSIONS)}")
            
            uploaded_file = st.file_uploader(
                "Selecciona un archivo de audio",
                type=list(AUDIO_EXTENSIONS),
                key=f"audio_uploader_{st.session_state.upload_key_counter}",
                help="Arrastra y suelta o haz clic para seleccionar"
            )
            
            if uploaded_file is not None:
                audio_bytes = uploaded_file.read()
                if len(audio_bytes) > 0:
                    filename = uploaded_file.name
                    
                    with st.spinner("Procesando archivo..."):
                        success, recording_id = process_audio_file(audio_bytes, filename, recorder, db_utils)
                        
                        if success:
                            st.session_state.upload_key_counter += 1
                            st.success(f"✅ Archivo '{filename}' subido exitosamente")

# ============================================================================
# SECCIÓN 2: AUDIOS GUARDADOS
# ============================================================================

elif sections[selected_section] == "audios":
    st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">📁 Audios Guardados</h2>', unsafe_allow_html=True)
    
    # Refresh de la lista de audios
    recordings = recorder.get_recordings_from_supabase()
    st.session_state.recordings = recordings
    
    if recordings:
        # Barra de búsqueda y filtros
        col_search, col_filter = st.columns([3, 1])
        
        with col_search:
            search_query = st.text_input(
                "🔍 Buscar audio:",
                placeholder="Nombre del archivo...",
                key="audio_search"
            )
        
        with col_filter:
            filter_option = st.selectbox(
                "Filtrar por:",
                ["Todos", "Transcritos", "Sin transcribir"],
                key="audio_filter"
            )
        
        # Filtrar audios
        filtered_recordings = recordings
        
        if search_query.strip():
            search_safe = re.escape(search_query.strip())
            filtered_recordings = [
                r for r in filtered_recordings 
                if search_safe.lower() in r.lower()
            ]
        
        if filter_option == "Transcritos":
            filtered_recordings = [r for r in filtered_recordings if is_audio_transcribed(r, db_utils)]
        elif filter_option == "Sin transcribir":
            filtered_recordings = [r for r in filtered_recordings if not is_audio_transcribed(r, db_utils)]
        
        # Mostrar resultados
        if filtered_recordings:
            st.info(f"📊 Mostrando {len(filtered_recordings)} de {len(recordings)} audios")
            
            # Tabs para diferentes vistas
            tab1, tab2 = st.tabs(["📝 Vista Individual", "🗑️ Gestión en Lote"])
            
            with tab1:
                selected_audio = st.selectbox(
                    "Selecciona un audio para trabajar:",
                    filtered_recordings,
                    format_func=lambda x: format_recording_name(x) + (
                        " ✅" if is_audio_transcribed(x, db_utils) else " ⏳"
                    ),
                    key=f"selectbox_audio_{len(filtered_recordings)}"
                )
                
                if selected_audio:
                    # Cargar transcripción existente automáticamente
                    if selected_audio != st.session_state.get("loaded_audio"):
                        existing_transcription = db_utils.get_transcription_by_filename(selected_audio)
                        if existing_transcription:
                            st.session_state.contexto = existing_transcription["content"]
                            st.session_state.selected_audio = selected_audio
                            st.session_state.loaded_audio = selected_audio
                            st.session_state.chat_enabled = True
                            st.session_state.keywords = {}
                    
                    # Panel de acciones para el audio seleccionado
                    col_info, col_actions = st.columns([2, 1])
                    
                    with col_info:
                        st.markdown(f"**Archivo:** `{selected_audio}`")
                        status = "✅ Transcrito" if is_audio_transcribed(selected_audio, db_utils) else "⏳ Sin transcribir"
                        st.markdown(f"**Estado:** {status}")
                    
                    with col_actions:
                        st.markdown("**Acciones:**")
                        
                        # Botones en una cuadrícula
                        col_play, col_trans, col_del = st.columns(3)
                        
                        with col_play:
                            if st.button("▶️", help="Reproducir audio", use_container_width=True):
                                audio_path = recorder.get_recording_path(selected_audio)
                                extension = selected_audio.split('.')[-1]
                                with open(audio_path, "rb") as f:
                                    st.audio(f.read(), format=f"audio/{extension}")
                        
                        with col_trans:
                            if st.button("📝", help="Transcribir audio", use_container_width=True):
                                with st.spinner("Transcribiendo..."):
                                    try:
                                        audio_path = recorder.get_recording_path(selected_audio)
                                        transcription = transcriber_model.transcript_audio(audio_path)
                                        st.session_state.contexto = transcription.text
                                        st.session_state.selected_audio = selected_audio
                                        st.session_state.loaded_audio = selected_audio
                                        st.session_state.chat_enabled = True
                                        st.session_state.keywords = {}
                                        
                                        transcription_id = db_utils.save_transcription(
                                            recording_filename=selected_audio,
                                            content=transcription.text,
                                            language="es"
                                        )
                                        
                                        st.success("✅ Transcripción completada")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error al transcribir: {e}")
                        
                        with col_del:
                            if st.button("🗑️", help="Eliminar audio", use_container_width=True, type="secondary"):
                                st.session_state.delete_confirmation[selected_audio] = True
                        
                        # Confirmación de eliminación
                        if st.session_state.delete_confirmation.get(selected_audio):
                            st.warning(f"⚠️ ¿Eliminar '{selected_audio}'?")
                            col_yes, col_no = st.columns(2)
                            with col_yes:
                                if st.button("✅ Sí, eliminar", key=f"confirm_yes_{selected_audio}", use_container_width=True):
                                    if delete_audio(selected_audio, recorder, db_utils):
                                        delete_recording_local(selected_audio)
                                        st.session_state.chat_enabled = False
                                        st.session_state.loaded_audio = None
                                        st.session_state.selected_audio = None
                                        st.session_state.delete_confirmation.pop(selected_audio, None)
                                        st.success("✅ Audio eliminado")
                                        st.rerun()
                            with col_no:
                                if st.button("❌ Cancelar", key=f"confirm_no_{selected_audio}", use_container_width=True):
                                    st.session_state.delete_confirmation.pop(selected_audio, None)
                                    st.rerun()
            
            with tab2:
                st.markdown("### Eliminación Masiva")
                st.warning("⚠️ Esta acción eliminará permanentemente los audios seleccionados")
                
                # Lista con checkboxes
                audios_to_delete = []
                for audio in filtered_recordings:
                    if st.checkbox(format_recording_name(audio), key=f"cb_{audio}"):
                        audios_to_delete.append(audio)
                
                if audios_to_delete:
                    st.error(f"**Se eliminarán {len(audios_to_delete)} audio(s):**")
                    for audio in audios_to_delete:
                        st.write(f"• {audio}")
                    
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("🗑️ Eliminar Seleccionados", type="primary", use_container_width=True):
                            with st.spinner(f"Eliminando {len(audios_to_delete)} audio(s)..."):
                                deleted_count = 0
                                for audio in audios_to_delete:
                                    if delete_audio(audio, recorder, db_utils):
                                        delete_recording_local(audio)
                                        deleted_count += 1
                                
                                st.session_state.chat_enabled = False
                                st.session_state.selected_audio = None
                                
                                if deleted_count > 0:
                                    st.success(f"✅ {deleted_count} audio(s) eliminado(s)")
                                    st.rerun()
                    
                    with col_cancel:
                        if st.button("❌ Cancelar", use_container_width=True):
                            st.rerun()
                else:
                    st.info("Selecciona al menos un audio para eliminar")
        
        else:
            st.warning("No se encontraron audios con los criterios seleccionados")
    
    else:
        st.info("📭 No hay audios guardados. Sube un archivo o graba uno nuevo.")

# ============================================================================
# SECCIÓN 3: TRANSCRIPCIÓN
# ============================================================================

elif sections[selected_section] == "transcription":
    if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
        st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">📝 Transcripción</h2>', unsafe_allow_html=True)
        
        st.markdown(f"**Archivo:** `{st.session_state.get('selected_audio', 'Ninguno seleccionado')}`")
        
        # Mostrar transcripción en un contenedor elegante
        with st.container(border=True, height=400):
            st.markdown("### Texto Transcrito")
            st.text_area(
                "",
                st.session_state.contexto,
                height=350,
                disabled=True,
                label_visibility="collapsed"
            )
        
        # Estadísticas de la transcripción
        col_words, col_chars, col_lines = st.columns(3)
        
        with col_words:
            word_count = len(st.session_state.contexto.split())
            st.metric("Palabras", word_count)
        
        with col_chars:
            char_count = len(st.session_state.contexto)
            st.metric("Caracteres", char_count)
        
        with col_lines:
            line_count = st.session_state.contexto.count('\n') + 1
            st.metric("Líneas", line_count)
    
    else:
        st.warning("⚠️ Primero selecciona y transcribe un audio en la sección 'Audios Guardados'")

# ============================================================================
# SECCIÓN 4: PALABRAS CLAVE
# ============================================================================

elif sections[selected_section] == "keywords":
    if st.session_state.get("chat_enabled", False):
        st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">🏷️ Palabras Clave</h2>', unsafe_allow_html=True)
        
        st.caption("Añade palabras clave para identificar oportunidades en la transcripción")
        
        # Formulario para añadir palabras clave
        with st.form("add_keyword_form"):
            col_kw1, col_kw2 = st.columns([3, 1])
            with col_kw1:
                new_keyword = st.text_input("Nueva palabra clave:", placeholder="Ej: presupuesto, proyecto, cliente...")
            with col_kw2:
                submitted = st.form_submit_button("➕ Añadir", use_container_width=True)
            
            if submitted:
                if new_keyword:
                    cleaned_keyword = new_keyword.strip().lower()
                    
                    if not cleaned_keyword:
                        st.error("❌ La palabra clave no puede estar vacía")
                    elif cleaned_keyword in st.session_state.get("keywords", {}):
                        st.warning(f"⚠️ '{cleaned_keyword}' ya existe")
                    else:
                        if "keywords" not in st.session_state:
                            st.session_state.keywords = {}
                        st.session_state.keywords[cleaned_keyword] = cleaned_keyword
                        st.success(f"✅ '{cleaned_keyword}' añadida")
                        st.rerun()
                else:
                    st.error("❌ Ingresa una palabra clave")
        
        # Mostrar palabras clave existentes
        keywords_dict = st.session_state.get("keywords", {})
        
        if keywords_dict:
            st.markdown("### Palabras Clave Configuradas")
            
            # Mostrar como badges
            cols = st.columns(4)
            keywords_list = list(keywords_dict.keys())
            
            for idx, keyword in enumerate(keywords_list):
                with cols[idx % 4]:
                    with st.container(border=True):
                        st.markdown(f"**{keyword}**")
                        if st.button("❌", key=f"del_{keyword}", help="Eliminar", use_container_width=True):
                            delete_keyword_local(keyword)
                            st.rerun()
            
            # Botón para generar oportunidades
            st.markdown("---")
            if st.button("🔍 Buscar Oportunidades", type="primary", use_container_width=True):
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
                        st.success(f"✅ {saved_count} oportunidad(es) encontrada(s)")
                        st.session_state.show_opportunities = True
                        st.rerun()
                    else:
                        st.warning("⚠️ No se encontraron oportunidades con las palabras clave")
        
        else:
            st.info("📝 No hay palabras clave configuradas. Añade algunas para buscar oportunidades.")
    
    else:
        st.warning("⚠️ Primero carga y transcribe un audio")

# ============================================================================
# SECCIÓN 5: OPORTUNIDADES
# ============================================================================

elif sections[selected_section] == "opportunities":
    if st.session_state.get("chat_enabled", False):
        selected_audio = st.session_state.get("selected_audio", "")
        opportunities = opp_manager.load_opportunities(selected_audio)
        
        if opportunities:
            st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">🎯 Oportunidades de Negocio</h2>', unsafe_allow_html=True)
            
            # Filtros para oportunidades
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                status_filter = st.selectbox(
                    "Filtrar por estado:",
                    ["Todos", "Nuevo", "En progreso", "Cerrado", "Ganado"]
                )
            
            with col_filter2:
                priority_filter = st.selectbox(
                    "Filtrar por prioridad:",
                    ["Todas", "Alta", "Media", "Baja"]
                )
            
            with col_filter3:
                keyword_filter = st.selectbox(
                    "Filtrar por palabra clave:",
                    ["Todas"] + sorted(list(set([opp['keyword'] for opp in opportunities])))
                )
            
            # Aplicar filtros
            filtered_opps = opportunities
            
            if status_filter != "Todos":
                status_map = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
                filtered_opps = [opp for opp in filtered_opps if opp.get('status') == status_map[status_filter]]
            
            if priority_filter != "Todas":
                priority_map = {"Alta": "High", "Media": "Medium", "Baja": "Low"}
                filtered_opps = [opp for opp in filtered_opps if opp.get('priority') == priority_map[priority_filter]]
            
            if keyword_filter != "Todas":
                filtered_opps = [opp for opp in filtered_opps if opp['keyword'] == keyword_filter]
            
            st.info(f"📊 Mostrando {len(filtered_opps)} de {len(opportunities)} oportunidades")
            
            # Mostrar oportunidades
            for idx, opp in enumerate(filtered_opps):
                occurrence_text = f" (#{opp.get('occurrence', 1)})" if opp.get('occurrence', 1) > 1 else ""
                
                with st.expander(f"**{opp['keyword']}**{occurrence_text} - {opp['created_at']}", expanded=False):
                    col_opp1, col_opp2 = st.columns([2, 1])
                    
                    with col_opp1:
                        st.markdown("**Contexto encontrado:**")
                        st.info(opp['full_context'])
                        
                        st.markdown("**Notas:**")
                        new_notes = st.text_area(
                            "",
                            value=opp.get('notes', ''),
                            placeholder="Añade notas sobre esta oportunidad...",
                            height=100,
                            key=f"notes_{idx}",
                            label_visibility="collapsed"
                        )
                    
                    with col_opp2:
                        # Estado
                        status_options = {"Nuevo": "new", "En progreso": "in_progress", "Cerrado": "closed", "Ganado": "won"}
                        status_display_names = list(status_options.keys())
                        current_status = opp.get('status', 'new')
                        current_status_label = [k for k, v in status_options.items() if v == current_status][0]
                        
                        st.markdown("**Estado:**")
                        selected_status_label = st.selectbox(
                            "",
                            status_display_names,
                            index=status_display_names.index(current_status_label),
                            key=f"status_{idx}",
                            label_visibility="collapsed"
                        )
                        new_status = status_options[selected_status_label]
                        
                        # Prioridad
                        priority_options = {"Alta": "High", "Media": "Medium", "Baja": "Low"}
                        priority_display_names = list(priority_options.keys())
                        current_priority = opp.get('priority', 'Medium')
                        current_priority_label = [k for k, v in priority_options.items() if v == current_priority][0]
                        
                        st.markdown("**Prioridad:**")
                        selected_priority_label = st.selectbox(
                            "",
                            priority_display_names,
                            index=priority_display_names.index(current_priority_label),
                            key=f"priority_{idx}",
                            label_visibility="collapsed"
                        )
                        new_priority = priority_options[selected_priority_label]
                    
                    # Botones de acción
                    col_save, col_delete = st.columns(2)
                    with col_save:
                        if st.button("💾 Guardar", key=f"save_{idx}", use_container_width=True):
                            updates = {
                                "notes": new_notes,
                                "status": new_status,
                                "priority": new_priority
                            }
                            if opp_manager.update_opportunity(opp['id'], updates):
                                update_opportunity_local(idx, updates)
                                st.success("✅ Cambios guardados")
                                st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️ Eliminar", key=f"delete_{idx}", use_container_width=True, type="secondary"):
                            st.session_state.opp_delete_confirmation[idx] = True
                        
                        if st.session_state.opp_delete_confirmation.get(idx):
                            st.warning("⚠️ ¿Eliminar esta oportunidad?")
                            col_yes, col_no = st.columns(2)
                            with col_yes:
                                if st.button("✅ Sí", key=f"opp_confirm_yes_{idx}", use_container_width=True):
                                    if opp_manager.delete_opportunity(opp['id']):
                                        delete_opportunity_local(idx)
                                        st.session_state.opp_delete_confirmation.pop(idx, None)
                                        st.success("✅ Oportunidad eliminada")
                                        st.rerun()
                            with col_no:
                                if st.button("❌ No", key=f"opp_confirm_no_{idx}", use_container_width=True):
                                    st.session_state.opp_delete_confirmation.pop(idx, None)
                                    st.rerun()
            
            # Exportar oportunidades
            st.markdown("---")
            if st.button("📥 Exportar Oportunidades", use_container_width=True):
                st.info("Función de exportación en desarrollo...")
        
        else:
            st.info("📭 No hay oportunidades generadas. Ve a la sección 'Palabras Clave' para buscarlas.")
    
    else:
        st.warning("⚠️ Primero carga un audio y busca oportunidades")

# ============================================================================
# SECCIÓN 6: CHAT IA
# ============================================================================

elif sections[selected_section] == "chat":
    if st.session_state.get("chat_enabled", False):
        st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">💬 Asistente IA</h2>', unsafe_allow_html=True)
        
        st.markdown(f"**Conversando sobre:** `{st.session_state.get('selected_audio', 'audio')}`")
        
        # Info sobre palabras clave activas
        if st.session_state.get("keywords"):
            keywords_list = list(st.session_state.get("keywords", {}).keys())
            if keywords_list:
                st.info(f"🔑 **Palabras clave activas:** {', '.join(keywords_list)}")
        
        # Inicializar historial de chat
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            st.session_state.chat_history.append("🤖 **IA**: ¡Hola! Soy tu asistente de análisis de reuniones. Puedo ayudarte a analizar la transcripción, identificar puntos importantes, resumir contenido, o responder preguntas específicas sobre lo discutido. ¿En qué te puedo ayudar?")
        
        # Mostrar historial de chat
        chat_container = st.container(height=400, border=True)
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message.startswith("👤"):
                    user_text = message.replace("👤 **Usuario**: ", "")
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%); color: white; padding: 10px 15px; border-radius: 15px 15px 0 15px; margin: 10px 0 10px auto; max-width: 80%;">
                        {user_text}
                    </div>
                    """, unsafe_allow_html=True)
                elif message.startswith("🤖"):
                    ai_text = message.replace("🤖 **IA**: ", "")
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; color: #333; padding: 10px 15px; border-radius: 15px 15px 15px 0; margin: 10px auto 10px 0; max-width: 80%; border: 1px solid #ddd;">
                        {ai_text}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Campo de entrada
        user_input = st.chat_input("Escribe tu pregunta o solicitud de análisis...")
        
        if user_input:
            st.session_state.chat_history.append(f"👤 **Usuario**: {user_input}")
            
            with st.spinner("🤖 Pensando..."):
                try:
                    keywords = st.session_state.get("keywords", {})
                    response = chat_model.call_model(user_input, st.session_state.contexto, keywords)
                    st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                    
                    # Limitar historial
                    max_history = st.session_state.chat_history_limit
                    if len(st.session_state.chat_history) > max_history:
                        st.session_state.chat_history = st.session_state.chat_history[-max_history:]
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        # Botones de acción rápida
        st.markdown("**Acciones rápidas:**")
        col_q1, col_q2, col_q3 = st.columns(3)
        
        with col_q1:
            if st.button("📋 Resumir reunión", use_container_width=True):
                st.session_state.chat_history.append("👤 **Usuario**: Haz un resumen ejecutivo de esta reunión")
                with st.spinner("Generando resumen..."):
                    try:
                        keywords = st.session_state.get("keywords", {})
                        response = chat_model.call_model(
                            "Haz un resumen ejecutivo de esta reunión", 
                            st.session_state.contexto, 
                            keywords
                        )
                        st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with col_q2:
            if st.button("🎯 Puntos clave", use_container_width=True):
                st.session_state.chat_history.append("👤 **Usuario**: Identifica los puntos clave discutidos en la reunión")
                with st.spinner("Identificando puntos clave..."):
                    try:
                        keywords = st.session_state.get("keywords", {})
                        response = chat_model.call_model(
                            "Identifica los puntos clave discutidos en la reunión", 
                            st.session_state.contexto, 
                            keywords
                        )
                        st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with col_q3:
            if st.button("🔍 Buscar decisiones", use_container_width=True):
                st.session_state.chat_history.append("👤 **Usuario**: ¿Qué decisiones se tomaron en esta reunión?")
                with st.spinner("Buscando decisiones..."):
                    try:
                        keywords = st.session_state.get("keywords", {})
                        response = chat_model.call_model(
                            "¿Qué decisiones se tomaron en esta reunión?", 
                            st.session_state.contexto, 
                            keywords
                        )
                        st.session_state.chat_history.append(f"🤖 **IA**: {response}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    else:
        st.warning("⚠️ Primero carga y transcribe un audio para habilitar el chat")

# ============================================================================
# SECCIÓN 7: DEBUG
# ============================================================================

elif sections[selected_section] == "debug":
    st.markdown('<h2 style="border-bottom: 2px solid #3B82F6; padding-bottom: 10px;">🔍 Panel de Diagnóstico</h2>', unsafe_allow_html=True)
    
    # Tabs para diferentes diagnósticos
    tab1, tab2, tab3 = st.tabs(["📊 Estado del Sistema", "📋 Registro de Eventos", "⚙️ Configuración"])
    
    with tab1:
        st.markdown("### Conexión a Base de Datos")
        
        try:
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
                
                # Mostrar métricas
                col_db1, col_db2, col_db3 = st.columns(3)
                
                with col_db1:
                    st.metric("Grabaciones", record_count, delta=None)
                
                with col_db2:
                    st.metric("Oportunidades", opp_count, delta=None)
                
                with col_db3:
                    st.metric("Transcripciones", trans_count, delta=None)
                
                st.success("✅ Conexión a Supabase establecida correctamente")
                
                # Estado de las tablas
                st.markdown("### Estado de las Tablas")
                
                tables_status = {
                    "recordings": "✅ Activa" if record_count >= 0 else "❌ Error",
                    "opportunities": "✅ Activa" if opp_count >= 0 else "❌ Error",
                    "transcriptions": "✅ Activa" if trans_count >= 0 else "❌ Error"
                }
                
                for table, status in tables_status.items():
                    st.write(f"- **{table}**: {status}")
                
            else:
                st.error("❌ No se pudo inicializar Supabase")
                st.info("**Posibles causas:**")
                st.write("1. Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")
                st.write("2. Problemas de conexión a internet")
                st.write("3. Credenciales incorrectas")
                
        except Exception as e:
            st.error(f"❌ Error de conexión: {str(e)}")
        
        # Estado de sesión
        st.markdown("### Estado de la Sesión")
        
        session_keys = [
            "selected_audio", "chat_enabled", "keywords", 
            "recordings", "contexto"
        ]
        
        for key in session_keys:
            value = st.session_state.get(key, "No definido")
            if isinstance(value, dict):
                value = f"Dict con {len(value)} elementos"
            elif isinstance(value, list):
                value = f"Lista con {len(value)} elementos"
            st.write(f"- **{key}**: `{value}`")
    
    with tab2:
        st.markdown("### Registro de Eventos")
        
        debug_log = st.session_state.get("debug_log", [])
        
        if debug_log:
            # Filtros para eventos
            col_filter_type, col_filter_limit = st.columns(2)
            
            with col_filter_type:
                event_type_filter = st.selectbox(
                    "Tipo de evento:",
                    ["Todos", "success", "error", "info"]
                )
            
            with col_filter_limit:
                event_limit = st.slider("Mostrar últimos eventos:", 5, 50, 20)
            
            # Filtrar eventos
            filtered_events = debug_log
            
            if event_type_filter != "Todos":
                filtered_events = [e for e in filtered_events if e.get("type") == event_type_filter]
            
            filtered_events = filtered_events[-event_limit:]
            
            # Mostrar eventos
            for event in reversed(filtered_events):
                time = event.get("time", "??:??:??")
                event_type = event.get("type", "info")
                message = event.get("message", "")
                
                if event_type == "success":
                    st.success(f"[{time}] {message}")
                elif event_type == "error":
                    st.error(f"[{time}] {message}")
                else:
                    st.info(f"[{time}] {message}")
            
            # Botón para limpiar registro
            if st.button("🧹 Limpiar Registro", use_container_width=True):
                st.session_state.debug_log = []
                st.rerun()
        
        else:
            st.info("📭 No hay eventos registrados aún")
    
    with tab3:
        st.markdown("### Configuración de la Aplicación")
        
        st.markdown("**Límites y configuraciones:**")
        
        # Ajustar límite de historial de chat
        new_limit = st.slider(
            "Límite de mensajes en el chat:",
            min_value=5,
            max_value=100,
            value=st.session_state.chat_history_limit,
            step=5
        )
        
        if new_limit != st.session_state.chat_history_limit:
            st.session_state.chat_history_limit = new_limit
            st.success(f"✅ Límite actualizado a {new_limit} mensajes")
        
        # Información del sistema
        st.markdown("**Información del sistema:**")
        
        import platform
        import streamlit as st
        
        sys_info = {
            "Sistema Operativo": platform.system(),
            "Versión Python": platform.python_version(),
            "Streamlit": st.__version__,
            "APP_NAME": APP_NAME
        }
        
        for key, value in sys_info.items():
            st.write(f"- **{key}**: `{value}`")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "🎙️ Transcripción Inteligente v1.0 · Análisis de Oportunidades en Reuniones · "
    "© 2024 Todos los derechos reservados"
    "</div>",
    unsafe_allow_html=True
)