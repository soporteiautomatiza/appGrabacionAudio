"""OpportunitiesManager.py - Extrae oportunidades (300 → 140 líneas)"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import streamlit as st
import sys
import google.generativeai as genai
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger
from database import init_supabase
from helpers import safe_json_dump
from config import GEMINI_API_KEY

logger = get_logger(__name__)
BASE_DIR = Path(__file__).parent.parent / "data" / "opportunities"
KEYWORDS_DICT_PATH = Path(__file__).parent.parent / "keywords_dict.json"

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

class OpportunitiesManager:
    def __init__(self):
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        self.db = init_supabase()
    
    def get_recording_id(self, filename: str) -> Optional[str]:
        """Obtiene ID del recording"""
        try:
            if not self.db:
                logger.warning(f"DB unavailable: {filename}")
                return None
            result = self.db.table("recordings").select("id").eq("filename", filename).execute()
            recording_id = result.data[0]["id"] if result.data else None
            if recording_id:
                logger.debug(f"Recording ID: {recording_id}")
            else:
                logger.warning(f"Recording not found: {filename}")
            return recording_id
        except Exception as e:
            logger.error(f"get_recording_id: {type(e).__name__} - {str(e)}")
            return None
    
    def extract_opportunities(self, transcription: str, keywords_list: List[str]) -> List[Dict]:
        """Extrae oportunidades de keywords en transcripción"""
        if not keywords_list:
            return []
        
        opportunities, words = [], transcription.lower().split()
        for keyword in keywords_list:
            occurrence_count = 0
            for i, word in enumerate(words):
                if keyword.lower() not in word:
                    continue
                occurrence_count += 1
                context_window = 15
                start, end = max(0, i - context_window), min(len(words), i + context_window + 1)
                
                opportunity = {
                    "id": f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{keyword}_{occurrence_count}",
                    "keyword": keyword,
                    "context_before": " ".join(words[start:i]),
                    "context_after": " ".join(words[i+1:end]),
                    "full_context": f"{' '.join(words[start:i])} **{keyword}** {' '.join(words[i+1:end])}",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "new",
                    "notes": "",
                    "occurrence": occurrence_count,
                    "priority": "Medium",
                    "title": keyword
                }
                opportunities.append(opportunity)
        return opportunities
    
    def save_opportunity(self, opportunity: Dict, audio_filename: str) -> bool:
        """Guarda oportunidad en BD/local"""
        try:
            if not self.db:
                logger.warning(f"BD unavailable, saving locally: {audio_filename}")
                return self._save_local(opportunity, audio_filename)
            
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"Recording ID not found, fallback local")
                return self._save_local(opportunity, audio_filename)
            
            priority = opportunity.get("priority", "Medium").capitalize()
            data = {
                "recording_id": recording_id,
                "title": opportunity.get("keyword", "Opportunity"),
                "description": opportunity.get("full_context", ""),
                "status": opportunity.get("status", "new"),
                "priority": priority,
                "notes": opportunity.get("notes", ""),
                "created_at": datetime.now().isoformat()
            }
            
            result = self.db.table("opportunities").insert(data).execute()
            if result.data:
                supabase_id = result.data[0].get("id")
                opportunity["supabase_id"] = supabase_id
                opportunity["id"] = supabase_id
                logger.info(f"✓ Opportunity saved: {supabase_id}")
                return True
            
            logger.warning(f"Supabase empty response, fallback local")
            return self._save_local(opportunity, audio_filename)
        
        except Exception as e:
            logger.error(f"save_opportunity: {type(e).__name__} - {str(e)}")
            return self._save_local(opportunity, audio_filename)
    
    def _save_local(self, opportunity: Dict, audio_filename: str) -> bool:
        """Fallback: guarda JSON localmente"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        return safe_json_dump(opportunity, filename, BASE_DIR)
    
    def load_opportunities(self, audio_filename: str) -> List[Dict]:
        """Carga oportunidades desde BD/local"""
        try:
            if not self.db:
                logger.warning(f"BD unavailable, loading local: {audio_filename}")
                return self._load_local(audio_filename)
            
            recording_id = self.get_recording_id(audio_filename)
            if not recording_id:
                logger.warning(f"Recording ID not found, fallback local")
                return self._load_local(audio_filename)
            
            result = self.db.table("opportunities").select("*").eq("recording_id", recording_id).execute()
            if not result.data:
                logger.debug(f"No opportunities found for: {audio_filename}")
                return []
            
            opportunities = [{
                "id": r.get("id"),
                "supabase_id": r.get("id"),
                "keyword": r.get("title", ""),
                "full_context": r.get("description", ""),
                "status": r.get("status", "new"),
                "notes": r.get("notes", ""),
                "priority": r.get("priority", "Medium"),
                "created_at": r.get("created_at", ""),
                "occurrence": 1
            } for r in result.data]
            
            logger.info(f"✓ Loaded {len(opportunities)} opportunities")
            return opportunities
        
        except Exception as e:
            logger.error(f"load_opportunities: {type(e).__name__} - {str(e)}")
            return self._load_local(audio_filename)
    
    def _load_local(self, audio_filename: str) -> List[Dict]:
        """Carga oportunidades de archivos JSON locales"""
        opportunities = []
        try:
            pattern = f"opp_{audio_filename.replace('.', '_')}_*.json"
            for filepath in BASE_DIR.glob(pattern):
                with open(filepath, "r", encoding="utf-8") as f:
                    opportunities.append(json.load(f))
            return opportunities if opportunities else []
        except:
            return []
    
    def update_opportunity(self, opportunity_id: str, updates: Dict) -> bool:
        """Actualiza oportunidad"""
        try:
            if not self.db:
                logger.warning("BD unavailable for update")
                return False
            
            result = self.db.table("opportunities").update(updates).eq("id", opportunity_id).execute()
            if result.data:
                logger.info(f"✓ Opportunity updated: {opportunity_id}")
                return True
            
            logger.warning(f"Update returned empty")
            return False
        
        except Exception as e:
            logger.error(f"update_opportunity: {type(e).__name__} - {str(e)}")
            return False
    
    def delete_opportunity(self, opportunity_id: str) -> bool:
        """Elimina oportunidad"""
        try:
            if not self.db:
                logger.warning("BD unavailable for delete")
                return False
            
            result = self.db.table("opportunities").delete().eq("id", opportunity_id).execute()
            logger.info(f"✓ Opportunity deleted: {opportunity_id}")
            return True
        
        except Exception as e:
            logger.error(f"delete_opportunity: {type(e).__name__} - {str(e)}")
            return False
    
    def load_keywords_dict(self) -> Dict:
        """Carga el diccionario de keywords desde JSON"""
        try:
            if not KEYWORDS_DICT_PATH.exists():
                logger.warning(f"Keywords dict not found at {KEYWORDS_DICT_PATH}")
                return {}
            
            with open(KEYWORDS_DICT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading keywords dict: {type(e).__name__} - {str(e)}")
            return {}
    
    def extract_speakers_from_transcription(self, transcription: str) -> Dict[str, List[str]]:
        """Extrae speakers y sus fragmentos de la transcripción con formato 'Nombre: "..."'"""
        speakers = {}
        try:
            # Patrón para detectar "Nombre: "texto""
            pattern = r'^([^:]+):\s*["\']?(.+?)["\']?\s*$'
            
            for line in transcription.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(pattern, line)
                if match:
                    speaker = match.group(1).strip()
                    text = match.group(2).strip()
                    
                    if speaker not in speakers:
                        speakers[speaker] = []
                    speakers[speaker].append(text)
            
            return speakers if speakers else {"Unknown": [transcription]}
        except Exception as e:
            logger.error(f"Error extracting speakers: {type(e).__name__} - {str(e)}")
            return {"Unknown": [transcription]}
    
    def analyze_opportunities_with_ai(
        self, 
        transcription: str, 
        audio_filename: str
    ) -> Tuple[int, List[Dict]]:
        """
        Análisis inteligente de oportunidades usando Gemini.
        Detección de intenciones y conceptos, no solo palabras clave exactas.
        
        Args:
            transcription: Texto completo de la transcripción
            audio_filename: Nombre del archivo de audio para asociar la oportunidad
        
        Returns:
            Tuple con (número de oportunidades detectadas, lista de oportunidades)
        """
        try:
            # Cargar diccionario de keywords
            keywords_dict = self.load_keywords_dict()
            if not keywords_dict:
                logger.warning("Keywords dict is empty, skipping AI analysis")
                return 0, []
            
            # Extraer speakers de la transcripción
            speakers = self.extract_speakers_from_transcription(transcription)
            logger.info(f"Speakers detectados: {list(speakers.keys())}")
            
            # Preparar lista de temas
            temas = keywords_dict.get("temas_de_interes", {})
            config = keywords_dict.get("configuracion", {})
            
            if not temas:
                logger.warning("No topics found in keywords dict")
                return 0, []
            
            speakers_list = ", ".join(speakers.keys())
            
            # Limitar transcripción si es necesario
            transcription_limited = transcription[:12000] if len(transcription) > 12000 else transcription
            
            # PROMPT EXTREMADAMENTE DIRECTO
            prompt = f"""CRÍTICO: Analiza esta conversación/reunión palabra por palabra. Detecta TODAS las oportunidades que encuentres.

MAPEO SIMPLE:
• Presupuesto / dinero / gasto / inversión / coste → "Presupuesto" (HIGH)
• Contactar / llamar / tarea / acción / hacer / pendiente / debe / responsabilidad → "Acción requerida" (HIGH)
• Regulación / ley / cumplimiento / compliance / auditoría / riesgo legal → "Cumplimiento Legal" (HIGH)
• Formación / capacitación / entrenamiento / curso / educación → "Formación" (MEDIUM)
• Contratar / empleado / personal / equipo / rol / recurso humano → "Recursos Humanos" (MEDIUM)
• Cliente / venta / deal / contrato / negocio / oportunidad / acuerdo → "Cierre de venta" (HIGH)
• Decisión / cambio / estrategia / importante / aprobado → "Decisión importante" (HIGH)
• Herramienta / infraestructura / sistema / plataforma / equipo tecnológico → "Infraestructura" (MEDIUM)

TRANSCRIPCIÓN:
{transcription_limited}

SPEAKERS: {speakers_list}

RESPONDE SOLO CON JSON (sin markdown, sin explicaciones):

{{"analisis_completo": true, "oportunidades": [{{"tema": "TemaExacto", "prioridad": "high/medium/low", "mencionado_por": "Nombre", "contexto": "frase", "confianza": 0.85}}]}}

Si no hay oportunidades: {{"analisis_completo": true, "oportunidades": []}}"""
            
            # Llamar a Gemini
            logger.info(f"Iniciando analisis con Gemini para: {audio_filename}")
            logger.info(f"Modelo: {config.get('modelo_gemini', 'gemini-2.0-flash')}")
            logger.info(f"Transcripción: {len(transcription_limited)} caracteres, Speakers: {speakers_list}")
            
            model = genai.GenerativeModel(config.get("modelo_gemini", "gemini-2.0-flash"))
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            logger.info(f"Respuesta Gemini recibida: {len(response_text)} caracteres")
            logger.info(f"RESPUESTA COMPLETA:\n{response_text}")
            
            # Limpiar respuesta
            # Remover markdown code blocks
            if "```json" in response_text:
                logger.info("Limpiando: encontrado ```json")
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                logger.info("Limpiando: encontrado ```")
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Remover caracteres de control
            response_text = response_text.strip()
            logger.info(f"Texto limpio: {response_text[:200]}")
            
            # Parsear JSON
            try:
                response_json = json.loads(response_text)
                logger.info(f"JSON parseado exitosamente: {response_json}")
            except json.JSONDecodeError as e:
                logger.error(f"ERROR al parsear JSON: {str(e)[:100]}")
                logger.error(f"Response text: {response_text[:300]}")
                # Intentar limpiar y reparsear
                try:
                    # Buscar el primer { y último }
                    start = response_text.find("{")
                    end = response_text.rfind("}") + 1
                    if start >= 0 and end > start:
                        cleaned = response_text[start:end]
                        logger.info(f"Intentando limpiar JSON desde {start} a {end}")
                        response_json = json.loads(cleaned)
                        logger.info("JSON recuperado tras limpieza")
                    else:
                        logger.error("No JSON encontrado en respuesta")
                        return 0, []
                except Exception as clean_err:
                    logger.error(f"Error en cleanup: {str(clean_err)[:100]}")
                    return 0, []
            
            oportunidades_data = response_json.get("oportunidades", [])
            logger.info(f"IA detectó {len(oportunidades_data)} oportunidades: {oportunidades_data}")
            
            if not oportunidades_data:
                logger.info(f"Análisis completado: 0 oportunidades detectadas")
                return 0, []
            
            # Obtener recording_id
            recording_id = self.get_recording_id(audio_filename)
            
            # Si no hay recording_id en BD, retornar las oportunidades detectadas al menos
            # (aunque no se puedan guardar en BD)
            if not recording_id:
                logger.warning(f"Recording ID not found, cannot save to DB but IA detected {len(oportunidades_data)} opportunities")
                # Retornar el número de oportunidades detectadas para mostrar feedback al usuario
                # aunque no se guarden en BD
                return len(oportunidades_data), []
            
            # Guardar cada oportunidad
            saved_opportunities = []
            for idx, opp in enumerate(oportunidades_data, 1):
                try:
                    tema = str(opp.get("tema", "")).strip()
                    mencionado_por = str(opp.get("mencionado_por", "Unknown")).strip()
                    contexto = str(opp.get("contexto", "")).strip()
                    confianza = float(opp.get("confianza", 0.8))
                    prioridad_str = str(opp.get("prioridad", "medium")).lower().strip()
                    
                    # Validar tema
                    if tema not in temas:
                        logger.warning(f"Tema '{tema}' no está en diccionario. Temas válidos: {list(temas.keys())}")
                        continue
                    
                    # Validar confianza
                    min_confianza = float(config.get("minimo_confianza", 0.5))
                    if confianza < min_confianza:
                        logger.debug(f"Opp {idx}: Confianza {confianza:.2f} < {min_confianza:.2f}")
                        continue
                    
                    if not contexto:
                        logger.warning(f"Opp {idx}: Sin contexto")
                        continue
                    
                    # Mapear prioridades
                    priority_map = {"high": "High", "medium": "Medium", "low": "Low"}
                    priority = priority_map.get(prioridad_str, "Medium")
                    
                    # Construir nota
                    tema_data = temas.get(tema, {})
                    nota = f"🤖 TICKET GENERADO AUTOMÁTICAMENTE\n\n"
                    nota += f"📌 Tema: {tema}\n"
                    nota += f"📝 Descripción: {tema_data.get('descripcion', '')}\n"
                    nota += f"👤 Mencionado por: {mencionado_por}\n"
                    nota += f"💬 Contexto: {contexto}\n"
                    nota += f"🎯 Confianza: {confianza:.0%}"
                    
                    opportunity_data = {
                        "recording_id": recording_id,
                        "title": f"[IA] {tema} - {mencionado_por}",
                        "description": contexto,
                        "status": "new",
                        "priority": priority,
                        "notes": nota,
                        "created_at": datetime.now().isoformat(),
                        "mencionado_por": mencionado_por
                    }
                    
                    # Insertar en Supabase
                    if self.db:
                        result = self.db.table("opportunities").insert(opportunity_data).execute()
                        if result.data:
                            opp_id = result.data[0].get("id")
                            logger.info(f"✅ Opp {idx} guardada: {opp_id} (Tema: {tema}, Por: {mencionado_por})")
                            saved_opportunities.append(result.data[0])
                        else:
                            logger.warning(f"Opp {idx}: Respuesta vacía de Supabase")
                    else:
                        logger.warning("DB no disponible")
                
                except Exception as inner_e:
                    logger.error(f"Error guardando opp {idx}: {type(inner_e).__name__} - {str(inner_e)}")
            
            total = len(saved_opportunities)
            total_detectadas = len(oportunidades_data)
            logger.info(f"ANÁLISIS COMPLETADO: {total} guardadas / {total_detectadas} detectadas")
            
            # Retornar total detectadas (para mostrar feedback), y las guardadas (si existen)
            return total_detectadas, saved_opportunities
        
        except Exception as e:
            logger.error(f"analyze_opportunities_with_ai error: {type(e).__name__} - {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return 0, []
            import traceback
            logger.error(traceback.format_exc())
            return 0, []

