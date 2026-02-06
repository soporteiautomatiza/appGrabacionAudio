import streamlit as st
import os
from datetime import datetime
import httpx
import json

class SimpleSupabaseClient:
    """Cliente Supabase simplificado usando httpx directamente"""
    
    def __init__(self, url: str, key: str):
        self.url = url.rstrip('/')
        self.key = key
        self.rest_url = f'{self.url}/rest/v1'
        self.headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        self._client = httpx.Client()
    
    def table(self, table_name: str):
        """Retorna un objeto que permite hacer queries a una tabla"""
        return TableClient(self, table_name)

class TableClient:
    """Cliente para una tabla específica"""
    
    def __init__(self, db: SimpleSupabaseClient, table_name: str):
        self.db = db
        self.table_name = table_name
        self.url = f'{db.rest_url}/{table_name}'
        self.query_params = {}
        self.select_cols = '*'
        self.order_by = None
    
    def select(self, columns='*'):
        """SELECT columnas"""
        self.select_cols = columns
        return self
    
    def order(self, column, desc=False):
        """ORDER BY"""
        order_dir = 'desc' if desc else 'asc'
        self.order_by = f'{column}.{order_dir}'
        return self
    
    def eq(self, column, value):
        """WHERE column = value"""
        self.query_params[column] = f'eq.{value}'
        return self
    
    def execute(self):
        """Ejecuta la query"""
        try:
            params = {'select': self.select_cols}
            params.update(self.query_params)
            
            if self.order_by:
                params['order'] = self.order_by
            
            response = self.db._client.get(self.url, headers=self.db.headers, params=params)
            response.raise_for_status()
            
            # Retornar un objeto con atributo .data
            class Response:
                def __init__(self, data):
                    self.data = data
            
            return Response(response.json())
        
        except Exception as e:
            # Retornar respuesta vacía en caso de error
            class Response:
                def __init__(self):
                    self.data = []
            
            return Response()
    
    def insert(self, data):
        """INSERT datos"""
        try:
            response = self.db._client.post(self.url, headers=self.db.headers, json=data)
            response.raise_for_status()
            
            class Response:
                def __init__(self, data):
                    self.data = data if isinstance(data, list) else [data]
            
            return Response(response.json())
        except:
            class Response:
                def __init__(self):
                    self.data = []
            
            return Response()
    
    def delete(self):
        """DELETE"""
        return DeleteClient(self)

class DeleteClient:
    def __init__(self, table_client: TableClient):
        self.table_client = table_client
    
    def eq(self, column, value):
        self.table_client.query_params[column] = f'eq.{value}'
        return self
    
    def execute(self):
        """Ejecuta el delete"""
        try:
            response = self.table_client.db._client.delete(
                self.table_client.url,
                headers=self.table_client.db.headers,
                params=self.table_client.query_params
            )
            response.raise_for_status()
            
            class Response:
                data = []
            
            return Response()
        except:
            class Response:
                data = []
            
            return Response()

def create_client(url: str, key: str):
    """Crea un cliente Supabase"""
    return SimpleSupabaseClient(url, key)

@st.cache_resource
def init_supabase() -> Client:
    """Inicializa conexión con Supabase"""
    try:
        supabase_url = st.secrets.get("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY")
        
        # Debug: mostrar si existen los secrets
        if not supabase_url:
            return None
        if not supabase_key:
            return None
        
        # Limpiar espacios en blanco
        supabase_url = supabase_url.strip()
        supabase_key = supabase_key.strip()
        
        client = create_client(supabase_url, supabase_key)
        return client
    except Exception as e:
        return None

def save_recording_to_db(filename: str, filepath: str, transcription: str = None):
    """Guarda grabación en la base de datos"""
    try:
        db = init_supabase()
        if db is None:
            st.error("No se pudo conectar a Supabase")
            return False
        
        data = {
            "filename": filename,
            "filepath": filepath,
            "transcription": transcription,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.table("recordings").insert(data).execute()
        
        if response.data:
            st.success(f"✅ Guardado en Supabase: {filename}")
            return response.data[0]["id"]
        else:
            st.warning(f"⚠️ No se guardó correctamente")
            return None
    except Exception as e:
        st.error(f"❌ Error guardando: {str(e)}")
        return None

def get_all_recordings():
    """Obtiene todas las grabaciones de la BD"""
    try:
        db = init_supabase()
        if db is None:
            return []
        
        response = db.table("recordings").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error obteniendo grabaciones: {e}")
        return []

def update_transcription(recording_id: str, transcription: str):
    """Actualiza la transcripción de una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        response = db.table("recordings").update({
            "transcription": transcription,
            "updated_at": datetime.now().isoformat()
        }).eq("id", recording_id).execute()
        
        return True if response.data else False
    except Exception as e:
        st.error(f"Error actualizando transcripción: {e}")
        return False

def save_opportunity(recording_id: str, title: str, description: str):
    """Guarda una oportunidad asociada a una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        data = {
            "recording_id": recording_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.table("opportunities").insert(data).execute()
        return True if response.data else False
    except Exception as e:
        st.error(f"Error guardando oportunidad: {e}")
        return False

def get_opportunities_by_recording(recording_id: str):
    """Obtiene las oportunidades de una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return []
        
        response = db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error obteniendo oportunidades: {e}")
        return []
def delete_recording_from_db(recording_id: int):
    """Elimina una grabación de la base de datos"""
    try:
        db = init_supabase()
        if db is None:
            st.error("No se pudo conectar a Supabase")
            return False
        
        # Primero eliminar las oportunidades asociadas (por seguridad)
        try:
            delete_opportunities_by_recording(recording_id)
        except:
            pass  # Si no hay oportunidades, ignorar
        
        # Luego eliminar la grabación
        response = db.table("recordings").delete().eq("id", recording_id).execute()
        
        return True
    except Exception as e:
        st.error(f"❌ Error eliminando grabación: {str(e)}")
        return False

def delete_opportunities_by_recording(recording_id: int):
    """Elimina todas las oportunidades asociadas a una grabación"""
    try:
        db = init_supabase()
        if db is None:
            return False
        
        # Primero obtener los IDs de las oportunidades
        response = db.table("opportunities").select("id").eq("recording_id", recording_id).execute()
        
        if response.data and len(response.data) > 0:
            # Eliminar cada oportunidad
            for opp in response.data:
                db.table("opportunities").delete().eq("id", opp["id"]).execute()
        
        return True
    except Exception as e:
        return False

def delete_recording_by_filename(filename: str):
    """Busca y elimina una grabación por nombre de archivo"""
    try:
        db = init_supabase()
        if db is None:
            st.error("No se pudo conectar a Supabase")
            return False
        
        # Buscar el recording_id por filename
        try:
            response = db.table("recordings").select("id").eq("filename", filename).execute()
            
            if response.data and len(response.data) > 0:
                recording_id = response.data[0]["id"]
                result = delete_recording_from_db(recording_id)
                if result:
                    st.success(f"✅ Grabación eliminada de Supabase")
                return result
            else:
                # No existe en BD (ya fue eliminado o nunca se guardó)
                return True
        except Exception as e:
            # Si no existe, retornar True (no es error)
            return True
    except Exception as e:
        st.error(f"Error eliminando grabación: {str(e)}")
        return False