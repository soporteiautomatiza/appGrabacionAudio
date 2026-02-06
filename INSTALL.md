# 🔧 Guía de Instalación y Configuración

## Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes)
- Git

## Pasos de Instalación

### 1. Clonar el Repositorio
```bash
git clone <tu_repositorio>
cd appGrabacionAudio
```

### 2. Crear Entorno Virtual
```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

#### Opción A: Para desarrollo local
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# - Obtén GEMINI_API_KEY de: https://ai.google.dev/
# - Obtén credenciales SUPABASE de: https://supabase.com/
```

#### Opción B: Para Streamlit Cloud
```bash
# Ir a: https://share.streamlit.io/
# En app settings, agregar estos secrets:
GEMINI_API_KEY=tu_valor
SUPABASE_URL=tu_valor
SUPABASE_KEY=tu_valor
```

### 5. Configurar Secrets en Streamlit (Opcional para Local)
```bash
# Crear archivo de secrets
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
GEMINI_API_KEY = "tu_valor_aqui"
SUPABASE_URL = "tu_valor_aqui"
SUPABASE_KEY = "tu_valor_aqui"
EOF
```

## Ejecución

### Opción 1: Usar script run.py
```bash
python run.py
```

### Opción 2: Ejecutar Streamlit directamente
```bash
streamlit run frontend/index.py
```

## Estructura de Carpetas Creadas

```
appGrabacionAudio/
├── frontend/           # Interfaz web (Streamlit)
├── backend/            # Lógica de negocio
├── data/              # Almacenamiento local
│   ├── recordings/    # Audios grabados
│   └── opportunities/ # Oportunidades en JSON (fallback)
└── .venv/             # Entorno virtual
```

## Solución de Problemas

### Error: "ModuleNotFoundError"
- Verifica que `.venv` esté activado
- Ejecuta: `pip install -r requirements.txt`

### Error de credenciales Supabase
- Verifica que `.env` o `secrets.toml` tengan los valores correctos
- Asegúrate de NO incluir espacios en blanco

### Error: "Permission denied"
- En Windows, ejecuta PowerShell como Administrador
- En Linux/Mac: `chmod +x run.py`

### Las carpetas data no se crean
- Las carpetas se crean automáticamente al ejecutar
- Si falla, crealas manualmente: `mkdir -p data/recordings data/opportunities`

## Seguridad - Checklist Importante

- [ ] Nunca commitear `.env`
- [ ] Nunca commitear `.streamlit/secrets.toml`
- [ ] Verificar que `.gitignore` incluya `data/` y archivos de secretos
- [ ] Cambiar las API keys en producción regularmente
- [ ] Usar credenciales separadas para desarrollo y producción
- [ ] Habilitar RLS (Row Level Security) en Supabase en producción

## Soporte

Si tienes problemas:
1. Revisa los logs: `streamlit run --logger.level=debug frontend/index.py`
2. Verifica las credenciales
3. Asegúrate de que las tablas en Supabase existan
