# 🎙️ AppGrabacionAudio - Sistema de Grabación y Gestión de Reuniones

<div align="center">

**Una plataforma completa para grabar, transcribir e inteligentemente analizar reuniones y conversaciones con IA**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Supabase](https://img.shields.io/badge/Supabase-Database-green)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-yellow)

</div>

---

## 📋 Descripción General

**AppGrabacionAudio** es un sistema integral para la gestión de reuniones que permite:

✅ Grabar y gestionar audios desde el micrófono o subir archivos  
✅ Renombrar audios directamente desde la interfaz  
✅ Transcribir automáticamente con **diarización inteligente** (identifica quién habla)  
✅ Consultar un **Asistente IA** sobre el contenido de las reuniones  
✅ Gestionar **tickets y oportunidades de negocio** generadas desde transcripciones  
✅ Almacenamiento seguro en la nube con Supabase  
✅ Interfaz moderna y responsiva con Streamlit  

---

## 🎯 Características Principales

### 🎤 Grabación de Audio
- **Grabación en vivo** desde tu micrófono
- **Subida de archivos** en formatos: MP3, WAV, M4A
- **Validación automática** de archivos
- Almacenamiento en **Supabase Storage**

### ✏️ Gestión de Audios
- **Renombrar audios** inline directamente en la interfaz
- Edición en tiempo real con confirmación y cancelación
- **Sincronización automática** con Supabase
- Búsqueda y paginación inteligente de grabaciones

### 🗣️ Transcripción Inteligente
- Transcripción automática con **Google Gemini**
- **Diarización avanzada**: Identifica automáticamente cada hablante
- **Identificación deductiva de nombres**: Si alguien dice "Hola María", reconoce que María es un participante
- Formato limpio y profesional:
  ```
  Jorge: "Hola a todos, ¿qué tal?"
  María: "Bien, bien. ¿Y tú?"
  Voz 3: "Todo correcto."
  ```

### 🤖 Asistente IA
- **Chatbot inteligente** basado en GPT para analizar transcripciones
- Haz preguntas sobre el contenido de tus reuniones
- Extrae información clave automáticamente
- Respuestas contextuales basadas en el audio transcrito

### 🎫 Gestión de Tickets
- **Sistema de oportunidades de negocio** automático
- Crear tickets desde transcripciones
- Estados: Open, In Progress, Closed
- Niveles de prioridad: High, Medium, Low
- Paginación inteligente con navegación por números de página

### 💾 Almacenamiento en la Nube
- **Base de datos Supabase** para metadatos
- **Storage Supabase** para archivos de audio
- Sincronización automática de cambios
- Respaldo seguro de tus grabaciones

---

## 💼 Casos de Uso Reales

### 🏛️ Caso 1: Administración Municipal - Gestión de Reuniones

**Escenario:**
Un ayuntamiento necesita administrar y documentar sus reuniones de forma eficiente, manteniendo un control perfecto de los temas importantes y decisiones tomadas.

**Solución:**

1. **Grabación automática de reuniones**
   - Inicia una grabación cuando comienza la reunión en el salón de acuerdos
   - La app captura todos los participantes (Alcalde, Concejales, Secretario, etc.)

2. **Identificación automática de participantes**
   - La aplicación identifica automáticamente quién habla en cada momento
   ```
   Alcalde: "Buenos días a todos, necesitamos hablar del presupuesto de 2026"
   Concejal García: "De acuerdo, primero debemos revisar las partidas principales"
   Secretaria Rosa: "Tengo el documento listo para compartir"
   ```

3. **Generación automática de tickets por palabras clave**
   - Define palabras clave específicas: **"presupuesto"**, **"gasto"**, **"aprobado"**, **"acuerdo"**, **"acción"**
   - Cuando estas palabras se mencionan en la reunión, automáticamente se crea un ticket con:
     - El contexto completo de lo dicho
     - Quién lo mencionó
     - El momento de la reunión
   
   **Ejemplo:**
   ```
   ✓ Ticket creado: "Presupuesto 2026"
   Prioridad: HIGH
   Mencionado por: Alcalde
   Contexto: "Buenos días a todos, necesitamos hablar del presupuesto de 2026"
   ```

4. **Asistente IA para información rápida**
   - Pregunta: "¿Qué temas de presupuesto se discutieron?"
   - IA responde: "Se discutieron las siguientes partidas: sanidad, educación, infraestructuras..."
   
   - Pregunta: "¿Qué decisión tomó el concejal García sobre el gasto?"
   - IA responde: "El concejal García propuso reducir el gasto en..."

**Beneficios:**
- ✅ **Documentación automática** - No necesitas tomar notas manualmente
- ✅ **Trazabilidad** - Sabes exactamente quién dijo qué y cuándo
- ✅ **Ticket control** - Todos los temas importantes generados automáticamente
- ✅ **Búsqueda fácil** - Pregunta al IA sobre decisiones pasadas
- ✅ **Legal** - Registro completo de reuniones para auditoría

---

### 🎓 Caso 2: Formador Técnico - Captura de Oportunidades de Negocio

**Escenario:**
Un formador técnico imparte cursos y formaciones, pero durante las sesiones se entera de oportunidades de negocio (empresas que necesitan formación, consultorías, etc.) y quiere capturarlas automáticamente.

**Solución:**

1. **Grabación de sesiones de formación**
   - Graba toda la sesión de formación (ejemplo: "Ciberseguridad para empresas")
   - Participantes: Formador, Juan (alumno empresa A), María (alumno empresa B), Carlos (decisor empresa C)

2. **Identificación inteligente de participantes**
   ```
   Formador: "Buenos días, hoy veremos ciberseguridad avanzada"
   Juan: "Esto es crucial para nuestra empresa A, tenemos muchos clientes"
   Formador: "Excelente Juan, ¿y tú María, cómo lo ves desde empresa B?"
   María: "Nuestro equipo definitivamente necesita capacitación en esto"
   Carlos: "Estaría interesado en una formación customizada para mi organización"
   ```

3. **Generación automática de oportunidades por palabra clave**
   - Define la palabra clave: **"formación"** (o variantes: "capacitación", "entrenamiento", "curso")
   - Sistema automáticamente busca dónde se menciona **"formación"** en la transcripción
   - Genera tickets de oportunidad para CADA mención con nombres identificados

   **Tickets generados automáticamente:**
   ```
   🎫 TICKET 1: "Formación Ciberseguridad - Empresa A"
   Mencionado por: Juan
   Contexto: "Esto es crucial para nuestra empresa A, tenemos muchos clientes"
   Prioridad: HIGH
   Estado: OPEN
   
   🎫 TICKET 2: "Capacitación Seguridad - Empresa B"
   Mencionado por: María  
   Contexto: "Nuestro equipo definitivamente necesita capacitación en esto"
   Prioridad: MEDIUM
   Estado: OPEN
   
   🎫 TICKET 3: "Formación Customizada"
   Mencionado por: Carlos
   Contexto: "Estaría interesado en una formación customizada para mi organización"
   Prioridad: HIGH
   Estado: OPEN
   ```

4. **Seguimiento de oportunidades**
   - Ves todos los tickets generados
   - Cambias el estado a "In Progress" cuando contactas a Juan/María/Carlos
   - Cambias a "Closed" cuando cierras la venta

5. **Análisis mediante IA**
   - Pregunta: "¿Cuántas oportunidades de formación surgieron?"
   - IA responde: "Se encontraron 3 oportunidades de formación durante la sesión..."
   
   - Pregunta: "¿Quién mencionó la palabra formación?"
   - IA responde: "Juan de Empresa A, María de Empresa B, y Carlos..."

**Beneficios:**
- ✅ **Captura automática** - No pierdes ninguna oportunidad
- ✅ **Identificación clara** - Sabes exactamente quién es cada contacto
- ✅ **Contexto completo** - Qué dijeron exactamente sobre formación
- ✅ **Pipeline automático** - Tickets listos para seguimiento
- ✅ **Escalabilidad** - Graba N sesiones y todas generan oportunidades automáticamente

---

### 🔑 El Factor Diferenciador: Diarización con Nombres

**¿Por qué esto es importante en ambos casos?**

Sin diarización inteligente obtendrías:
```
❌ "Buenos días, necesitamos hablar del presupuesto... de acuerdo, primero debemos revisar... tengo el documento listo"
(Todo masticado, no sabes quién dijo qué)
```

Con diarización inteligente obtienes:
```
✅ Alcalde: "Buenos días a todos, necesitamos hablar del presupuesto"
✅ Concejal García: "De acuerdo, primero debemos revisar las partidas principales"
✅ Secretaria Rosa: "Tengo el documento listo para compartir"
```

**Esto permite:**
- Responsabilidad individual
- Seguimiento a personas específicas
- Análisis por participante
- Documentación legal
- Tickets vinculados a personas reales

---



### Frontend
- **Streamlit** - Framework para interfaz web interactiva
- **HTML/CSS** - Estilos glassmorphism personalizados
- **Python 3.10+** - Lenguaje principal

### Backend
- **Python** - Lógica de negocio
- **Google Generative AI (Gemini)** - Transcripción y análisis inteligente
- **Supabase** - Base de datos PostgreSQL + Storage
- **Supabase Python Client** - Integración con base de datos

### Arquitectura
```
appGrabacionAudio/
├── frontend/
│   ├── index.py              # Aplicación principal Streamlit
│   ├── AudioRecorder.py      # Gestor de grabaciones
│   ├── components.py         # Componentes reutilizables
│   ├── styles.py             # Estilos CSS
│   ├── notifications.py      # Notificaciones y alertas
│   ├── performance.py        # Optimizaciones y caché
│   └── utils.py              # Funciones auxiliares
├── backend/
│   ├── Transcriber.py        # Transcripción con Gemini
│   ├── Model.py              # Chat IA (GPT)
│   ├── OpportunitiesManager.py # Gestión de tickets
│   ├── database.py           # Operaciones CRUD Supabase
│   └── helpers.py            # Utilidades compartidas
├── config.py                 # Configuración y constantes
├── logger.py                 # Sistema de logging
├── requirements.txt          # Dependencias Python
└── streamlit_app.py          # Punto de entrada
```

---

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.10 o superior
- Cuenta en Supabase
- API Key de Google Gemini
- Cuenta para Chat IA (OpenAI o similar)

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/appGrabacionAudio.git
cd appGrabacionAudio
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # macOS/Linux
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear archivo `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "tu-url-supabase"
SUPABASE_KEY = "tu-key-supabase"
GEMINI_API_KEY = "tu-api-key-gemini"
OPENAI_API_KEY = "tu-api-key-openai"
```

5. **Ejecutar la aplicación**
```bash
streamlit run streamlit_app.py
```

---

## 📖 Guía de Uso

### 1️⃣ Grabar o Subir Audio
- **Grabadora en vivo**: Usa tu micrófono para grabar directamente
- **Subir archivo**: Selecciona un archivo MP3, WAV o M4A
- Los archivos se guardan automáticamente en Supabase

### 2️⃣ Renombrar Audios
1. Ve a la pestaña **"Audios guardados"**
2. Haz clic en el lápiz **✏️** del audio que deseas renombrar
3. Edita el nombre directamente en la línea
4. Presiona **✓** para confirmar o **✕** para cancelar
5. El cambio se sincroniza automáticamente con Supabase

### 3️⃣ Transcribir Audio
1. Ve a la pestaña **"Transcribir"**
2. Selecciona un audio de la lista
3. Presiona **"Transcribir"**
4. Espera a que Gemini procese el audio
5. Verás la transcripción con los hablantes identificados

### 4️⃣ Chatear con el Asistente IA
1. Después de transcribir, aparece el panel de chat
2. Haz preguntas sobre el contenido de la reunión
3. El IA responde basándose en la transcripción

### 5️⃣ Gestionar Tickets
1. Ve a la pestaña **"Gestión en lote"** (en la sección derecha)
2. Crea tickets desde transcripciones
3. Establece prioridad y estado
4. Navega entre pages con los números de página

---

## 🔄 Flujo de Diarización

El sistema identifica automáticamente quién habla en cada momento:

**Ejemplo de entrada de audio:**
```
Persona 1: "Hola María, ¿cómo estás?"
Persona 1: "¿Viste el email que envié?"
Persona 2: "Sí, lo vi. Muy bien."
```

**Transcripción generada:**
```
Jorge: "Hola María, ¿cómo estás?"
Jorge: "¿Viste el email que envié?"
María: "Sí, lo vi. Muy bien."
```

El sistema **reconoce automáticamente** que María es la segunda voz porque fue mencionada en la conversación.

---

## 🔐 Seguridad

- ✅ Autenticación segura con Supabase
- ✅ Encriptación de datos en tránsito
- ✅ Sin almacenamiento local de credenciales
- ✅ Acceso controlado a la base de datos
- ✅ Logs de auditoría de operaciones

---

## 📊 Base de Datos (Supabase)

### Tablas principales

**recordings**
```
id: UUID
filename: String
filepath: String
created_at: Timestamp
updated_at: Timestamp
user_id: UUID (referencia a usuario)
```

**transcriptions**
```
id: UUID
recording_id: UUID (referencia a recording)
content: Text
language: String (default: 'es')
created_at: Timestamp
updated_at: Timestamp
```

**opportunities**
```
id: UUID
recording_id: UUID
title: String
description: Text
priority: String (high/medium/low)
status: String (open/progress/closed)
created_at: Timestamp
updated_at: Timestamp
```

---

## 🎨 Interfaz

- **Diseño Glassmorphism**: Moderna y elegante
- **Tema oscuro**: Cómodo para sesiones prolongadas
- **Responsivo**: Funciona en desktop y tablet
- **Components reutilizables**: Código limpio y mantenible

---

## 📦 Dependencias Principales

```
streamlit>=1.28.0           # Framework web
supabase>=2.0.0             # Base de datos
google-generativeai>=0.3.0  # Gemini AI
openai>=1.0.0               # ChatGPT
python-dotenv>=1.0.0        # Variables de entorno
```

Ver `requirements.txt` para lista completa.

---

## 🐛 Troubleshooting

### Error: "Credenciales de Supabase no configuradas"
- Verifica que `secrets.toml` esté en `.streamlit/`
- Comprueba que las claves sean correctas

### Error: "Archivo no encontrado"
- Los archivos se descargan automáticamente desde Storage
- Verifica que tengas conexión a internet

### Transcripción lenta
- Los audios largos tardan más en procesarse
- Utiliza audios de máximo 30 minutos para mejor rendimiento

---

## 🚀 Mejoras Futuras

- [ ] Exportar transcripciones a PDF
- [ ] Integración con Google Calendar
- [ ] Notificaciones por email
- [ ] Análisis de sentimiento
- [ ] Soporte para múltiples idiomas
- [ ] SDK para terceras aplicaciones
- [ ] Análisis de palabras clave automático

---

## 👨‍💼 Autor

Desarrollado con ❤️ para mejorar la gestión de reuniones y toma de notas.

---

## 📝 Licencia

MIT License - Siéntete libre de usar este proyecto

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

Si encuentras problemas o tienes preguntas, abre un issue en el repositorio.

---

<div align="center">

**¡Transforma tu forma de gestionar reuniones!** 🚀

[⬆ Volver arriba](#-appgrabacionaudio---sistema-de-grabación-y-gestión-de-reuniones)

</div>
