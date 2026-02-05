# 🧪 Quick Test - Probar la API

Este archivo contiene ejemplos rápidos para testear todos los endpoints de la API.

1. **Asegúrate de que Backend está corriendo:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **En otra terminal, ejecuta los siguiente comandos:**

---

## 1️⃣ Registro de Usuario

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "full_name": "Test User",
    "password": "SecurePass123"
  }'
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Guarda el access_token para los próximos requests**

---

## 2️⃣ Login de Usuario

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "SecurePass123"
  }'
```

---

## 3️⃣ Obtener Datos del Usuario Actual

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

Replace `YOUR_ACCESS_TOKEN_HERE` con el token del paso 1.

---

## 4️⃣ Subir Archivo de Audio

```bash
# Asegúrate de tener un archivo de audio local (test-audio.mp3)
curl -X POST "http://localhost:8000/audios/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -F "file=@test-audio.mp3"
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "filename": "test-audio.mp3",
  "file_size": 102400,
  "duration": null,
  "status": "uploaded",
  "created_at": "2026-02-05T10:00:00"
}
```

**Guarda el ID para verificar transcripción después**

---

## 5️⃣ Listar Audios del Usuario

```bash
curl -X GET "http://localhost:8000/audios/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "filename": "test-audio.mp3",
    "file_size": 102400,
    "status": "completed",
    "transcription": {
      "id": 1,
      "text": "...",
      "keywords": ["..."],
      "confidence": 95
    },
    "opportunities": [...]
  }
]
```

---

## 6️⃣ Obtener Audio Específico

```bash
curl -X GET "http://localhost:8000/audios/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

(Reemplaza `1` por el ID del audio que subiste)

---

## 7️⃣ Enviar Mensaje de Chat

```bash
curl -X POST "http://localhost:8000/chat/send" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "content": "¿Cuáles fueron los temas principales?",
    "audio_id": 1
  }'
```

---

## 8️⃣ Obtener Historial de Chat

```bash
curl -X GET "http://localhost:8000/chat/history?limit=50" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 9️⃣ Obtener Historial Completo (Audios + Chat)

```bash
curl -X GET "http://localhost:8000/history/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 🔟 Obtener Resumen del Historial

```bash
curl -X GET "http://localhost:8000/history/summary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Respuesta:**
```json
{
  "total_audios": 5,
  "completed_audios": 4,
  "transcriptions": 4,
  "opportunities": 8,
  "chat_messages": 12
}
```

---

## ❌ Eliminar Audio

```bash
curl -X DELETE "http://localhost:8000/audios/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 🔐 Refrescar Token

```bash
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN_HERE"
  }'
```

---

## 📖 Ver Documentación Interactiva

Abre en tu navegador:
```
http://localhost:8000/docs
```

Aquí puedes:
- Ver todos los endpoints
- Probar directamente
- Ver esquemas y tipos
- Leer descripciones

---

## 💡 Tips para Testing

### Usar Postman (GUI)
1. Descargar Postman: https://www.postman.com/downloads/
2. Importar los ejemplos aquí
3. Obtener token
4. Usar en Authorization

### Usar HTTPie (CLI mejora)
```bash
pip install httpie

http POST http://localhost:8000/auth/login \
  email="test@example.com" \
  password="SecurePass123"
```

### Usar VS Code REST Client
1. Instalar extensión: REST Client
2. Crear archivo `test.http`
3. Copiar ejemplos
4. Click "Send Request"

---

## 🧪 Workflow Completo de Testing

```bash
# 1. Registrar
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{...}' | jq -r '.access_token')

# 2. Obtener usuario
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 3. Subir audio
curl -X POST "http://localhost:8000/audios/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@audio.mp3"

# 4. Esperar transcripción (2-30 segundos)
sleep 5

# 5. Listar audios
curl -X GET "http://localhost:8000/audios/" \
  -H "Authorization: Bearer $TOKEN"

# 6. Chat
curl -X POST "http://localhost:8000/chat/send" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "Resumen", "audio_id": 1}'
```

---

## ⚠️ Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Connection refused` | Backend no corre | `uvicorn main:app --reload` |
| `401 Unauthorized` | Token inválido | Obt
ener nuevo token |
| `404 Not Found` | Endpoint incorrecto | Revisar typo en URL |
| `422 Validation Error` | JSON incorrecto | Revisar formato |
| `413 Payload Too Large` | Archivo muy grande | Máx 100MB |

---

## 🎯 Verificación Rápida (1 minuto)

```bash
# Terminal 1: Backend
cd backend && python -m uvicorn main:app --reload

# Terminal 2: Todos estos comandos (copiar/pegar):
curl http://localhost:8000/health
curl http://localhost:8000/
curl http://localhost:8000/docs
```

Si ves respuestas JSON: ✅ **API funciona!**

---

**¡Happy Testing!** 🚀
