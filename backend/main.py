"""
Aplicación principal FastAPI
Punto de entrada de la API
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.core.config import get_settings
from app.core.database import init_db
from app.routes import auth, audio, chat, history

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener configuración
settings = get_settings()

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API robusta para gestión de grabaciones de audio, transcripciones y chat con IA",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware simple de logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response

# Inicializar base de datos
@app.on_event("startup")
async def startup():
    """Evento de inicio de la aplicación"""
    logger.info(f"🚀 Iniciando aplicación en ambiente: {settings.ENVIRONMENT}")
    try:
        init_db()
        logger.info("✅ Base de datos inicializada")
    except Exception as e:
        logger.error(f"❌ Error inicializando BD: {str(e)}")

@app.on_event("shutdown")
async def shutdown():
    """Evento de cierre de la aplicación"""
    logger.info("🛑 Aplicación cerrada")

# Incluir rutas
app.include_router(auth.router)
app.include_router(audio.router)
app.include_router(chat.router)
app.include_router(history.router)

# Rutas raíz
@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz de la API"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "🟢 Online",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Verificar estado de salud de la API"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

# Manejo de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno del servidor"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
