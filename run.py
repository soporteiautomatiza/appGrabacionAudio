#!/usr/bin/env python
"""
Script para ejecutar la aplicación Streamlit manteniendo la estructura segura backend/frontend
"""
import subprocess
import sys
from pathlib import Path

# Obtener el directorio de la aplicación
app_dir = Path(__file__).parent / "frontend"

# Ejecutar Streamlit apuntando a index.py en la carpeta frontend
subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_dir / "index.py")])
