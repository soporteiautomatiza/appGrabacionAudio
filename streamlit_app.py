#!/usr/bin/env python3
"""
streamlit_app.py - Entrada principal para Streamlit Cloud
Ejecuta correctamente frontend/index.py resolviendo los imports
"""
import sys
from pathlib import Path

# Configurar paths ANTES de cualquier import de la app
backend_path = str(Path(__file__).parent / "backend")
frontend_path = str(Path(__file__).parent / "frontend")

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if frontend_path not in sys.path:
    sys.path.insert(0, frontend_path)

# Ahora ejecutar el archivo principal del frontend
# Nota: Este truco funciona porque estamos en el mismo proceso Python
import runpy
index_path = str(Path(__file__).parent / "frontend" / "index.py")

# Ejecutar como si fuera el main
runpy.run_path(index_path, run_name="__main__")
