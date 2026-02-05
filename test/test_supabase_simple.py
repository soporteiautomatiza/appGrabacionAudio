import psycopg2
import streamlit as st

st.set_page_config(page_title="Test Supabase Simple", layout="wide")
st.title("🔧 Test Conexión Supabase (Simple)")

# Cargar secretos
supabase_url = st.secrets.get("SUPABASE_URL", "").strip()
supabase_key = st.secrets.get("SUPABASE_KEY", "").strip()

st.write("## PASO 1: Verificar Secretos")
if supabase_url:
    st.success(f"✅ URL encontrada: {supabase_url}")
else:
    st.error("❌ URL no encontrada")

if supabase_key:
    st.success(f"✅ KEY encontrada: {supabase_key[:40]}...")
else:
    st.error("❌ KEY no encontrada")

# Extraer credenciales de la URL de Supabase
# URL formato: https://PROJECT_ID.supabase.co
project_id = supabase_url.split("//")[1].split(".")[0] if supabase_url else None
st.write(f"Project ID: `{project_id}`")

st.write("\n## PASO 2: Conectar a PostgreSQL")

if supabase_url and supabase_key and project_id:
    try:
        # Supabase usa estos detalles de conexión
        conn = psycopg2.connect(
            host=f"{project_id}.supabase.co",
            user="postgres",
            password=supabase_key,
            database="postgres",
            port=5432
        )
        st.success("✅ **CONECTADO a Supabase PostgreSQL**")
        
        cursor = conn.cursor()
        
        st.write("\n## PASO 3: Consultar tabla 'recordings'")
        try:
            cursor.execute("SELECT COUNT(*) FROM recordings;")
            count = cursor.fetchone()[0]
            st.success(f"✅ Tabla 'recordings' existe - {count} registros")
        except Exception as e:
            st.error(f"❌ Error consultando tabla: {str(e)}")
        
        st.write("\n## PASO 4: Insertar dato de prueba")
        try:
            cursor.execute("""
                INSERT INTO recordings (filename, file_path) 
                VALUES (%s, %s)
                RETURNING id;
            """, ("test_" + str(__import__('time').time()), "/tmp/test.wav"))
            new_id = cursor.fetchone()[0]
            conn.commit()
            st.success(f"✅ Dato insertado - ID: {new_id}")
        except Exception as e:
            st.error(f"❌ Error insertando: {str(e)}")
        
        conn.close()
        
    except psycopg2.OperationalError as e:
        st.error(f"❌ **NO CONECTADO** - Error de conexión:")
        st.error(str(e))
    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")
else:
    st.warning("⚠️ Falta información en los secretos")
