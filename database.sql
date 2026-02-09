-- ============================================================================
-- Audio Recording & Opportunity Extraction Platform - Database Schema
-- ============================================================================
-- Supabase/PostgreSQL Database
-- Created: 2025-02-09
-- ============================================================================

-- ============================================================================
-- TABLE: recordings
-- ============================================================================
-- Almacena información de los audios subidos
-- ============================================================================

CREATE TABLE IF NOT EXISTS recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL UNIQUE,
    filepath VARCHAR(500) NOT NULL,
    transcription TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices para búsquedas rápidas
    CONSTRAINT recordings_filename_not_empty CHECK (filename != ''),
    CONSTRAINT recordings_filepath_not_empty CHECK (filepath != '')
);

-- Índices de performance
CREATE INDEX IF NOT EXISTS idx_recordings_filename ON recordings(filename);
CREATE INDEX IF NOT EXISTS idx_recordings_created_at ON recordings(created_at DESC);

-- Comentarios para documentación
COMMENT ON TABLE recordings IS 'Tabla madre: almacena todos los audios subidos al sistema';
COMMENT ON COLUMN recordings.id IS 'UUID único del audio';
COMMENT ON COLUMN recordings.filename IS 'Nombre del archivo (ej: meeting_2025-02-09.wav)';
COMMENT ON COLUMN recordings.filepath IS 'Ruta en Supabase Storage (ej: recordings/meeting_2025-02-09.wav)';
COMMENT ON COLUMN recordings.transcription IS 'Texto completo transcrito del audio';
COMMENT ON COLUMN recordings.created_at IS 'Timestamp de cuando se subió el audio';

---

-- ============================================================================
-- TABLE: transcriptions
-- ============================================================================
-- Almacena transcripciones con versionamiento
-- Permite múltiples idiomas o versiones del mismo audio
-- ============================================================================

CREATE TABLE IF NOT EXISTS transcriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'es',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints de integridad
    CONSTRAINT transcriptions_content_not_empty CHECK (content != ''),
    CONSTRAINT transcriptions_language_valid CHECK (language IN ('es', 'en', 'fr', 'de', 'pt', 'it'))
);

-- Índices de performance
CREATE INDEX IF NOT EXISTS idx_transcriptions_recording_id ON transcriptions(recording_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_created_at ON transcriptions(created_at DESC);

-- Comentarios para documentación
COMMENT ON TABLE transcriptions IS 'Almacena transcripciones de audios (permite múltiples versiones/idiomas por audio)';
COMMENT ON COLUMN transcriptions.id IS 'UUID único de la transcripción';
COMMENT ON COLUMN transcriptions.recording_id IS 'Foreign Key a recordings.id';
COMMENT ON COLUMN transcriptions.content IS 'Texto completo de la transcripción';
COMMENT ON COLUMN transcriptions.language IS 'Idioma detectado (es, en, fr, de, pt, it)';
COMMENT ON COLUMN transcriptions.created_at IS 'Cuándo se transcribió el audio';

---

-- ============================================================================
-- TABLE: opportunities
-- ============================================================================
-- Almacena los tickets de oportunidades extraídas de transcripciones
-- Status y Priority son enums configurables
-- ============================================================================

CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'new',
    priority VARCHAR(50) DEFAULT 'medium',
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints de integridad (sin restricciones en status/priority para máxima flexibilidad)
    CONSTRAINT opportunities_pk PRIMARY KEY (id),
    CONSTRAINT opportunities_recording_id_fkey FOREIGN KEY (recording_id) REFERENCES recordings(id) ON DELETE CASCADE,
    CONSTRAINT opportunities_title_not_empty CHECK (title != ''),
    CONSTRAINT opportunities_description_not_empty CHECK (description != '')
    -- NOTE: status y priority sin CHECK constraint para permitir cualquier valor
    -- Actualiza estos valores según tu aplicación
);

