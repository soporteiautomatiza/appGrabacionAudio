"""
Componentes reutilizables para la interfaz - Diseño Glassmorphism
"""
import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional


def render_glass_card(content: str, key: Optional[str] = None, hover: bool = False) -> None:
    """
    Renderiza una tarjeta con efecto glassmorphism
    
    Args:
        content: Contenido HTML a mostrar dentro de la tarjeta
        key: Identificador único para el componente
        hover: Si True, agrega efecto hover
    """
    hover_class = "glass-card-hover" if hover else ""
    st.markdown(f'''
    <div class="glass-card {hover_class}">
        {content}
    </div>
    ''', unsafe_allow_html=True)


def render_gradient_button(text: str, icon: str = "", gradient_type: str = "primary") -> str:
    """
    Renderiza HTML para un botón con gradiente
    
    Args:
        text: Texto del botón
        icon: Emoji o icono a mostrar
        gradient_type: Tipo de gradiente (primary, secondary, destructive)
    
    Returns:
        HTML del botón
    """
    gradient_class = f"gradient-{gradient_type}"
    return f'''
    <button class="btn {gradient_class}">
        {icon} {text}
    </button>
    '''


def render_badge(text: str, badge_type: str = "default") -> str:
    """
    Renderiza un badge con estilo
    
    Args:
        text: Texto del badge
        badge_type: Tipo de badge (recording, upload, saved, transcribed,
                   priority-high, priority-medium, priority-low,
                   status-open, status-progress, status-closed)
    
    Returns:
        HTML del badge
    """
    return f'<span class="badge badge-{badge_type}">{text}</span>'


