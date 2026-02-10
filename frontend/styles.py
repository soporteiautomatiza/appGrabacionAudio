"""
Estilos CSS modernos y profesionales para la aplicación
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
    /* Fondo y tipografía */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 20px;
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
        color: #94a3b8;
        padding: 10px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    section[data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    section[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        font-weight: 600;
    }
    
    /* Botones mejorados */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        padding: 8px 16px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        color: white;
    }
    
    button[kind="secondary"] {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: white;
    }
    
    /* Tarjetas y contenedores */
    [data-testid="stExpander"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    
    [data-testid="stExpander"]:hover {
        border-color: #3B82F6;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    
    /* Inputs y selects */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Tabs */
    [data-testid="stTabs"] {
        background: white;
    }
    
    [data-testid="stTab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTab"]:hover {
        background: #f3f4f6;
    }
    
    [data-testid="stTab"][aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
    }
    
    /* Métricas */
    [data-testid="metric-container"] {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Chat bubbles */
    .chat-bubble-user {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 5px 0;
        max-width: 70%;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    .chat-bubble-ai {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        color: #374151;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        margin: 5px 0;
        max-width: 70%;
        border: 1px solid #d1d5db;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Notificaciones */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    /* Badges para palabras clave */
    .keyword-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        padding: 8px 16px;
        border-radius: 20px;
        color: white;
        font-weight: 500;
        font-size: 14px;
        margin: 4px;
        box-shadow: 0 2px 4px rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    .keyword-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(139, 92, 246, 0.3);
    }
    
    /* Animaciones sutiles */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stAlert {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
    
    /* Ajustes para tablas */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Separadores */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
    }
    
    /* Headers con gradiente */
    h1, h2, h3 {
        background: linear-gradient(135deg, #3B82F6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding-bottom: 5px;
    }
    
    h2 {
        position: relative;
        padding-bottom: 10px;
    }
    
    h2:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #3B82F6, #8b5cf6);
        border-radius: 2px;
    }
    
    /* Cards para contenedores */
    .card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* Tooltips */
    [data-tooltip] {
        position: relative;
    }
    
    [data-tooltip]:before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    [data-tooltip]:hover:before {
        opacity: 1;
        visibility: visible;
        bottom: calc(100% + 8px);
    }
    </style>
    """