-- Índices de performance
CREATE INDEX IF NOT EXISTS idx_opportunities_recording_id ON opportunities(recording_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_priority ON opportunities(priority);
CREATE INDEX IF NOT EXISTS idx_opportunities_created_at ON opportunities(created_at DESC);

-- Comentarios para documentación
COMMENT ON TABLE opportunities IS 'Tickets de oportunidades extraídas de transcripciones de audio';
COMMENT ON COLUMN opportunities.id IS 'UUID único de la oportunidad/ticket';
COMMENT ON COLUMN opportunities.recording_id IS 'Foreign Key a recordings.id';
COMMENT ON COLUMN opportunities.title IS 'Título breve del ticket (ej: "Presupuesto")';
COMMENT ON COLUMN opportunities.description IS 'Descripción detallada con contexto de la transcripción';
COMMENT ON COLUMN opportunities.status IS 'Estado del ticket: new, in_progress, completed, cancelled';
COMMENT ON COLUMN opportunities.priority IS 'Prioridad: low, medium, high, critical';
COMMENT ON COLUMN opportunities.notes IS 'Notas adicionales del usuario';
COMMENT ON COLUMN opportunities.created_at IS 'Cuándo se creó el ticket';
COMMENT ON COLUMN opportunities.updated_at IS 'Cuándo se actualizó por última vez';

---

-- ============================================================================
-- TABLE: chat_history (OPCIONAL - para persistencia de chat)
-- ============================================================================
-- Almacena el historial de conversaciones con la IA
-- Opcional: solo si quieres persistencia de chat entre sesiones
-- ============================================================================

CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chat_history_role_valid CHECK (role IN ('user', 'assistant')),
    CONSTRAINT chat_history_message_not_empty CHECK (message != '')
);

-- Índices de performance
CREATE INDEX IF NOT EXISTS idx_chat_history_recording_id ON chat_history(recording_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at DESC);

-- Comentarios
COMMENT ON TABLE chat_history IS 'Historial de conversaciones usuario-IA para cada audio (opcional)';
COMMENT ON COLUMN chat_history.role IS 'user (usuario) o assistant (IA Gemini)';
COMMENT ON COLUMN chat_history.message IS 'Contenido del mensaje';

---

-- ============================================================================
-- VISTAS ÚTILES (OPTIONAL)
-- ============================================================================

-- Vista: Oportunidades pendientes por audio
CREATE OR REPLACE VIEW v_pending_opportunities AS
SELECT 
    r.filename,
    COUNT(*) as total_pending,
    STRING_AGG(DISTINCT o.priority, ', ' ORDER BY o.priority) as priorities
FROM recordings r
LEFT JOIN opportunities o ON r.id = o.recording_id AND o.status = 'new'
GROUP BY r.id, r.filename
HAVING COUNT(o.id) > 0
ORDER BY r.created_at DESC;

-- Vista: Estadísticas por estado
CREATE OR REPLACE VIEW v_opportunities_stats AS
SELECT 
    status,
    priority,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM opportunities), 2) as percentage
FROM opportunities
GROUP BY status, priority
ORDER BY status, priority;

-- Vista: Audios sin transcribir
CREATE OR REPLACE VIEW v_untranscribed_recordings AS
SELECT 
    r.id,
    r.filename,
    r.filepath,
    r.created_at,
    COUNT(o.id) as opportunities_waiting
FROM recordings r
LEFT JOIN opportunities o ON r.id = o.recording_id
WHERE r.transcription IS NULL OR r.transcription = ''
GROUP BY r.id, r.filename, r.filepath, r.created_at
ORDER BY r.created_at DESC;

---

-- ============================================================================
-- FUNCIONES ÚTILES (OPTIONAL)
-- ============================================================================

-- Función: Actualizar timestamp de updated_at automáticamente
CREATE OR REPLACE FUNCTION update_opportunities_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Actualizar updated_at en opportunities
CREATE TRIGGER trigger_opportunities_updated_at
BEFORE UPDATE ON opportunities
FOR EACH ROW
EXECUTE FUNCTION update_opportunities_updated_at();

---

-- ============================================================================
-- DATOS DE PRUEBA (OPTIONAL - para desarrollo)
-- ============================================================================
-- Descomenta para cargar datos de ejemplo

