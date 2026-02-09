# 🔐 Guía: Configurar Streamlit Secrets en Streamlit Cloud

> Cómo configurar credenciales seguras en Streamlit Cloud sin exponerlas en el código

---

## 📋 Tabla de contenidos

1. [Conceptos básicos](#conceptos-básicos)
2. [Streamlit Cloud - Interfaz web](#streamlit-cloud---interfaz-web)
3. [Streamlit Cloud - Archivo secrets.toml](#streamlit-cloud---archivo-secretstoml)
4. [Desarrollo local](#desarrollo-local)
5. [Testing y debugging](#testing-y-debugging)
6. [Seguridad: Mejores prácticas](#seguridad-mejores-prácticas)

---

## 🎯 Conceptos básicos

### ¿Qué son los Secrets?

Los "Secrets" son variables de entorno privadas que:
- **No se commitean a Git** ✅
- **No se exponen en logs públicos** ✅
- **Se sincronican automáticamente** a Streamlit Cloud ✅
- Se usan igual que en desarrollo local (`st.secrets.get("KEY")`)

### Flujo de credenciales

```
Local (.env) 
    ↓
.gitignore (no commitear) 
    ↓
Streamlit Cloud (Settings → Secrets) 
    ↓
st.secrets.get("KEY")
```

---

## 🚀 Streamlit Cloud - Interfaz web

### Paso 1: Acceder a Settings

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Encuentra tu app en la lista
3. Haz click en los **3 puntos** (menú) → **Settings**

```
Tu App
├── (botón) New app
├── (botón) Shared items
├── (3 puntos) Settings  ← AQUÍ
└── (3 puntos) Delete app
```

### Paso 2: Abrir Secrets

En la ventana de Settings, busca la sección **"Secrets"** en la parte izquierda

```
Settings
├── General
├── Secrets   ← AQUÍ
└── Advanced
```

### Paso 3: Agregar credenciales

En el editor de Secrets, agrega tus variables en formato TOML:

```toml
# Google Gemini API
GEMINI_API_KEY = "AIzaSyXxxx..."

# Supabase
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "sb_publishable_xxx..."

# Logging (opcional)
LOG_LEVEL = "INFO"
```

### Paso 4: Guardar y reiniciar

1. Haz click en **"Save"** (abajo)
2. Ve a tu app
3. Haz click en el menú (**⋮**) → **Reboot app**
4. ¡Listo! Los secrets están disponibles

```python
# Dentro de tu app:
api_key = st.secrets.get("GEMINI_API_KEY")
db_url = st.secrets.get("SUPABASE_URL")
```

---

## 💾 Streamlit Cloud - Archivo secrets.toml

### Método alternativo: Upload directo

Si los Secrets son complejos, puedes subirlos como archivo:

1. En la sección Secrets, busca **"Copy paste your secrets from .streamlit/secrets.toml"**
2. **Copia TODO el contenido** de tu `.streamlit/secrets.toml` local
3. **Pégalo en el editor** de Secrets en Streamlit Cloud
4. Haz click en **Save**

### Formato TOML correcto

```toml
# ✅ CORRECTO
GEMINI_API_KEY = "AIzaSyXxxx..."
SUPABASE_URL = "https://xxx.supabase.co"

# ❌ INCORRECTO (sin comillas)
GEMINI_API_KEY = AIzaSyXxxx...

# ❌ INCORRECTO (con bash export)
export GEMINI_API_KEY="AIzaSyXxxx..."
```

---

## 🖥️ Desarrollo local

### Opción 1: Usar archivo .env

Para desarrollo local, puedes usar `.env` en lugar de secrets.toml:

**`.env`** (NO commitear):
```
GEMINI_API_KEY=AIzaSyXxxx...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=sb_publishable_xxx...
```

**`.gitignore`** (ya existe):
```
.env
.env.local
.streamlit/secrets.toml
```

**`config.py`** Lee desde `.env`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
```

### Opción 2: Usar .streamlit/secrets.toml local

Para sincronizar con Streamlit Cloud:

**`.streamlit/secrets.toml`** (NO commitear):
```toml
GEMINI_API_KEY = "AIzaSyXxxx..."
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "sb_publishable_xxx..."
```

**En tu código:**
```python
import streamlit as st

api_key = st.secrets.get("GEMINI_API_KEY")
db_url = st.secrets.get("SUPABASE_URL")
```

---

## ✅ Testing y debugging

### Ver los Secrets que está usando

```python
import streamlit as st

# Ver TODOS los secrets (solo para debug)
st.write(dict(st.secrets))  # ⚠️ Cuidado: muestra valores reales

# Ver un secret específico
api_key = st.secrets.get("GEMINI_API_KEY")
st.write(f"API Key (primeros 10 chars): {api_key[:10]}...")
```

### Verificar que los Secrets están disponibles

```python
import streamlit as st

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ GEMINI_API_KEY configurada")
except KeyError:
    st.error("❌ GEMINI_API_KEY NO ENCONTRADA")
```

### Debugging local vs Cloud

| Entorno | Dónde leer credenciales | Archivo |
|---------|------------------------|---------|
| **Local** | `.env` con `os.getenv()` | `.env` |
| **Local (Streamlit)** | `st.secrets` | `.streamlit/secrets.toml` |
| **Cloud** | `st.secrets` | Settings → Secrets |

---

## 🔐 Seguridad: Mejores prácticas

### ✅ HACER

```python
# ✅ Usar st.secrets en Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", default=None)

# ✅ Usar dotenv + os.getenv para apps no-Streamlit
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ✅ Validar que las credenciales existen
if not api_key:
    raise ValueError("GEMINI_API_KEY no está configurada")

# ✅ Mantener .env en .gitignore
# .env
# .streamlit/secrets.toml
```

### ❌ NO HACER

```python
# ❌ Hardcodear credenciales
GEMINI_API_KEY = "AIzaSyXxxx..."  # NUNCA

# ❌ Commitear .env
git add .env  # NUNCA

# ❌ Mostrar credenciales en logs
logger.info(f"API Key: {api_key}")  # NUNCA (excepto primeros chars)

# ❌ Usar variables de sesión para secrets
st.session_state.api_key = "..." # NUNCA
```

### Ejemplo de uso SEGURO

```python
# config.py - Manejo centralizado de credenciales
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_secret(key: str, default=None) -> str:
    """Obtiene un secret de forma segura (intenta Streamlit primero, luego .env)"""
    try:
        # Intenta desde Streamlit Secrets
        return st.secrets.get(key, default)
    except FileNotFoundError:
        # Fallback a .env
        return os.getenv(key, default)

# Uso en tu app
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
SUPABASE_URL = get_secret("SUPABASE_URL")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY no configurada en secrets ni .env")
```

---

## 🐛 Troubleshooting

### "KeyError: 'GEMINI_API_KEY'"

**Problema:** Secret no encontrado

**Soluciones:**
1. Verifica el nombre exacto en `st.secrets`
2. En Cloud: Settings → Secrets → Verifica que está ahí
3. Haz click en "Reboot app" después de agregar secrets
4. Usa `st.secrets.get()` en lugar de `st.secrets[]` para evitar error

```python
# ✅ Seguro
api_key = st.secrets.get("GEMINI_API_KEY", default=None)

# ❌ Puede fallar
api_key = st.secrets["GEMINI_API_KEY"]  # KeyError si no existe
```

### "No se puede conectar a Supabase"

**Problema:** Credenciales incorrectas o espacios en blanco

**Soluciones:**
1. Verifica que no haya espacios al inicio/final:
   ```toml
   # ❌ INCORRECTO
   SUPABASE_URL = " https://xxx.supabase.co "
   
   # ✅ CORRECTO
   SUPABASE_URL = "https://xxx.supabase.co"
   ```
2. Copia directamente desde Supabase (Settings → API)
3. En el código, limpia espacios:
   ```python
   url = st.secrets.get("SUPABASE_URL", "").strip()
   key = st.secrets.get("SUPABASE_KEY", "").strip()
   ```

### Secrets no se actualizan después de cambiar

**Problema:** App está cacheando valores viejos

**Solución:**
1. Ve a tu app en Streamlit Cloud
2. Menú (**⋮**) → **Reboot app**
3. Espera a que se reinicie

---

## 📚 Referencias

- [Streamlit Secrets Documentation](https://docs.streamlit.io/library/advanced-features/secrets-management)
- [Supabase API Keys](https://supabase.com/docs/guides/api/api-keys)
- [Google Gemini API Keys](https://ai.google.dev/docs/api_key_quick_start)
- [Python dotenv](https://github.com/thixo/python-dotenv)

---

## ✨ Resumen rápido

| Tarea | Pasos |
|-------|-------|
| **Local: .env** | 1. Crear `.env` 2. Agregar `KEY=value` 3. Usar `os.getenv("KEY")` |
| **Local: Streamlit** | 1. Crear `.streamlit/secrets.toml` 2. Agregar credenciales 3. Usar `st.secrets.get("KEY")` |
| **Cloud** | 1. Tu app → Settings 2. Secrets → Pegar contenido 3. Save 4. Reboot app |
| **Seguridad** | ✅ .gitignore ✅ No hardcodear ✅ Validar existencia |

---

**Última actualización:** Febrero 2026  
**Versión:** 1.0.0  

> 💡 **Tip:** ¿Error en Streamlit Cloud? Revisa los logs en Settings → Logs para ver mensajes de error detallados.
