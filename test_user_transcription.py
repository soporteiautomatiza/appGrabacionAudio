#!/usr/bin/env python
"""Test rapido de la transcripcion del usuario"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from OpportunitiesManager import OpportunitiesManager
from logger import get_logger

logger = get_logger(__name__)

# Transcripcion exacta del usuario (con el typo "aime:")
user_transcription = """aime: "Buenos, buenos días a todos. Hoy necesitamos hablar del presupuesto para este trimestre. Estimamos que necesitamos unos $75,000 para invertir en nuevas herramientas y software. ¿Todos de acuerdo?"
Mónica: "Sí, estoy de acuerdo, Jaime, pero alguien tiene que contactar a los proveedores para negociar los precios. Yo no tengo tiempo esta semana. ¿Quién se puede encargar?"
Fran: "Yo me encargo de eso, Mónica, también hemos considerado los temas de compliance. Necesitamos asegurarnos de que cumplimos todas las regulaciones antes de implementar nada nuevo."
Jaime: "Excelente pregunta, Fran, vamos a necesitar entrenar al equipo en esta nueva plataforma. ¿Podríamos contratar a alguien especializado para dar los cursos?"
Mónica: "Buena idea. Y otra cosa, tenemos un cliente realmente interesado en nuestros servicios. Creo que es el momento perfecto para cerrar ese dia. ¿Alguien puede trabajar en la propuesta esta semana?"
Fran: "Yo puedo ayudar con eso, pero primero necesitamos resolver lo del presupuesto y contactar a ese proveedor. Eso es de acción inmediata."
Jaime: "Perfecto, entonces Fran contacta a proveedores, alguien trabaja en la propuesta del cliente y buscamos a alguien para la capacitación. ¿Están listos?"
Fran: "Sí."
"""

def main():
    print("=" * 80)
    print("TEST: Transcripcion del Usuario")
    print("=" * 80)
    
    import google.generativeai as genai
    from config import GEMINI_API_KEY
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    print(f"\nTranscripcion ({len(user_transcription)} caracteres):")
    print("-" * 80)
    print(user_transcription[:400])
    print("...")
    print("-" * 80)
    
    # Test con el OpportunitiesManager
    manager = OpportunitiesManager()
    
    print("\n[ANALIZANDO CON GEMINI]...")
    num_opps, detected_opps = manager.analyze_opportunities_with_ai(
        transcription=user_transcription,
        audio_filename="user_test.wav"
    )
    
    print(f"\n[RESULTADO]")
    print(f"  Detectadas: {num_opps}")
    print(f"  Guardadas en BD: {len(detected_opps) if detected_opps else 0}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
