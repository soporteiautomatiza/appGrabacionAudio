"""
Estilos CSS modernos para la aplicación
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
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

    /* Estilos modernos para notificaciones */
    .notification-container {
        animation: slide-in 0.3s ease-out;
        margin: 10px 0;
    }

    .notification-success {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
        border-left: 5px solid #34d399;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        color: #10b981;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }

    .notification-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-left: 5px solid #f87171;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        color: #dc2626;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
    }

    .notification-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-left: 5px solid #fbbf24;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        color: #d97706;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.1);
    }

    .notification-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
        border-left: 5px solid #60a5fa;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        color: #2563eb;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
    }
    </style>
    """
