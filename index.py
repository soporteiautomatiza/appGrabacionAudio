import streamlit as st
import os
import AudioRecorder
import Transcriber
import Model
import OpportunitiesManager

# Configuración inicial de la interfaz de usuario
st.set_page_config(layout="wide", page_title="AudioToTextoIA")

# Inicializar objetos
recorder = AudioRecorder.AudioRecorder()
transcriber_model = Transcriber.Transcriber()
chat_model = Model.Model()
opp_manager = OpportunitiesManager.OpportunitiesManager()

st.title("🎙️ AudioToTextoIA")

# Crear dos columnas principales para la carga
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Carga tu audio")
    
    # Opción de subir archivo
    st.subheader("Sube un archivo de audio")
    uploaded_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3", "wav", "m4a", "ogg", "flac", "webm"])
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        filename = uploaded_file.name
        filepath = recorder.save_recording(audio_bytes, filename)
        st.success(f"✅ Archivo guardado: {filename}")
        st.session_state.update_list = True
        st.rerun()

with col2:
    st.header("📂 Audios Guardados")
    
    # Forzar actualización de la lista
    if st.session_state.get("update_list", False):
        st.session_state.update_list = False
    
    recordings = recorder.get_recordings_list()
    
    if recordings:
        st.success(f"📊 Total: {len(recordings)} audio(s)")
        
        # Tabs para diferentes vistas
        tab1, tab2 = st.tabs(["📝 Transcribir", "🗑️ Gestión en lote"])
        
        with tab1:
            selected_audio = st.selectbox(
                "Selecciona un audio para transcribir",
                recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
            )
            
            if selected_audio:
                col_play, col_transcribe, col_delete = st.columns([1, 1, 1])
                
                with col_play:
                    if st.button("▶️ Reproducir"):
                        audio_path = recorder.get_recording_path(selected_audio)
                        extension = selected_audio.split('.')[-1]
                        with open(audio_path, "rb") as f:
                            st.audio(f.read(), format=f"audio/{extension}")
                
                with col_transcribe:
                    if st.button("🎯 Transcribir"):
                        with st.spinner("Transcribiendo..."):
                            try:
                                audio_path = recorder.get_recording_path(selected_audio)
                                transcription = transcriber_model.transcript_audio(audio_path)
                                st.session_state.contexto = transcription.text
                                st.session_state.selected_audio = selected_audio
                                st.session_state.chat_enabled = True
                                st.session_state.keywords = {}
                                st.success("✅ Transcripción completada")
                            except Exception as e:
                                st.error(f"Error al transcribir: {e}")
                
                with col_delete:
                    if st.button("🗑️ Eliminar"):
                        recorder.delete_recording(selected_audio)
                        st.session_state.chat_enabled = False
                        st.rerun()
        
        with tab2:
            st.subheader("🗑️ Eliminar múltiples audios")
            st.write("Selecciona uno o varios audios para eliminarlos rápidamente")
            
            audios_to_delete = st.multiselect(
                "Audios a eliminar:",
                recordings,
                format_func=lambda x: x.replace("_", " ").replace(".wav", "").replace(".mp3", "").replace(".m4a", "").replace(".webm", "").replace(".ogg", "").replace(".flac", "")
            )
            
            if audios_to_delete:
                st.warning(f"⚠️ Vas a eliminar {len(audios_to_delete)} audio(s)")
                
                st.write("**Audios seleccionados:**")
                for audio in audios_to_delete:
                    st.write(f"  • {audio}")
                
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("🔥 Eliminar seleccionados", type="primary", use_container_width=True):
                        deleted_count = 0
                        for audio in audios_to_delete:
                            try:
                                recorder.delete_recording(audio)
                                deleted_count += 1
                            except Exception as e:
                                st.error(f"Error al eliminar {audio}: {e}")
                        
                        st.success(f"✅ {deleted_count} audio(s) eliminado(s)")
                        st.session_state.chat_enabled = False
                        st.rerun()
                
                with col_cancel:
                    st.write("")
    else:
        st.info("📭 No hay audios guardados. Sube un archivo.")

# SECCIÓN DE TRANSCRIPCIÓN (Div grande arriba del chat)
st.divider()

if st.session_state.get("chat_enabled", False) and st.session_state.get("contexto"):
    st.header("📋 Transcripción del Audio")
    st.caption(f"De: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar transcripción en un contenedor
    with st.container(border=True):
        st.text_area("", st.session_state.contexto, height=200, disabled=True, label_visibility="collapsed")
    
    # SECCIÓN DE PALABRAS CLAVE
    st.subheader("🏷️ Palabras Clave Contextualizadas")
    st.caption("Añade palabras clave con descripción para que la IA las entienda mejor")
    
    col_kw1, col_kw2, col_kw3 = st.columns([1.5, 1.5, 1])
    with col_kw1:
        new_keyword = st.text_input("Palabra clave:", placeholder="Ej: presupuesto")
    with col_kw2:
        keyword_context = st.text_input("Contexto/Descripción:", placeholder="Ej: total de $5000")
    with col_kw3:
        if st.button("➕ Añadir", use_container_width=True):
            if new_keyword:
                st.session_state.keywords[new_keyword] = keyword_context if keyword_context else "Sin descripción"
                st.success(f"✅ '{new_keyword}' añadida")
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
        st.divider()
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
                    st.success(f"✅ {saved_count} ticket(s) de oportunidad generado(s)")
                    st.session_state.show_opportunities = True
                    st.rerun()
                else:
                    st.warning("⚠️ No se encontraron oportunidades con las palabras clave")

# SECCIÓN DE OPORTUNIDADES
st.divider()

if st.session_state.get("chat_enabled", False):
    selected_audio = st.session_state.get("selected_audio", "")
    opportunities = opp_manager.load_opportunities(selected_audio)
    
    if opportunities:
        st.header("🎟️ Tickets de Oportunidades de Negocio")
        
        for idx, opp in enumerate(opportunities):
            with st.expander(f"📌 {opp['keyword']} - {opp['created_at']}", expanded=False):
                col_opp1, col_opp2 = st.columns([2, 1])
                
                with col_opp1:
                    st.write("**Contexto encontrado en el audio:**")
                    st.info(opp['full_context'])
                    
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
                
                col_save, col_delete = st.columns(2)
                with col_save:
                    if st.button("💾 Guardar cambios", key=f"save_{idx}", use_container_width=True):
                        opp['notes'] = new_notes
                        opp['status'] = new_status
                        opp_manager.update_opportunity(opp, selected_audio)
                        st.success("✅ Cambios guardados")
                
                with col_delete:
                    if st.button("🗑️ Eliminar", key=f"delete_{idx}", use_container_width=True):
                        opp_manager.delete_opportunity(opp['id'], selected_audio)
                        st.success("✅ Oportunidad eliminada")
                        st.rerun()

# SECCIÓN DE CHAT
st.divider()

if st.session_state.get("chat_enabled", False):
    st.header("💬 Chat con IA")
    st.caption(f"Conversando sobre: {st.session_state.get('selected_audio', 'audio')}")
    
    # Mostrar palabras clave activas
    if st.session_state.get("keywords"):
        st.info(f"🏷️ Palabras clave activas: {', '.join(st.session_state.keywords.keys())}")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        st.write(message)
    
    # Campo de entrada
    user_input = st.chat_input("Escribe tu pregunta sobre el audio:")
    
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
                st.error(f"Error al generar respuesta: {e}")
else:
    st.info("👆 Carga un audio y transcríbelo para habilitar el chat.")