/*

-- Insertar audio de prueba
INSERT INTO recordings (filename, filepath, transcription) VALUES (
    'test_meeting_2025-02-09.wav',
    'recordings/test_meeting_2025-02-09.wav',
    'Buenos días, hoy hablaremos sobre el presupuesto para el proyecto. Necesitamos $50,000 
     antes de marzo. También mencionamos a nuestro competidor principal que es Acme Corp. 
     El timeline es antes de fin de trimestre.'
) ON CONFLICT (filename) DO NOTHING;

-- Insertar transcripción
INSERT INTO transcriptions (recording_id, content, language) 
SELECT id, transcription, 'es' FROM recordings WHERE filename = 'test_meeting_2025-02-09.wav'
ON CONFLICT DO NOTHING;

-- Insertar oportunidades de prueba
INSERT INTO opportunities (recording_id, title, description, status, priority, notes)
SELECT 
    id, 
    'Presupuesto $50,000',
    'Cliente menciona necesidad de inversión de $50,000 para el proyecto',
    'new',
    'high',
    'Confirmar monto en próxima llamada'
FROM recordings WHERE filename = 'test_meeting_2025-02-09.wav'
ON CONFLICT DO NOTHING;

INSERT INTO opportunities (recording_id, title, description, status, priority, notes)
SELECT 
    id,
    'Timeline: Fin de Trimestre',
    'Proyecto debe estar completado antes de fin del trimestre (marzo 2025)',
    'in_progress',
    'high',
    'Agendar reunión de seguimiento'
FROM recordings WHERE filename = 'test_meeting_2025-02-09.wav'
ON CONFLICT DO NOTHING;

INSERT INTO opportunities (recording_id, title, description, status, priority, notes)
SELECT 
    id,
    'Competidor: Acme Corp',
    'Cliente menciona a Acme Corp como competidor directo en el espacio',
    'new',
    'medium',
    'Investigar posicionamiento competitivo'
FROM recordings WHERE filename = 'test_meeting_2025-02-09.wav'
ON CONFLICT DO NOTHING;

*/

---

-- ============================================================================
-- INFORMACIÓN DE LA BASE DE DATOS
-- ============================================================================

/*

ESTRUCTURA FINAL:

1. recordings (tabla madre)
   ├── id (UUID PK)
   ├── filename (VARCHAR, UNIQUE)
   ├── filepath (VARCHAR)
   ├── transcription (TEXT, nullable)
   ├── created_at (TIMESTAMP)

2. transcriptions (permite versionamiento multi-idioma)
   ├── id (UUID PK)
   ├── recording_id (UUID FK → recordings)
   ├── content (TEXT)
   ├── language (VARCHAR, enum)
   ├── created_at (TIMESTAMP)

3. opportunities (tickets extraídos)
   ├── id (UUID PK)
   ├── recording_id (UUID FK → recordings)
   ├── title (VARCHAR)
   ├── description (TEXT)
   ├── status (VARCHAR, enum)
   ├── priority (VARCHAR, enum)
   ├── notes (TEXT)
   ├── created_at (TIMESTAMP)
   ├── updated_at (TIMESTAMP)

4. chat_history (OPTIONAL - historial de chat)
   ├── id (UUID PK)
   ├── recording_id (UUID FK → recordings)
   ├── role (VARCHAR, enum: user|assistant)
   ├── message (TEXT)
   ├── created_at (TIMESTAMP)

RELACIONES:
- recordings 1-to-many transcriptions (CASCADE DELETE)
- recordings 1-to-many opportunities (CASCADE DELETE)
- recordings 1-to-many chat_history (CASCADE DELETE)

ENUMS (SIN CONSTRAINTS - FLEXIBLES):
- opportunities.status: Cualquier valor (ej: 'new', 'Open', 'won', 'in_progress', etc.)
- opportunities.priority: Cualquier valor (ej: 'low', 'medium', 'high', 'critical', 'Low', 'High', etc.)
- transcriptions.language: 'es' | 'en' | 'fr' | 'de' | 'pt' | 'it'
- chat_history.role: 'user' | 'assistant'

NOTA: status y priority NO tienen CHECK constraints para máxima flexibilidad.
      Si necesitas validación, hazla en la aplicación (Python/Streamlit).

VISTAS:
- v_pending_opportunities: oportunidades sin resolver
- v_opportunities_stats: estadísticas por estado/prioridad
- v_untranscribed_recordings: audios sin transcripciones

*/

-- ============================================================================
-- FIN DE SCHEMA
-- ============================================================================
