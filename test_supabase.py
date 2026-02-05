"""
Archivo de prueba de conexión a Supabase
Ejecuta este archivo localmente para debuggear problemas
"""

import streamlit as st
from supabase import create_client
import json

st.set_page_config(layout="wide", page_title="Test Supabase Connection")

st.title("🔧 Prueba de Conexión a Supabase")

st.write("Este archivo ayuda a debuggear problemas de conexión a Supabase")

# ============================================
# PASO 1: Verificar que los secrets existan
# ============================================
st.header("PASO 1: Verificar Secrets")

url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

if url:
    st.success(f"✅ SUPABASE_URL encontrado: {url}")
else:
    st.error("❌ SUPABASE_URL NO encontrado")

if key:
    st.success(f"✅ SUPABASE_KEY encontrado: {key[:30]}...")
    st.info(f"Key completa: {key}")
else:
    st.error("❌ SUPABASE_KEY NO encontrado")

# ============================================
# PASO 2: Intentar crear el cliente
# ============================================
st.header("PASO 2: Crear Cliente Supabase")

try:
    if url and key:
        # Limpiar espacios
        url_clean = url.strip()
        key_clean = key.strip()
        
        st.info(f"Intentando conectar con:")
        st.json({
            "url": url_clean,
            "key": key_clean[:20] + "..."
        })
        
        supabase = create_client(url_clean, key_clean)
        st.success("✅ Cliente creado exitosamente")
    else:
        st.error("No hay credentials para conectar")
        supabase = None
except Exception as e:
    st.error(f"❌ Error creando cliente: {e}")
    st.write(f"Tipo de error: {type(e).__name__}")
    supabase = None

# ============================================
# PASO 3: Intentar consultar tabla
# ============================================
st.header("PASO 3: Consultar Tabla 'recordings'")

if supabase:
    try:
        st.info("Intentando SELECT * FROM recordings...")
        response = supabase.table("recordings").select("*").execute()
        
        st.success(f"✅ Consulta exitosa!")
        st.write(f"Registros encontrados: {len(response.data)}")
        
        if response.data:
            st.write("**Últimas 3 grabaciones:**")
            for rec in response.data[-3:]:
                st.json(rec)
        else:
            st.info("No hay grabaciones en la BD")
            
    except Exception as e:
        st.error(f"❌ Error consultando: {e}")
        st.write(f"Tipo de error: {type(e).__name__}")
else:
    st.warning("⚠️ No hay cliente para consultar")

# ============================================
# PASO 4: Intentar insertar datos
# ============================================
st.header("PASO 4: Insertar Dato de Prueba")

if supabase:
    if st.button("Insertar grabación de prueba"):
        try:
            test_data = {
                "filename": "test_from_streamlit.wav",
                "filepath": "/test/test_from_streamlit.wav",
                "transcription": "Esta es una transcripción de prueba",
                "created_at": "2026-02-05T10:00:00",
            }
            
            st.info(f"Insertando: {json.dumps(test_data, indent=2)}")
            
            response = supabase.table("recordings").insert(test_data).execute()
            
            if response.data:
                st.success("✅ ¡Insertado exitosamente!")
                st.json(response.data[0])
            else:
                st.warning("⚠️ No se insertó")
                
        except Exception as e:
            st.error(f"❌ Error insertando: {e}")
            st.write(f"Tipo de error: {type(e).__name__}")
else:
    st.warning("⚠️ No hay cliente para insertar")

# ============================================
# PASO 5: Información de debugging
# ============================================
st.header("PASO 5: Info de Debugging")

st.subheader("Variables de entorno:")
st.json({
    "SUPABASE_URL_presente": bool(url),
    "SUPABASE_KEY_presente": bool(key),
    "URL_válida": url.startswith("https://") if url else False,
    "Key_válida": key.startswith("sb_publishable") if key else False,
})

st.subheader("Verificar en Supabase:")
st.write("1. ¿RLS está DESHABILITADO en ambas tablas?")
st.write("2. ¿La URL es correcta?")
st.write("3. ¿La API key es una PUBLISHABLE key?")
st.write("4. ¿No hay espacios en blanco en los secrets?")

st.divider()

st.info("""
💡 **Pasos si algo falla:**
1. Copia el error exacto que ves
2. Ve a Supabase → Settings → API Keys
3. Regenera la PUBLISHABLE key
4. Actualiza en Streamlit Cloud Secrets
5. Haz Reboot app
6. Vuelve a ejecutar este test
""")
