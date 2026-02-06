"""
Estilos CSS modernos para la aplicación
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
    /* Contenedor principal centrado */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 40px;
    }
    
    .stMainBlockContainer {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0;
    }
    
    [data-testid="stAppViewContainer"] > section {
        max-width: 1200px;
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
    
    @keyframes pulse-glow {
        0% { 
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        }
        70% { 
            box-shadow: 0 0 0 20px rgba(76, 175, 80, 0);
        }
        100% { 
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
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

    .success-pulse {
        animation: pulse-glow 1.5s infinite;
        padding: 12px 16px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
        border-left: 4px solid #4CAF50;
        font-weight: 500;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 6px;
        color: white;
        font-weight: 600;
        font-size: 14px;
        margin-right: 8px;
    }

    .badge-recording {
        background: linear-gradient(135deg, #FF6B6B, #FF5252);
    }

    .badge-upload {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
    }

    .badge-saved {
        background: linear-gradient(135deg, #95E77D, #4CAF50);
    }

    /* Estilos para notificaciones compactas con emoticono */
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
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
        border: 2px solid #34d399;
        color: #10b981;
    }

    .notification-icon-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 2px solid #f87171;
        color: #dc2626;
    }

    .notification-icon-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 2px solid #fbbf24;
        color: #d97706;
    }

    .notification-icon-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid #60a5fa;
        color: #2563eb;
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

    /* Estilos para notificaciones expandidas (para debug) */
    .notification-expanded {
        animation: slide-in 0.3s ease-out;
        margin: 10px 0;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .notification-expanded-success {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15) 0%, rgba(34, 197, 94, 0.08) 100%);
        border-left: 5px solid #34d399;
        color: #10b981;
    }

    .notification-expanded-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.15) 0%, rgba(239, 68, 68, 0.08) 100%);
        border-left: 5px solid #f87171;
        color: #dc2626;
    }

    .notification-expanded-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(59, 130, 246, 0.08) 100%);
        border-left: 5px solid #60a5fa;
        color: #2563eb;
    }

    /* Estilos para el chat */
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
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 14px;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
    }

    .chat-bubble-ai {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.1) 0%, rgba(75, 85, 99, 0.05) 100%);
        color: #e5e7eb;
        border: 1px solid rgba(107, 114, 128, 0.2);
        border-radius: 18px 18px 18px 4px;
    }

    .chat-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
        margin-top: 4px;
    }

    .chat-avatar-user {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }

    .chat-avatar-ai {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(75, 85, 99, 0.15) 100%);
        border: 1px solid rgba(107, 114, 128, 0.3);
    }

    .avatar-pulse {
        animation: avatar-pulse 2s ease-in-out infinite;
    }

    .avatar-spin {
        animation: avatar-spin 3s linear infinite;
    }
    </style>
    """

