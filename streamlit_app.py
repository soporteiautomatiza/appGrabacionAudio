# streamlit_app.py (en la raíz del proyecto)
import subprocess
import sys
from pathlib import Path

# Ejecutar index.py desde frontend
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Importar todo desde frontend/index.py
exec(open(Path(__file__).parent / "frontend" / "index.py").read())
