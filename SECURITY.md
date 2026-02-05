# 🔒 Seguridad y API Keys

## Manejo Seguro de Credenciales

### 1. **Configuración Local**
- Copia `.env.example` a `.env`: 
  ```bash
  cp .env.example .env
  ```
- Edita `.env` y agrega tus API keys reales
- **NUNCA** hagas commit de `.env`

### 2. **Variables de Entorno en Producción**
Para Streamlit Cloud o GitHub Codespaces:
1. Ve a Settings → Secrets
2. Agrega: `GEMINI_API_KEY` con tu valor
3. También: `OPENAI_API_KEY` si la usas

### 3. **Regenerar API Keys (URGENTE si estaban en GitHub)**

#### Google Gemini API:
1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Haz clic en "Create API Key"
3. Copia la nueva key a tu `.env`

#### OpenAI API (si la usas):
1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Haz clic en "Create new secret key"
3. Copia la nueva key a tu `.env`

### 4. **Limpiar Histórico de Git** (si la key ya estaba expuesta)
```bash
# Opción 1: Usar BFG (más fácil)
git clone --mirror https://github.com/tuusuario/appGrabacionAudio.git
bfg --delete-files .env appGrabacionAudio.git
cd appGrabacionAudio.git
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push

# Opción 2: Usar git-filter-branch
git filter-branch --force --index-filter \
  "git rm -r --cached --ignore-unmatch .env" \
  -- --all
```

### 5. **Seguridad en el Código**
✅ Correcto (lo que ya tienes):
```python
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

❌ Nunca hagas:
```python
GEMINI_API_KEY = "AIzaSyA_frNnDxrjQ5SpL6jhEZSNhpTnH7zqSy0"  # ¡NUNCA!
```

### 6. **Verificación Pre-Commit**
Para prevenir accidentes, instala un pre-commit hook:
```bash
pip install pre-commit
```

Crea `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--allow-missing-credentials']
```

Instala el hook:
```bash
pre-commit install
```

---
**Última revisión**: Feb 5, 2026
