"""
Estilos CSS modernos para la aplicación - Diseño Glassmorphism
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
    /* ============================================================
       VARIABLES CSS - Colores del diseño
       ============================================================ */
    :root {
        --deep-charcoal: #1a1d2e;
        --electric-blue: #0ea5e9;
        --cyber-purple: #8b5cf6;
        --foreground: #e4e5f1;
        --muted-foreground: #8b8d98;
        --glass-bg: rgba(42, 45, 62, 0.4);
        --glass-border: rgba(139, 92, 246, 0.2);
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --error-red: #ef4444;
    }
    
    /* ============================================================
       LAYOUT BASE - Fondo oscuro y contenedor
       ============================================================ */
    [data-testid="stAppViewContainer"] {
        background: var(--deep-charcoal);
        color: var(--foreground);
    }
    
    .main {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px 40px;
    }
    
    .stMainBlockContainer {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    [data-testid="stAppViewContainer"] > section {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px;
    }
    
    /* Centrar input de chat */
    [data-testid="stInputBase"] {
        max-width: 100%;
    }
    
    .stChatInputContainer {
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* ============================================================
       ANIMACIONES CSS
       ============================================================ */
    @keyframes pulse-glow {
        0%, 100% { 
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
        }
        50% { 
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.6), 0 0 40px rgba(14, 165, 233, 0.3);
        }
    }
    
    @keyframes glow-high-priority {
        0%, 100% {
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
        }
        50% {
            box-shadow: 0 0 25px rgba(239, 68, 68, 0.6);
        }
    }

    @keyframes slide-in {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fade-in {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes expand {
        from {
            max-width: 40px;
            padding: 8px;
        }
        to {
            max-width: 500px;
            padding: 14px 16px;
        }
    }

    @keyframes avatar-pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }

    @keyframes avatar-spin {
        0% {
            transform: rotateY(0deg);
        }
        100% {
            transform: rotateY(360deg);
        }
    }
    
    @keyframes orb-float {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        50% {
            transform: translate(20px, -20px) scale(1.1);
        }
    }
    
    @keyframes gradient-shift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* ============================================================
       EFECTO GLASSMORPHISM - Tarjetas con efecto vidrio
       ============================================================ */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        padding: 24px;
        margin: 16px 0;
        animation: fade-in 0.3s ease-out;
    }
    
    .glass-header {
        background: rgba(42, 45, 62, 0.5);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--glass-border);
        padding: 20px 0;
        margin-bottom: 30px;
        animation: slide-in 0.3s ease-out;
    }
    
    .glass-card-hover:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(139, 92, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .success-pulse {
        animation: pulse-glow 2s infinite;
        padding: 12px 16px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border-left: 4px solid var(--success-green);
        font-weight: 500;
    }

    /* ============================================================
       GRADIENTES Y BOTONES
       ============================================================ */
    .gradient-primary {
        background: linear-gradient(135deg, var(--electric-blue), var(--cyber-purple));
        color: white;
        border: none;
    }
    
    .gradient-secondary {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid var(--glass-border);
    }
    
    .gradient-destructive {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        border: none;
    }
    
    /* Botones modernos minimalistas */
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        font-size: 14px;
        padding: 10px 24px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        background: rgba(42, 45, 62, 0.6);
        color: var(--foreground);
        backdrop-filter: blur(10px);
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        background: rgba(139, 92, 246, 0.15);
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Botones primarios con gradiente sutil */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.8), rgba(139, 92, 246, 0.8));
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: white;
        font-weight: 600;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.9), rgba(139, 92, 246, 0.9));
        box-shadow: 0 6px 16px rgba(139, 92, 246, 0.3);
        border-color: rgba(139, 92, 246, 0.5);
    }

    /* Botones de eliminación (X rojo) */
    button[key*="del_"] {
        color: var(--error-red) !important;
        border-color: var(--error-red) !important;
    }

    button[key*="del_"]:hover {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.1)) !important;
        transform: scale(1.05) !important;
    }

    /* ============================================================
       BADGES Y PILLS
       ============================================================ */
    .badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        font-size: 13px;
        margin-right: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        animation: fade-in 0.3s ease-out;
    }

    .badge-recording {
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }

    .badge-upload {
        background: linear-gradient(135deg, var(--electric-blue), #0284c7);
    }

    .badge-saved {
        background: linear-gradient(135deg, var(--success-green), #059669);
    }
    
    .badge-transcribed {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success-green);
        border: 1px solid var(--success-green);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
    }
    
    .badge-priority-high {
        background: rgba(239, 68, 68, 0.15);
        color: var(--error-red);
        border: 1px solid var(--error-red);
    }
    
    .badge-priority-medium {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning-orange);
        border: 1px solid var(--warning-orange);
    }
    
    .badge-priority-low {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success-green);
        border: 1px solid var(--success-green);
    }
    
    .badge-status {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .badge-status-open {
        background: rgba(14, 165, 233, 0.15);
        color: var(--electric-blue);
    }
    
    .badge-status-progress {
        background: rgba(139, 92, 246, 0.15);
        color: var(--cyber-purple);
    }
    
    .badge-status-closed {
        background: rgba(107, 114, 128, 0.15);
        color: #9ca3af;
    }
    
    /* ============================================================
       HEADER PERSONALIZADO
       ============================================================ */
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--electric-blue), var(--cyber-purple));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        transition: transform 0.5s ease;
    }
    
    .logo-icon:hover {
        transform: rotate(180deg);
    }
    
    .subtitle {
        font-size: 12px;
        color: var(--muted-foreground);
        margin: 0;
    }
    
    .header-actions {
        display: flex;
        gap: 12px;
    }
    
    .icon-btn {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        color: var(--foreground);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .icon-btn:hover {
        background: rgba(139, 92, 246, 0.2);
        transform: scale(1.05);
    }
    
    /* ============================================================
       INPUTS Y SELECTBOXES MODERNOS
       ============================================================ */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background: rgba(42, 45, 62, 0.6) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: var(--foreground) !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--cyber-purple) !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* File uploader moderno */
    [data-testid="stFileUploader"] {
        background: var(--glass-bg);
        border: 2px dashed var(--glass-border);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--cyber-purple);
        background: rgba(139, 92, 246, 0.1);
    }
    
    /* Audio input moderno */
    .stAudioInput {
        background: var(--glass-bg);
        border: 2px dashed var(--glass-border);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .stAudioInput:hover {
        border-color: var(--cyber-purple);
        background: rgba(139, 92, 246, 0.1);
    }
    
    /* Reproductor de audio moderno */
    audio {
        width: 100%;
        height: 48px;
        border-radius: 12px;
        background: rgba(42, 45, 62, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.2);
        outline: none;
        backdrop-filter: blur(10px);
    }
    
    audio::-webkit-media-controls-panel {
        background: rgba(42, 45, 62, 0.9);
        border-radius: 12px;
    }
    
    audio::-webkit-media-controls-play-button,
    audio::-webkit-media-controls-mute-button {
        filter: brightness(1.2) saturate(1.3);
    }
    
    audio::-webkit-media-controls-timeline {
        border-radius: 4px;
        margin: 0 8px;
    }
    
    audio::-webkit-media-controls-current-time-display,
    audio::-webkit-media-controls-time-remaining-display {
        color: rgba(255, 255, 255, 0.8);
        font-size: 12px;
    }

    /* ============================================================
       NOTIFICACIONES
       ============================================================ */
    .notification-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 40px;
        height: 40px;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px 0;
        position: relative;
    }

    .notification-icon:hover {
        transform: scale(1.1);
    }

    .notification-icon-success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 2px solid var(--success-green);
        color: var(--success-green);
    }

    .notification-icon-error {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 2px solid var(--error-red);
        color: var(--error-red);
    }

    .notification-icon-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 2px solid var(--warning-orange);
        color: var(--warning-orange);
    }

    .notification-icon-info {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(14, 165, 233, 0.1) 100%);
        border: 2px solid var(--electric-blue);
        color: var(--electric-blue);
    }

    /* Tooltip para el mensaje */
    .notification-tooltip {
        visibility: hidden;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.9);
        color: white;
        text-align: center;
        border-radius: 8px;
        padding: 8px 12px;
        white-space: nowrap;
        font-size: 12px;
        font-weight: 500;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
        max-width: 200px;
        word-wrap: break-word;
        white-space: normal;
    }

    .notification-icon:hover .notification-tooltip {
        visibility: visible;
        opacity: 1;
    }

    /* Arrow para tooltip */
    .notification-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(0, 0, 0, 0.9) transparent transparent transparent;
    }

    /* Estilos para notificaciones expandidas */
    .notification-expanded {
        animation: slide-in 0.3s ease-out;
        margin: 10px 0;
        border-radius: 12px;
        padding: 14px 16px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .notification-expanded-success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
        border-left: 4px solid var(--success-green);
        color: var(--success-green);
    }

    .notification-expanded-error {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.08) 100%);
        border-left: 4px solid var(--error-red);
        color: var(--error-red);
    }

    .notification-expanded-info {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(14, 165, 233, 0.08) 100%);
        border-left: 4px solid var(--electric-blue);
        color: var(--electric-blue);
    }

    .notification-expanded-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        border-left: 4px solid var(--warning-orange);
        color: var(--warning-orange);
    }

    /* ============================================================
       CHAT MEJORADO
       ============================================================ */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 20px 0;
    }

    .chat-message {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
        animation: slide-in 0.3s ease-out;
    }

    .chat-message-user {
        justify-content: flex-end;
    }

    .chat-message-ai {
        justify-content: flex-start;
    }

    .chat-bubble {
        max-width: 70%;
        padding: 14px 18px;
        border-radius: 16px;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 14px;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, var(--electric-blue), var(--cyber-purple));
        color: white;
        border-radius: 18px 18px 4px 18px;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }

    .chat-bubble-ai {
        background: var(--glass-bg);
        color: var(--foreground);
        border: 1px solid var(--glass-border);
        border-radius: 18px 18px 18px 4px;
        backdrop-filter: blur(10px);
    }

    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
        margin-top: 4px;
    }

    .chat-avatar-user {
        background: linear-gradient(135deg, var(--electric-blue), var(--cyber-purple));
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
    }

    .chat-avatar-ai {
        background: var(--glass-bg);
        border: 2px solid var(--glass-border);
        backdrop-filter: blur(10px);
    }

    .avatar-pulse {
        animation: avatar-pulse 2s ease-in-out infinite;
    }

    .avatar-spin {
        animation: avatar-spin 3s linear infinite;
    }
    
    /* ============================================================
       TARJETAS DE OPORTUNIDADES
       ============================================================ */
    .opportunity-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
        cursor: pointer;
        animation: fade-in 0.3s ease-out;
    }
    
    .opportunity-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .opportunity-card-high-priority {
        border-color: rgba(239, 68, 68, 0.4);
        animation: glow-high-priority 2s infinite;
    }
    
    .opportunity-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .ticket-number {
        background: rgba(14, 165, 233, 0.15);
        color: var(--electric-blue);
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        font-family: monospace;
    }
    
    .opportunity-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--foreground);
        margin: 8px 0;
    }
    
    .opportunity-description {
        font-size: 13px;
        color: var(--muted-foreground);
        line-height: 1.5;
        margin-bottom: 12px;
    }
    
    .opportunity-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* ============================================================
       ESPACIADO Y TIPOGRAFÍA
       ============================================================ */
    h1 {
        color: var(--foreground);
        margin-top: 40px;
        margin-bottom: 20px;
        font-weight: 700;
    }

    h2 {
        color: var(--foreground);
        margin-top: 32px;
        margin-bottom: 16px;
        font-weight: 600;
    }

    h3 {
        color: var(--foreground);
        margin-top: 24px;
        margin-bottom: 12px;
        font-weight: 600;
    }

    h4 {
        color: var(--foreground);
        margin-top: 16px;
        margin-bottom: 12px;
        font-weight: 500;
    }
    
    /* ============================================================
       KEYWORDS Y TAGS
       ============================================================ */
    .keyword-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, var(--cyber-purple), var(--electric-blue));
        padding: 10px 14px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        font-size: 13px;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
    }

    .keyword-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
    }
    
    /* ============================================================
       TABS MODERNOS
       ============================================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        color: var(--foreground);
        padding: 12px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: var(--cyber-purple);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(139, 92, 246, 0.2));
        border-color: var(--cyber-purple);
    }
    
    /* Ocultar el indicador azul debajo de las pestañas */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* ============================================================
       EFECTOS DE FONDO ANIMADOS
       ============================================================ */
    .background-effects {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.3;
        animation: orb-float 20s ease-in-out infinite;
    }
    
    .orb-1 {
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(14, 165, 233, 0.3), transparent 70%);
        top: -10%;
        left: -5%;
    }
    
    .orb-2 {
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.3), transparent 70%);
        bottom: -10%;
        right: -5%;
        animation-delay: -10s;
    }
    
    </style>
    """

