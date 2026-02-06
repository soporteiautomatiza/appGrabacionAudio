import json
import os
from datetime import datetime
from pathlib import Path

OPPORTUNITIES_DIR = "opportunities"

class OpportunitiesManager:
    def __init__(self):
        Path(OPPORTUNITIES_DIR).mkdir(exist_ok=True)
    
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
                        "occurrence": occurrence_count  # Número de la ocurrencia
                    }
                    
                    opportunities.append(opportunity)
        
        return opportunities
    
    def save_opportunity(self, opportunity, audio_filename):
        """Guarda una oportunidad en un archivo JSON"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        filepath = os.path.join(OPPORTUNITIES_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(opportunity, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_opportunities(self, audio_filename):
        """Carga todas las oportunidades asociadas a un audio"""
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
        """Actualiza una oportunidad existente"""
        filename = f"opp_{audio_filename.replace('.', '_')}_{opportunity['id']}.json"
        filepath = os.path.join(OPPORTUNITIES_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(opportunity, f, ensure_ascii=False, indent=2)
    
    def delete_opportunity(self, opportunity_id, audio_filename):
        """Elimina una oportunidad"""
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
