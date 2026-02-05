"""
Rutas de Autenticación: registro, login, refresh token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario
    
    - **email**: Email único del usuario
    - **full_name**: Nombre completo
    - **password**: Contraseña (mínimo 8 caracteres)
    """
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            logger.warning(f"Intento de registro con email existente: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear nuevo usuario
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hash_password(user_data.password)
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"Nuevo usuario registrado: {user_data.email}")
        
        # Generar tokens
        access_token = create_access_token({"sub": str(new_user.id)})
        refresh_token = create_refresh_token({"sub": str(new_user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar usuario"
        )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión con email y contraseña
    
    - **email**: Email del usuario
    - **password**: Contraseña
    
    Returns: Tokens de acceso y refresco
    """
    try:
        # Buscar usuario
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user:
            logger.warning(f"Intento de login con email inexistente: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña inválidos"
            )
        
        # Verificar contraseña
        if not verify_password(credentials.password, user.password_hash):
            logger.warning(f"Intento de login con contraseña incorrecta: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña inválidos"
            )
        
        if not user.is_active:
            logger.warning(f"Intento de login con usuario inactivo: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo"
            )
        
        logger.info(f"Login exitoso: {credentials.email}")
        
        # Generar tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al iniciar sesión"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token_str: str):
    """
    Refresca el token de acceso usando un refresh token
    
    - **refresh_token_str**: Token de refresco válido
    """
    try:
        payload = verify_token(refresh_token_str)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )
        
        user_id = payload.get("sub")
        
        # Generar nuevo access token
        access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})
        
        logger.info(f"Token refrescado para usuario: {user_id}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al refrescar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo refrescar el token"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: dict = Depends(auth_dependency), db: Session = Depends(get_db)):
    """Obtiene los datos del usuario actual"""
    try:
        user = db.query(User).filter(User.id == int(current_user["user_id"])).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo usuario actual: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener datos del usuario"
        )

# Dependencia reutilizable
from app.core.security import get_current_user as auth_dependency
