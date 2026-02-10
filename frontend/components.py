"""
Componentes reutilizables para la interfaz - Diseño minimalista
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
    """Renderiza una tarjeta de oportunidad con estética minimalista"""
    priority_class = ""
    if opportunity.get("priority", "").lower() == "high":
        priority_class = "opportunity-card-high-priority"

    priority_badge = render_badge(
        opportunity.get("priority", "Medium"),
        f"priority-{opportunity.get('priority', 'medium').lower()}"
    )
    status_badge = render_badge(
        opportunity.get("status", "Open"),
        f"status-{opportunity.get('status', 'open').lower().replace(' ', '')}"
    )

    created_date = opportunity.get("created_at", "")
    if isinstance(created_date, str):
        try:
            date_obj = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%d %b %Y")
        except Exception:
            formatted_date = created_date
    else:
        formatted_date = str(created_date)

    st.markdown(f'''
    <div class="opportunity-card {priority_class}">
        <div class="opportunity-header">
            <div>
                <span class="ticket-number">#{opportunity.get("ticket_number", "")}</span>
                <div class="opportunity-title">{opportunity.get("title", "Sin título")}</div>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end;">
                {priority_badge}
                {status_badge}
            </div>
        </div>
        <div class="opportunity-description">{opportunity.get("description", "Sin descripción")}</div>
        <div class="opportunity-footer">
            <span>Actualizado: {formatted_date}</span>
            <span style="font-weight:600; color: var(--text-primary);">{opportunity.get("owner", "IA Assistant")}</span>
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
    """Renderiza el hero principal con un mensaje claro y profesional"""
    st.markdown('''
    <div class="app-hero">
        <div class="app-hero__content">
            <p class="helper-text" style="text-transform: uppercase; letter-spacing: 0.2em; font-weight: 600; margin-bottom: 8px;">AI Meeting Intelligence</p>
            <h1>Gestiona audios, transcripciones y oportunidades en un solo lugar</h1>
            <p>Sube grabaciones, extrae contexto relevante y convierte cada conversación en acciones comerciales claras.</p>
        </div>
        <div class="app-hero__actions">
            <div class="hero-pill">
                <span>Pipeline de audio</span>
                <strong>Procesamiento continuo</strong>
            </div>
            <div class="hero-pill">
                <span>Insights IA</span>
                <strong>Oportunidades listas</strong>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_background_effects() -> None:
    """Renderiza acentos de fondo suaves para el dashboard"""
    st.markdown('''
    <div class="background-effects">
        <div class="background-accent background-accent--one"></div>
        <div class="background-accent background-accent--two"></div>
    </div>
    ''', unsafe_allow_html=True)


def render_section_title(title: str, icon: str = "", count: Optional[int] = None) -> None:
    """Renderiza un título de sección consistente"""
    icon_html = f'<span class="section-title__icon">{icon}</span>' if icon else ""
    count_html = f'<span class="section-title__count">{count}</span>' if count is not None else ""
    st.markdown(f'''
    <div class="section-title">
        {icon_html}
        <span class="section-title__label">{title}</span>
        {count_html}
    </div>
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
        "high": ("🔴", "var(--error)"),
        "medium": ("🟡", "var(--warning)"),
        "low": ("🟢", "var(--success)")
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
