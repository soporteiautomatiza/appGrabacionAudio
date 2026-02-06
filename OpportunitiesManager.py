import json
import os
from datetime import datetime
from pathlib import Path
import streamlit as st
from database import init_supabase

OPPORTUNITIES_DIR = "opportunities"

class OpportunitiesManager:
    def __init__(self):
        Path(OPPORTUNITIES_DIR).mkdir(exist_ok=True)
        self.db = None
        try:
            # Inicializar cliente Supabase
            self.db = init_supabase()
        except:
            pass
    
    def get_recording_id(self, filename):
        """Obtiene el ID del recording por nombre de archivo"""
        try:
            if not self.db:
                return None
            
            response = self.db.table("recordings").select("id").eq("filename", filename).execute()
            if response and response.data and len(response.data) > 0:
                return response.data[0]["id"]
        except:
            pass
        return None
    
    def extract_opportunities(self, transcription, keywords_list):
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
    
    def save_opportunity(self, opportunity, audio_filename):
        """Guarda una oportunidad en Supabase"""
        try:
            if not self.db:
                # Fallback a archivo JSON si no hay BD
                return self._save_opportunity_local(opportunity, audio_filename)
            
            # Obtener el recording_id
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                # Fallback a archivo JSON
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
                opportunity["id"] = supabase_id  # También guardar como id principal
                return True
            
            return False
        
        except Exception as e:
            # Fallback a archivo JSON
            return self._save_opportunity_local(opportunity, audio_filename)
    
    def _save_opportunity_local(self, opportunity, audio_filename):
        """Fallback: Guarda una oportunidad en archivo JSON"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        filepath = os.path.join(OPPORTUNITIES_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(opportunity, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_opportunities(self, audio_filename):
        """Carga todas las oportunidades asociadas a un audio desde Supabase"""
        opportunities = []
        
        try:
            if not self.db:
                # Fallback a archivos locales
                return self._load_opportunities_local(audio_filename)
            
            # Obtener el recording_id
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                # Fallback a archivos locales
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
        
        except Exception as e:
            # Fallback a archivos locales
            return self._load_opportunities_local(audio_filename)
        
        return opportunities
    
    def _load_opportunities_local(self, audio_filename):
        """Fallback: Carga oportunidades desde archivos JSON"""
        opportunities = []
        prefix = f"opp_{audio_filename.replace('.', '_')}_"
        
        try:
            files = os.listdir(OPPORTUNITIES_DIR)
            for file in files:
                if file.startswith(prefix) and file.endswith(".json"):
                    filepath = os.path.join(OPPORTUNITIES_DIR, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        opp = json.load(f)
                        opportunities.append(opp)
        except:
            pass
        
        return opportunities
    
    def update_opportunity(self, opportunity, audio_filename):
        """Actualiza una oportunidad en Supabase"""
        try:
            if not self.db:
                # Fallback a archivo JSON
                return self._update_opportunity_local(opportunity, audio_filename)
            
            # Obtener el ID (puede estar en 'id' o 'supabase_id')
            opp_id = opportunity.get("supabase_id") or opportunity.get("id")
            
            if not opp_id:
                # Fallback a archivo JSON si no hay ID
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
            
            return response is not None and len(response.data) > 0
        
        except Exception as e:
            # Fallback a archivo JSON
            return self._update_opportunity_local(opportunity, audio_filename)
    
    def _update_opportunity_local(self, opportunity, audio_filename):
        """Fallback: Actualiza una oportunidad en archivo JSON"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        filepath = os.path.join(OPPORTUNITIES_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(opportunity, f, ensure_ascii=False, indent=2)
    
    def delete_opportunity(self, opportunity_id, audio_filename):
        """Elimina una oportunidad de Supabase"""
        try:
            if self.db and opportunity_id:
                # Intentar eliminar de Supabase usando el UUID
                response = self.db.table("opportunities").delete().eq("id", opportunity_id).execute()
                if response:
                    return True
        except:
            pass
        
        # Fallback: eliminar archivo local
        return self._delete_opportunity_local(opportunity_id, audio_filename)
    
    def _delete_opportunity_local(self, opportunity_id, audio_filename):
        """Fallback: Elimina una oportunidad del archivo JSON"""
        prefix = f"opp_{audio_filename.replace('.', '_')}_"
        
        try:
            files = os.listdir(OPPORTUNITIES_DIR)
            for file in files:
                if file.startswith(prefix) and opportunity_id in file:
                    filepath = os.path.join(OPPORTUNITIES_DIR, file)
                    os.remove(filepath)
                    return True
        except:
            pass
        
        return False
