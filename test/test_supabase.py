"""
Archivo de prueba de conexión a Supabase
Ejecuta este archivo localmente para debuggear problemas
"""

import streamlit as st
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

supabase = None

try:
    from supabase import create_client
    
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
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.write(f"Tipo de error: {type(e).__name__}")

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
            st.write("**Primeros 3 registros:**")
            for rec in response.data[:3]:
                st.json(rec)
        else:
            st.info("No hay grabaciones en la BD (Esto es OK)")
            
    except Exception as e:
        st.error(f"❌ Error consultando: {e}")
        st.write(f"Tipo de error: {type(e).__name__}")
        st.write(f"Mensaje completo: {str(e)}")
else:
    st.warning("⚠️ No hay cliente para consultar (falla en PASO 2)")

# ============================================
# PASO 4: Intentar insertar datos
# ============================================
st.header("PASO 4: Insertar Dato de Prueba")

if supabase:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Insertar grabación de prueba"):
            try:
                test_data = {
                    "filename": "test_streamlit_local.wav",
                    "filepath": "/test/test_streamlit_local.wav",
                    "transcription": "Prueba desde test_supabase.py local",
                    "created_at": "2026-02-05T10:00:00",
                }
                
                st.info(f"Insertando:")
                st.json(test_data)
                
                response = supabase.table("recordings").insert(test_data).execute()
                
                if response.data:
                    st.success("✅ ¡Insertado exitosamente!")
                    st.json(response.data[0])
                else:
                    st.warning("⚠️ Respuesta vacía")
                    
            except Exception as e:
                st.error(f"❌ Error insertando: {e}")
                st.write(f"Tipo: {type(e).__name__}")
    
    with col2:
        if st.button("🔄 Recargar datos"):
            st.rerun()
else:
    st.warning("⚠️ No hay cliente para insertar (falla en PASO 2)")

# ============================================
# PASO 5: Información de debugging
# ============================================
st.header("PASO 5: Info de Debugging")

st.subheader("Variables:")
st.json({
    "SUPABASE_URL_presente": bool(url),
    "SUPABASE_KEY_presente": bool(key),
    "URL_inicia_bien": url.startswith("https://") if url else False,
    "Key_inicia_bien": key.startswith("sb_publishable") if key else False,
    "Cliente_creado": supabase is not None,
})

st.subheader("Checklist:")
st.checkbox("¿RLS está DESHABILITADO en tabla 'recordings'?", value=False)
st.checkbox("¿RLS está DESHABILITADO en tabla 'opportunities'?", value=False)
st.checkbox("¿La URL es correcta?", value=False)
st.checkbox("¿La API key es una PUBLISHABLE key (no secret)?", value=False)
st.checkbox("¿No hay espacios en blanco en los secrets?", value=False)

st.divider()

st.info("""
💡 **Si algo falla:**
1. Verifica el checklist arriba
2. En Supabase → Settings → API Keys → Rota la key
3. Copia la nueva PUBLISHABLE key
4. Actualiza en `.env` local
5. Vuelve a ejecutar este test

**Si falla en PASO 2 (crear cliente):**
- Probablemente API key invalida
- Regenera en Supabase

**Si falla en PASO 3 (consultar):**
- Probablemente RLS está activado
- Desactívalo en ambas tablas
""")
