import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import streamlit as st
import sys

# Agregar ruta padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from database import init_supabase

logger = get_logger(__name__)

# Obtener ruta a datos desde la carpeta parent/data
BASE_DIR = Path(__file__).parent.parent / "data"
OPPORTUNITIES_DIR = BASE_DIR / "opportunities"

class OpportunitiesManager:
    def __init__(self) -> None:
        OPPORTUNITIES_DIR.mkdir(parents=True, exist_ok=True)
        self.db = None
        try:
            # Inicializar cliente Supabase
            self.db = init_supabase()
        except Exception as e:
            logger.warning(f"Failed to initialize Supabase client: {str(e)}. Using local fallback.")
    
    def get_recording_id(self, filename: str) -> Optional[str]:
        """Obtiene el ID del recording por nombre de archivo"""
        try:
            if not self.db:
                logger.warning(f"Base de datos no disponible para obtener ID de {filename}")
                return None
            
            response = self.db.table("recordings").select("id").eq("filename", filename).execute()
            if response and response.data and len(response.data) > 0:
                recording_id = response.data[0]["id"]
                logger.debug(f"Recording ID obtenido para {filename}: {recording_id}")
                return recording_id
            
            logger.warning(f"No se encontró recording para {filename}")
            return None
        except Exception as e:
            logger.error(f"Error al obtener recording ID para {filename}: {type(e).__name__} - {str(e)}")
            return None
    
    def extract_opportunities(self, transcription: str, keywords_list: List[str]) -> List[Dict]:
        """Extrae oportunidades de negocio basadas en palabras clave encontradas en la transcripción"""
        opportunities = []
        
        if not keywords_list:
            return opportunities
        
        # Dividir la transcripción en palabras
        words = transcription.lower().split()
        
        for keyword in keywords_list:
            keyword_lower = keyword.lower()
            occurrence_count = 0
            
            # Buscar TODAS las ocurrencias de la palabra clave
            for i, word in enumerate(words):
                if keyword_lower in word:
                    occurrence_count += 1
                    
                    # Extraer contexto: 15 palabras antes y después (más contexto)
                    context_window = 15
                    start = max(0, i - context_window)
                    end = min(len(words), i + context_window + 1)
                    
                    context_before = " ".join(words[start:i])
                    context_after = " ".join(words[i+1:end])
                    
                    # Crear un ID único para cada ocurrencia
                    opportunity_id = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{keyword}_{occurrence_count}"
                    
                    opportunity = {
                        "id": opportunity_id,
                        "keyword": keyword,
                        "context_before": context_before,
                        "context_after": context_after,
                        "full_context": f"{context_before} **{keyword}** {context_after}",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "new",
                        "notes": "",
                        "occurrence": occurrence_count,  # Número de la ocurrencia
                        "priority": "Medium",
                        "title": keyword
                    }
                    
                    opportunities.append(opportunity)
        
        return opportunities
    
    def save_opportunity(self, opportunity: Dict, audio_filename: str) -> bool:
        """Guarda una oportunidad en Supabase"""
        try:
            if not self.db:
                logger.warning(f"BD no disponible, guardando oportunidad localmente para {audio_filename}")
                return self._save_opportunity_local(opportunity, audio_filename)
            
            # Obtener el recording_id
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"No se puede guardar oportunidad: Recording ID no encontrado para {audio_filename}")
                return self._save_opportunity_local(opportunity, audio_filename)
            
            # Preparar datos para Supabase - con formato correcto para la tabla
            priority = opportunity.get("priority", "Medium")
            # Asegurar que la prioridad tiene el formato correcto (capitalizada)
            if priority.lower() == "low":
                priority = "Low"
            elif priority.lower() == "high":
                priority = "High"
            elif priority.lower() == "medium":
                priority = "Medium"
            
            data = {
                "recording_id": recording_id,
                "title": opportunity.get("keyword", "Oportunidad"),
                "description": opportunity.get("full_context", ""),
                "status": opportunity.get("status", "new"),
                "priority": priority,
                "notes": opportunity.get("notes", ""),
                "created_at": datetime.now().isoformat()
            }
            
            # Guardar en Supabase
            response = self.db.table("opportunities").insert(data).execute()
            
            if response and response.data and len(response.data) > 0:
                # Guardar el ID de Supabase para futuros updates/deletes
                supabase_id = response.data[0].get("id")
                opportunity["supabase_id"] = supabase_id
                opportunity["id"] = supabase_id
                logger.info(f"Oportunidad guardada en Supabase: {supabase_id} para {audio_filename}")
                return True
            
            logger.warning(f"Supabase respondió vacío al guardar oportunidad para {audio_filename}")
            return False
        
        except Exception as e:
            logger.error(f"Error al guardar oportunidad para {audio_filename}: {type(e).__name__} - {str(e)}")
            logger.info("Haciendo fallback a almacenamiento local")
            return self._save_opportunity_local(opportunity, audio_filename)
    
    def _save_opportunity_local(self, opportunity, audio_filename):
        """Fallback: Guarda una oportunidad en archivo JSON"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        filepath = OPPORTUNITIES_DIR / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(opportunity, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def load_opportunities(self, audio_filename: str) -> List[Dict]:
        """Carga todas las oportunidades asociadas a un audio desde Supabase"""
        opportunities = []
        
        try:
            if not self.db:
                logger.warning(f"BD no disponible, cargando oportunidades locales para {audio_filename}")
                return self._load_opportunities_local(audio_filename)
            
            # Obtener el recording_id
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"No se puede cargar oportunidades: Recording ID no encontrado para {audio_filename}")
                return self._load_opportunities_local(audio_filename)
            
            # Cargar desde Supabase
            response = self.db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
            
            if response and response.data:
                for record in response.data:
                    opportunity = {
                        "id": record.get("id"),
                        "supabase_id": record.get("id"),
                        "keyword": record.get("title", ""),
                        "full_context": record.get("description", ""),
                        "status": record.get("status", "new"),
                        "notes": record.get("notes", ""),
                        "priority": record.get("priority", "Medium"),
                        "created_at": record.get("created_at", ""),
                        "occurrence": 1
                    }
                    opportunities.append(opportunity)
                logger.info(f"Cargadas {len(opportunities)} oportunidades desde Supabase para {audio_filename}")
            else:
                logger.debug(f"No hay oportunidades en Supabase para {audio_filename}")
        
        except Exception as e:
            logger.error(f"Error al cargar oportunidades para {audio_filename}: {type(e).__name__} - {str(e)}")
            logger.info("Haciendo fallback a archivos locales")
            return self._load_opportunities_local(audio_filename)
        
        return opportunities
    
    def _load_opportunities_local(self, audio_filename):
        """Fallback: Carga oportunidades desde archivos JSON"""
        opportunities = []
        prefix = f"opp_{audio_filename.replace('.', '_')}_"
        
        try:
            files = os.listdir(str(OPPORTUNITIES_DIR))
            for file in files:
                if file.startswith(prefix) and file.endswith(".json"):
                    filepath = OPPORTUNITIES_DIR / file
                    with open(filepath, "r", encoding="utf-8") as f:
                        opp = json.load(f)
                        opportunities.append(opp)
        except Exception as e:
            logger.warning(f"Error loading local opportunities for {audio_filename}: {str(e)}")
        
        return opportunities
    
    def update_opportunity(self, opportunity: Dict, audio_filename: str) -> bool:
        """Actualiza una oportunidad en Supabase"""
        try:
            if not self.db:
                logger.warning(f"BD no disponible, actualizando oportunidad localmente")
                return self._update_opportunity_local(opportunity, audio_filename)
            
            # Obtener el ID (puede estar en 'id' o 'supabase_id')
            opp_id = opportunity.get("supabase_id") or opportunity.get("id")
            
            if not opp_id:
                logger.error(f"No se puede actualizar oportunidad: ID no disponible")
                return self._update_opportunity_local(opportunity, audio_filename)
            
            # Actualizar en Supabase - campos que admite la tabla
            update_data = {
                "status": opportunity.get("status", "new"),
                "priority": opportunity.get("priority", "Medium"),
                "description": opportunity.get("full_context", ""),
                "notes": opportunity.get("notes", "")
            }
            
            # Intentar actualizar
            response = self.db.table("opportunities").update(update_data).eq("id", opp_id).execute()
            
            if response is not None and len(response.data) > 0:
                logger.info(f"Oportunidad actualizada en Supabase: {opp_id}")
                return True
            
            logger.warning(f"Supabase no confirmó actualización de oportunidad {opp_id}")
            return False
        
        except Exception as e:
            logger.error(f"Error al actualizar oportunidad {opportunity.get('id', 'unknown')}: {type(e).__name__} - {str(e)}")
            logger.info("Haciendo fallback a almacenamiento local")
            return self._update_opportunity_local(opportunity, audio_filename)
    
    def _update_opportunity_local(self, opportunity, audio_filename):
        """Fallback: Actualiza una oportunidad en archivo JSON"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        filepath = OPPORTUNITIES_DIR / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(opportunity, f, ensure_ascii=False, indent=2)
    
    def delete_opportunity(self, opportunity_id: str, audio_filename: str) -> bool:
        """Elimina una oportunidad de Supabase"""
        try:
            if self.db and opportunity_id:
                # Intentar eliminar de Supabase usando el UUID
                response = self.db.table("opportunities").delete().eq("id", opportunity_id).execute()
                if response:
                    logger.info(f"Oportunidad eliminada de Supabase: {opportunity_id}")
                    return True
                else:
                    logger.warning(f"Supabase no confirmó eliminación de oportunidad {opportunity_id}")
            else:
                logger.warning(f"No se puede conectar a BD para eliminar oportunidad {opportunity_id}")
        except Exception as e:
            logger.error(f"Error al eliminar oportunidad {opportunity_id} de Supabase: {type(e).__name__} - {str(e)}")
        
        # Fallback: eliminar archivo local
        logger.debug(f"Intentando eliminación local de oportunidad {opportunity_id}")
        return self._delete_opportunity_local(opportunity_id, audio_filename)
    
    def _delete_opportunity_local(self, opportunity_id, audio_filename):
        """Fallback: Elimina una oportunidad del archivo JSON"""
        prefix = f"opp_{audio_filename.replace('.', '_')}_"
        
        try:
            files = os.listdir(str(OPPORTUNITIES_DIR))
            for file in files:
                if file.startswith(prefix) and opportunity_id in file:
                    filepath = OPPORTUNITIES_DIR / file
                    filepath.unlink()
                    return True
        except Exception as e:
            logger.error(f"Error deleting local opportunity {opportunity_id}: {str(e)}")
        
        return False
