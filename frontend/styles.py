"""
Estilos CSS minimalistas y profesionales para la aplicación
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap');

    :root {
        --page-bg: #f5f6fb;
        --surface: #ffffff;
        --surface-alt: #f0f2fa;
        --surface-muted: #f8f9ff;
        --border: #e4e7f4;
        --border-strong: #cfd5e6;
        --shadow-soft: 0 20px 45px rgba(15, 23, 42, 0.08);
        --shadow-hover: 0 30px 70px rgba(15, 23, 42, 0.12);
        --text-primary: #0f172a;
        --text-secondary: #475467;
        --text-muted: #8a93a8;
        --muted-foreground: #8a93a8;
        --accent: #2563eb;
        --accent-strong: #1d4ed8;
        --accent-soft: #dce7ff;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --info: #0ea5e9;
    }

    *, *::before, *::after {
        box-sizing: border-box;
    }

    body, [data-testid="stAppViewContainer"] {
        background: var(--page-bg);
        color: var(--text-primary);
        font-family: 'Manrope', 'Space Grotesk', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        letter-spacing: -0.01em;
    }

    .stMainBlockContainer,
    .main {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 32px 32px;
        position: relative;
        z-index: 1;
    }

    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-family: 'Space Grotesk', 'Manrope', sans-serif;
    }

    p, span, label {
        color: var(--text-secondary);
    }

    /* =========================== HERO =========================== */
    .glass-header {
        background: transparent;
        border: none;
        padding: 0;
        margin-bottom: 24px;
    }

    .app-hero {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 28px;
        padding: 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 32px;
        box-shadow: var(--shadow-soft);
        position: relative;
        overflow: hidden;
    }

    .app-hero::after {
        content: "";
        position: absolute;
        right: -40px;
        top: -40px;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle at center, rgba(37, 99, 235, 0.35), transparent 70%);
        z-index: 0;
    }

    .app-hero__content {
        position: relative;
        z-index: 1;
    }

    .app-hero__content h1 {
        font-size: 32px;
        margin-bottom: 12px;
    }

    .app-hero__content p {
        max-width: 520px;
        color: var(--text-secondary);
    }

    .app-hero__actions {
        display: flex;
        gap: 12px;
        position: relative;
        z-index: 1;
    }

    .hero-pill {
        background: var(--surface-muted);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 14px 20px;
        min-width: 160px;
        box-shadow: var(--shadow-soft);
    }

    .hero-pill span {
        display: block;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 4px;
    }

    .hero-pill strong {
        color: var(--accent-strong);
        font-size: 16px;
    }

    /* ======================== SURFACE CARDS ====================== */
    .glass-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 24px;
        box-shadow: var(--shadow-soft);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .glass-card-hover:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-hover);
    }

    /* ====================== SECTION TITLES ======================= */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 18px;
        font-weight: 600;
        margin: 24px 0 4px;
        color: var(--text-primary);
    }

    .section-title__icon {
        width: 36px;
        height: 36px;
        border-radius: 12px;
        background: var(--surface-muted);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: var(--accent-strong);
    }

    .section-title__label {
        font-weight: 600;
        color: var(--text-primary);
    }

    .section-title__count {
        color: var(--text-muted);
        font-size: 14px;
        font-weight: 500;
    }

    .helper-text {
        font-size: 13px;
        color: var(--text-muted);
        margin-bottom: 12px;
    }

    /* ========================== CHIPS =========================== */
    .keyword-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 999px;
        border: 1px solid var(--border-strong);
        background: var(--surface-muted);
        color: var(--text-primary);
        font-weight: 600;
        font-size: 13px;
    }

    .keyword-highlight {
        color: var(--accent-strong);
        font-weight: 600;
    }

    /* ========================= BADGES =========================== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid transparent;
    }

    .badge-recording { background: rgba(239, 68, 68, 0.12); color: #b91c1c; border-color: rgba(239, 68, 68, 0.4); }
    .badge-upload { background: rgba(37, 99, 235, 0.12); color: var(--accent-strong); border-color: rgba(37, 99, 235, 0.35); }
    .badge-saved { background: rgba(16, 185, 129, 0.12); color: var(--success); border-color: rgba(16, 185, 129, 0.35); }
    .badge-transcribed {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success);
        border-color: rgba(16, 185, 129, 0.4);
    }

    .badge-priority-high { background: rgba(239, 68, 68, 0.1); color: var(--error); border-color: rgba(239, 68, 68, 0.4); }
    .badge-priority-medium { background: rgba(245, 158, 11, 0.12); color: var(--warning); border-color: rgba(245, 158, 11, 0.4); }
    .badge-priority-low { background: rgba(16, 185, 129, 0.12); color: var(--success); border-color: rgba(16, 185, 129, 0.35); }

    .badge-status {
        font-size: 12px;
        border-radius: 12px;
        padding: 4px 12px;
    }

    .badge-status-open { background: rgba(37, 99, 235, 0.1); color: var(--accent-strong); }
    .badge-status-progress { background: rgba(14, 165, 233, 0.15); color: var(--info); }
    .badge-status-closed { background: rgba(15, 23, 42, 0.08); color: var(--text-secondary); }

    /* ========================== BUTTONS ========================= */
    .stButton > button {
        border-radius: 14px;
        border: 1px solid var(--border);
        background: var(--surface);
        color: var(--text-primary);
        font-weight: 600;
        padding: 10px 18px;
        box-shadow: var(--shadow-soft);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .stButton > button:hover {
        border-color: var(--accent-soft);
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: #fff;
        border-color: var(--accent-strong);
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.25);
    }

    .stButton > button[kind="secondary"] {
        background: var(--surface-muted);
    }

    button[key*="del_"] {
        border-color: rgba(239, 68, 68, 0.5) !important;
        color: var(--error) !important;
    }

    button[key*="del_"]:hover {
        background: rgba(239, 68, 68, 0.08) !important;
    }

    .btn {
        border: none;
        border-radius: 14px;
        padding: 10px 18px;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .btn:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-soft);
    }

    .gradient-primary {
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: #fff;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.2);
    }

    .gradient-secondary {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(14, 165, 233, 0.15));
        color: var(--accent-strong);
    }

    .gradient-destructive {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.95), rgba(220, 38, 38, 0.9));
        color: #fff;
        box-shadow: 0 12px 30px rgba(239, 68, 68, 0.25);
    }

    /* ========================= INPUTS =========================== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stChatInputContainer textarea {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px !important;
        padding: 12px 16px;
        color: var(--text-primary);
        box-shadow: var(--shadow-soft);
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus-within,
    .stChatInputContainer textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }

    [data-testid="stFileUploader"],
    .stAudioInput {
        background: var(--surface);
        border: 1px dashed var(--border-strong);
        border-radius: 18px;
        padding: 24px;
        transition: border-color 0.2s ease, background 0.2s ease;
    }

    [data-testid="stFileUploader"]:hover,
    .stAudioInput:hover {
        border-color: var(--accent);
        background: var(--surface-muted);
    }

    audio {
        width: 100%;
        border-radius: 18px;
        border: 1px solid var(--border);
        background: var(--surface);
        box-shadow: var(--shadow-soft);
    }

    /* ======================= LIST ELEMENTS ====================== */
    .recording-list-item {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: var(--shadow-soft);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .recording-list-item:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-hover);
    }

    .recording-list-item__title {
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-primary);
    }

    .recording-list-item__subtitle {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 4px;
    }

    .context-panel {
        background: var(--surface-muted);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        line-height: 1.6;
        color: var(--text-secondary);
    }

    /* ==================== OPORTUNIDADES ======================== */
    .opportunity-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 20px 24px;
        box-shadow: var(--shadow-soft);
        margin-bottom: 18px;
    }

    .opportunity-card-high-priority {
        border-color: rgba(239, 68, 68, 0.4);
    }

    .opportunity-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 16px;
    }

    .ticket-number {
        font-family: 'Space Grotesk', monospace;
        font-weight: 600;
        background: var(--surface-muted);
        border-radius: 999px;
        padding: 6px 12px;
        color: var(--accent-strong);
    }

    .opportunity-title {
        font-size: 18px;
        margin: 12px 0 6px;
    }

    .opportunity-description {
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 16px;
    }

    .opportunity-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        color: var(--text-muted);
    }

    /* ========================== CHAT =========================== */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin: 16px 0;
    }

    .chat-message {
        display: flex;
        gap: 12px;
    }

    .chat-bubble {
        max-width: 70%;
        padding: 14px 18px;
        border-radius: 18px;
        line-height: 1.6;
        border: 1px solid transparent;
        box-shadow: var(--shadow-soft);
    }

    .chat-message-user {
        justify-content: flex-end;
    }

    .chat-message-user .chat-bubble {
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: #fff;
        border-color: transparent;
    }

    .chat-message-ai .chat-bubble {
        background: var(--surface);
        border-color: var(--border);
        color: var(--text-secondary);
    }

    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 12px;
        background: var(--surface-muted);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: var(--accent-strong);
    }

    /* =========================== TABS ========================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        padding-bottom: 8px;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 16px;
        border: 1px solid var(--border);
        background: var(--surface-muted);
        color: var(--text-secondary);
        padding: 12px 20px;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--surface);
        color: var(--text-primary);
        border-color: var(--accent-soft);
        box-shadow: var(--shadow-soft);
    }

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ======================= NOTIFICACIONES ===================== */
    .notification-container {
        border-radius: 16px;
        padding: 16px;
        border: 1px solid var(--border);
        background: var(--surface);
        box-shadow: var(--shadow-soft);
    }

    .notification-info { border-left: 4px solid var(--accent); }
    .notification-success { border-left: 4px solid var(--success); }
    .notification-warning { border-left: 4px solid var(--warning); }
    .notification-error { border-left: 4px solid var(--error); }

    /* ===================== BACKGROUND EFFECTS =================== */
    .background-effects {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }

    .background-accent {
        position: absolute;
        width: 480px;
        height: 480px;
        border-radius: 50%;
        filter: blur(120px);
        opacity: 0.35;
        animation: float 18s ease-in-out infinite;
    }

    .background-accent--one {
        top: -120px;
        left: -120px;
        background: #c7d8ff;
    }

    .background-accent--two {
        bottom: -140px;
        right: -80px;
        background: #ffe3d9;
        animation-delay: -6s;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    @media (max-width: 900px) {
        .app-hero {
            flex-direction: column;
            align-items: flex-start;
        }

        .app-hero__actions {
            width: 100%;
            flex-wrap: wrap;
        }

        .hero-pill {
            flex: 1;
        }
    }
    </style>
    """