def render_opportunity_card(opportunity: Dict[str, Any]) -> None:
    """
    Renderiza una tarjeta de oportunidad con el diseño completo
    
    Args:
        opportunity: Diccionario con los datos de la oportunidad
                    Debe contener: id, ticket_number, title, description,
                    priority, status, created_at
    """
    # Determinar clase de prioridad
    priority_class = ""
    if opportunity.get("priority", "").lower() == "high":
        priority_class = "opportunity-card-high-priority"
    
    # Badges de prioridad y estado
    priority_badge = render_badge(opportunity.get("priority", "Medium"), 
                                 f"priority-{opportunity.get('priority', 'medium').lower()}")
    status_badge = render_badge(opportunity.get("status", "Open"), 
                               f"status-{opportunity.get('status', 'open').lower().replace(' ', '')}")
    
    # Formatear fecha
    created_date = opportunity.get("created_at", "")
    if isinstance(created_date, str):
        try:
            date_obj = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%d %b %Y")
        except:
            formatted_date = created_date
    else:
        formatted_date = str(created_date)
    
    # Renderizar tarjeta
    st.markdown(f'''
    <div class="opportunity-card {priority_class}">
        <div class="opportunity-header">
            <span class="ticket-number">#{opportunity.get("ticket_number", "")}</span>
            {priority_badge}
        </div>
        
        <div class="opportunity-title">{opportunity.get("title", "Sin título")}</div>
        
        <div class="opportunity-description">{opportunity.get("description", "Sin descripción")}</div>
        
        <div class="opportunity-footer">
            <div>{status_badge}</div>
            <div style="font-size: 12px; color: var(--muted-foreground);">{formatted_date}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_recording_item(recording: Dict[str, Any], on_play=None, on_transcribe=None, on_delete=None) -> None:
    """
    Renderiza un item de grabación en la lista
    
    Args:
        recording: Diccionario con datos de la grabación (filename, duration, created_at, has_transcription)
        on_play: Callback para reproducir
        on_transcribe: Callback para transcribir
        on_delete: Callback para eliminar
    """
    filename = recording.get("filename", "audio.wav")
    duration = recording.get("duration", "00:00")
    has_transcription = recording.get("has_transcription", False)
    created_at = recording.get("created_at", "")
    
    # Badge de transcrito
    transcribed_badge = render_badge("✓ Transcrito", "transcribed") if has_transcription else ""
    
    # Formatear fecha
    try:
        if isinstance(created_at, str):
            date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")
        else:
            formatted_date = str(created_at)
    except:
        formatted_date = created_at
    
    # Crear columnas para el item
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f'''
        <div style="padding: 8px 0;">
            <div style="font-weight: 600; margin-bottom: 4px;">{filename} {transcribed_badge}</div>
            <div style="font-size: 12px; color: var(--muted-foreground);">
                {duration} • {formatted_date}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        if on_play and st.button("▶️", key=f"play_{filename}", help="Reproducir"):
            on_play(recording)
    
    with col3:
        if on_transcribe and not has_transcription:
            if st.button("📝", key=f"transcribe_{filename}", help="Transcribir"):
                on_transcribe(recording)
    
    with col4:
        if on_delete and st.button("🗑️", key=f"delete_{filename}", help="Eliminar"):
            on_delete(recording)


def render_header() -> None:
    """Renderiza el header personalizado de la aplicación"""
    st.markdown('''
    <div class="glass-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo-icon">✨</div>
                <div>
                    <h1 style="margin: 0; font-size: 20px; font-weight: 700;">AI Meeting Intelligence</h1>
                    <p class="subtitle">Transform conversations into opportunities</p>
                </div>
            </div>
            <div class="header-actions">
                <button class="icon-btn" title="Settings">⚙️</button>
                <button class="icon-btn" title="User">👤</button>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_background_effects() -> None:
    """Renderiza los efectos de fondo animados (orbes)"""
    st.markdown('''
    <div class="background-effects">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
    </div>
    ''', unsafe_allow_html=True)


def render_section_title(title: str, icon: str = "", count: Optional[int] = None) -> None:
    """
    Renderiza un título de sección con estilo
    
    Args:
        title: Título de la sección
        icon: Emoji o icono
        count: Número a mostrar (opcional)
    """
    count_text = f'<span style="color: var(--muted-foreground); font-weight: normal;"> ({count})</span>' if count is not None else ""
    st.markdown(f'''
    <h3 style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
        <span style="font-size: 20px;">{icon}</span>
        {title}{count_text}
    </h3>
    ''', unsafe_allow_html=True)


def render_priority_indicator(priority: str) -> str:
    """
    Retorna el emoji y color para un nivel de prioridad
    
    Args:
        priority: Nivel de prioridad (High, Medium, Low)
    
    Returns:
        Tuple de (emoji, color)
    """
    indicators = {
        "high": ("🔴", "var(--error-red)"),
        "medium": ("🟡", "var(--warning-orange)"),
        "low": ("🟢", "var(--success-green)")
    }
    return indicators.get(priority.lower(), ("⚪", "var(--muted-foreground)"))


def render_status_pill(status: str) -> str:
    """
    Renderiza una píldora de estado con icono
    
    Args:
        status: Estado (Open, In Progress, Closed)
    
    Returns:
        HTML del pill
    """
    status_icons = {
        "open": "🕐",
        "in progress": "📊",
        "closed": "✓"
    }
    icon = status_icons.get(status.lower(), "•")
    return f'''
    <span class="badge badge-status badge-status-{status.lower().replace(' ', '')}">
        {icon} {status}
    </span>
    '''


def render_search_box(placeholder: str = "Buscar...", key: str = "search") -> str:
    """
    Renderiza un cuadro de búsqueda con estilo
    
    Args:
        placeholder: Texto del placeholder
        key: Key único para el input
    
    Returns:
        Valor del input de búsqueda
    """
    search_value = st.text_input(
        "🔍",
        placeholder=placeholder,
        key=key,
        label_visibility="collapsed"
    )
    return search_value


def render_empty_state(icon: str, message: str) -> None:
    """
    Renderiza un estado vacío con icono y mensaje
    
    Args:
        icon: Emoji o icono grande
        message: Mensaje a mostrar
    """
    st.markdown(f'''
    <div style="text-align: center; padding: 60px 20px; color: var(--muted-foreground);">
        <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.3;">{icon}</div>
        <p style="font-size: 14px;">{message}</p>
    </div>
    ''', unsafe_allow_html=True)


def render_colorful_transcription(transcription: str) -> None:
    """
    Renderiza la transcripción con colores diferentes para cada persona.
    Con expansión/colapso: muestra primeras 5 líneas por defecto.
    
    Formato esperado:
    Nombre: "texto..."
    Otro Nombre: "más texto..."
    
    Args:
        transcription: Texto completo de la transcripción
    """
    # Paleta de colores vibrantes y contrastantes para fondo oscuro
    colors = [
        "#FF6B6B",  # Rojo coral
        "#4ECDC4",  # Turquesa
        "#45B7D1",  # Azul cielo
        "#FFA07A",  # Salmón claro
        "#98D8C8",  # Verde menta
        "#F7DC6F",  # Amarillo dorado
        "#BB8FCE",  # Púrpura
        "#85C1E2",  # Azul claro
        "#F8B88B",  # Naranja claro
        "#A8D8EA",  # Azul pastel
        "#FF9FF3",  # Rosa
        "#54A0FF",  # Azul brillante
    ]
    
    # Diccionario para mapear personas a colores
    speaker_colors = {}
    color_index = 0
    
    # Parsear líneas y extraer nombres de personas
    lines = transcription.split('\n')
    html_parts = []
    
    for line in lines:
        if ':' in line:
            # Separar nombre del contenido
            parts = line.split(':', 1)
            if len(parts) == 2:
                speaker = parts[0].strip()
                text = parts[1].strip()
                
                # Si es un nuevo hablante, asignarle color
                if speaker not in speaker_colors:
                    speaker_colors[speaker] = colors[color_index % len(colors)]
                    color_index += 1
                
                color = speaker_colors[speaker]
                
                # Escapar caracteres especiales en el texto
                text_safe = text.replace('<', '&lt;').replace('>', '&gt;')
                
                # Crear línea HTML sin saltos de línea
                html_line = f'<div style="margin-bottom:12px;padding:12px;background:rgba(255,255,255,0.05);border-left:4px solid {color};border-radius:4px;"><span style="color:{color};font-weight:700;font-size:14px;">{speaker}:</span><span style="color:rgba(255,255,255,0.9);margin-left:8px;">{text_safe}</span></div>'
                html_parts.append(html_line)
            else:
                # Si no hay ":", simplemente mostrar la línea
                if line.strip():
                    line_safe = line.replace('<', '&lt;').replace('>', '&gt;')
                    html_parts.append(f'<div style="color:rgba(255,255,255,0.7);margin-bottom:8px;">{line_safe}</div>')
        else:
            # Líneas sin ":" (líneas en blanco o texto sin speaker)
            if line.strip():
                line_safe = line.replace('<', '&lt;').replace('>', '&gt;')
                html_parts.append(f'<div style="color:rgba(255,255,255,0.7);margin-bottom:8px;">{line_safe}</div>')
    
    # Determinar si hay que mostrar expansión
    total_lines = len(html_parts)
    max_initial_lines = 5
    needs_expansion = total_lines > max_initial_lines
    
    # Inicializar estado de expansión en session_state
    if 'transcript_expanded' not in st.session_state:
        st.session_state.transcript_expanded = False
    
    # Mostrar primeras líneas siempre
    html_content = '<div style="font-family:\'Segoe UI\',Tahoma,Geneva,Verdana,sans-serif;line-height:1.8;padding:20px;background:rgba(20,30,50,0.5);border-radius:12px;border:1px solid rgba(255,255,255,0.1);">'
    
    if needs_expansion and not st.session_state.transcript_expanded:
        # Mostrar solo primeras 5 líneas
        html_content += ''.join(html_parts[:max_initial_lines])
        html_content += '</div>'
        st.markdown(html_content, unsafe_allow_html=True)
        
        # Botón para expandir
        if st.button(f"📖 Mostrar más ({total_lines - max_initial_lines} líneas restantes)", use_container_width=True):
            st.session_state.transcript_expanded = True
            st.rerun()
    else:
        # Mostrar todo
        html_content += ''.join(html_parts)
        html_content += '</div>'
        st.markdown(html_content, unsafe_allow_html=True)
        
        # Botón para colapsar si está expandido
        if needs_expansion:
            if st.button("📖 Mostrar menos", use_container_width=True):
                st.session_state.transcript_expanded = False
                st.rerun()
