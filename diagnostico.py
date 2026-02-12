#!/usr/bin/env python
"""Test diagnostico del problema"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from OpportunitiesManager import OpportunitiesManager
from logger import get_logger

logger = get_logger(__name__)

# Transcripcion del audio que el usuario subio (segun la captura)
transcription_text = """Jaime: "Buenos, buenos días a todos. Hoy necesitamos hablar del presupuesto para este trimestre. Estimamos que necesitamos unos $75,000 para invertir en nuevas herramientas y software. ¿Todos de acuerdo?"
Mónica: "Sí, estoy de acuerdo, Jaime, pero alguien tiene que contactar a los proveedores para negociar los precios. Yo no tengo tiempo esta semana. ¿Quién se puede encargar?"
Fran: "Yo me encargo de eso, Mónica, también hemos considerado los temas de compliance. Necesitamos asegurarnos de que cumplimos todas las regulaciones antes de implementar nada nuevo."
Jaime: "Excelente pregunta, Fran, vamos a necesitar entrenar al equipo en esta nueva plataforma. ¿Podríamos contratar a alguien especializado para dar los cursos?"
Mónica: "Buena idea. Y otra cosa, tenemos un cliente realmente interesado en nuestros servicios. Creo que es el momento perfecto para cerrar ese dia. ¿Alguien puede trabajar en la propuesta esta semana?"
Fran: "Yo puedo ayudar con eso, pero primero necesitamos resolver lo del presupuesto y contactar a ese proveedor. Eso es de acción inmediata."
Jaime: "Perfecto, entonces Fran contacta a proveedores, alguien trabaja en la propuesta del cliente y buscamos a alguien para la capacitación. ¿Están listos?"
Fran: "Sí."
"""

print("=" * 80)
print("DIAGNOSTICO DEL PROBLEMA")
print("=" * 80)

manager = OpportunitiesManager()
print(f"\nAnalizando transcripción ({len(transcription_text)} caracteres)...")

num_opps, detected = manager.analyze_opportunities_with_ai(
    transcription=transcription_text,
    audio_filename="conversation_presupuestos.wav"
)

print(f"\n[RESULTADO]")
print(f"  Detectadas: {num_opps}")
print(f"  Guardadas: {len(detected) if detected else 0}")
print("\n" + "=" * 80)
