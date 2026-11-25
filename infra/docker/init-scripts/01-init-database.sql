-- ClipYantra Database Initialization Script
-- This script runs on first PostgreSQL container startup

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- Create application user (if not using default postgres)
-- DO $$
-- BEGIN
--     IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'clipyantra') THEN
--         CREATE ROLE clipyantra WITH LOGIN PASSWORD 'clipyantra_dev';
--     END IF;
-- END
-- $$;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE clipyantra TO clipyantra;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO clipyantra;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO clipyantra;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO clipyantra;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO clipyantra;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS clipyantra;
CREATE SCHEMA IF NOT EXISTS analytics;

GRANT ALL ON SCHEMA clipyantra TO clipyantra;
GRANT ALL ON SCHEMA analytics TO clipyantra;

-- Set search path
ALTER DATABASE clipyantra SET search_path = clipyantra, public;

-- Create enum types
CREATE TYPE clipyantra.media_status AS ENUM (
    'pending',
    'validating',
    'validated',
    'processing',
    'completed',
    'failed',
    'archived'
);

CREATE TYPE clipyantra.task_status AS ENUM (
    'pending',
    'queued',
    'running',
    'completed',
    'failed',
    'cancelled',
    'retrying'
);

CREATE TYPE clipyantra.transcription_status AS ENUM (
    'pending',
    'processing',
    'completed',
    'failed'
);

CREATE TYPE clipyantra.render_status AS ENUM (
    'pending',
    'queued',
    'rendering',
    'completed',
    'failed'
);

CREATE TYPE clipyantra.analysis_type AS ENUM (
    'scene_detection',
    'face_detection',
    'content_classification',
    'nsfw_detection',
    'audio_analysis',
    'speech_detection'
);

-- Core tables
CREATE TABLE IF NOT EXISTS clipyantra.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS clipyantra.projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS clipyantra.media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES clipyantra.projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    media_type VARCHAR(20) NOT NULL, -- video, audio, image
    status clipyantra.media_status DEFAULT 'pending',
    duration_seconds DOUBLE PRECISION,
    width INTEGER,
    height INTEGER,
    frame_rate DOUBLE PRECISION,
    video_codec VARCHAR(50),
    audio_codec VARCHAR(50),
    bitrate BIGINT,
    metadata JSONB DEFAULT '{}',
    thumbnails JSONB DEFAULT '[]',
    proxy_path TEXT,
    sprite_path TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS clipyantra.transcriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    media_id UUID NOT NULL REFERENCES clipyantra.media(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    status clipyantra.transcription_status DEFAULT 'pending',
    language VARCHAR(10),
    model VARCHAR(50) DEFAULT 'base',
    segments JSONB DEFAULT '[]',
    full_text TEXT,
    word_timestamps JSONB DEFAULT '[]',
    confidence DOUBLE PRECISION,
    diarization JSONB DEFAULT '[]',
    error_message TEXT,
    processing_time_seconds DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS clipyantra.tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES clipyantra.projects(id) ON DELETE SET NULL,
    user_id UUID REFERENCES clipyantra.users(id) ON DELETE SET NULL,
    media_id UUID REFERENCES clipyantra.media(id) ON DELETE SET NULL,
    task_type VARCHAR(50) NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    status clipyantra.task_status DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    payload JSONB DEFAULT '{}',
    result JSONB DEFAULT '{}',
    error_message TEXT,
    progress INTEGER DEFAULT 0,
    celery_task_id VARCHAR(255),
    retries INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS clipyantra.analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    media_id UUID NOT NULL REFERENCES clipyantra.media(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    analysis_type clipyantra.analysis_type NOT NULL,
    status clipyantra.task_status DEFAULT 'pending',
    result JSONB DEFAULT '{}',
    confidence DOUBLE PRECISION,
    model VARCHAR(100),
    parameters JSONB DEFAULT '{}',
    error_message TEXT,
    processing_time_seconds DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS clipyantra.renders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES clipyantra.projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    timeline JSONB NOT NULL DEFAULT '{}',
    preset VARCHAR(100) DEFAULT 'social_1080p',
    status clipyantra.render_status DEFAULT 'pending',
    output_path TEXT,
    output_url TEXT,
    file_size BIGINT,
    duration_seconds DOUBLE PRECISION,
    width INTEGER,
    height INTEGER,
    fps INTEGER,
    video_codec VARCHAR(50),
    audio_codec VARCHAR(50),
    bitrate BIGINT,
    error_message TEXT,
    progress INTEGER DEFAULT 0,
    celery_task_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS clipyantra.clips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES clipyantra.projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    render_id UUID REFERENCES clipyantra.renders(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source_media_id UUID REFERENCES clipyantra.media(id) ON DELETE SET NULL,
    start_time DOUBLE PRECISION NOT NULL,
    end_time DOUBLE PRECISION NOT NULL,
    duration_seconds DOUBLE PRECISION NOT NULL,
    output_path TEXT,
    output_url TEXT,
    file_size BIGINT,
    status clipyantra.render_status DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Analytics tables
CREATE TABLE IF NOT EXISTS analytics.daily_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    user_id UUID REFERENCES clipyantra.users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES clipyantra.projects(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    dimensions JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(date, user_id, project_id, metric_name)
);

CREATE TABLE IF NOT EXISTS analytics.events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES clipyantra.users(id) ON DELETE SET NULL,
    project_id UUID REFERENCES clipyantra.projects(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    session_id VARCHAR(255),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_media_project_id ON clipyantra.media(project_id);
CREATE INDEX IF NOT EXISTS idx_media_user_id ON clipyantra.media(user_id);
CREATE INDEX IF NOT EXISTS idx_media_status ON clipyantra.media(status);
CREATE INDEX IF NOT EXISTS idx_media_created_at ON clipyantra.media(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_media_file_path ON clipyantra.media USING GIN (file_path gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_transcriptions_media_id ON clipyantra.transcriptions(media_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_user_id ON clipyantra.transcriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_status ON clipyantra.transcriptions(status);

CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON clipyantra.tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON clipyantra.tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_media_id ON clipyantra.tasks(media_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON clipyantra.tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_celery_task_id ON clipyantra.tasks(celery_task_id);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON clipyantra.tasks(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_analyses_media_id ON clipyantra.analyses(media_id);
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON clipyantra.analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_type ON clipyantra.analyses(analysis_type);
CREATE INDEX IF NOT EXISTS idx_analyses_status ON clipyantra.analyses(status);

CREATE INDEX IF NOT EXISTS idx_renders_project_id ON clipyantra.renders(project_id);
CREATE INDEX IF NOT EXISTS idx_renders_user_id ON clipyantra.renders(user_id);
CREATE INDEX IF NOT EXISTS idx_renders_status ON clipyantra.renders(status);

CREATE INDEX IF NOT EXISTS idx_clips_project_id ON clipyantra.clips(project_id);
CREATE INDEX IF NOT EXISTS idx_clips_user_id ON clipyantra.clips(user_id);
CREATE INDEX IF NOT EXISTS idx_clips_render_id ON clipyantra.clips(render_id);

CREATE INDEX IF NOT EXISTS idx_daily_metrics_date ON analytics.daily_metrics(date DESC);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_user_id ON analytics.daily_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_project_id ON analytics.daily_metrics(project_id);

CREATE INDEX IF NOT EXISTS idx_events_user_id ON analytics.events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_project_id ON analytics.events(project_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON analytics.events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON analytics.events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_session_id ON analytics.events(session_id);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION clipyantra.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON clipyantra.users
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON clipyantra.projects
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_media_updated_at BEFORE UPDATE ON clipyantra.media
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_transcriptions_updated_at BEFORE UPDATE ON clipyantra.transcriptions
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON clipyantra.tasks
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON clipyantra.analyses
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_renders_updated_at BEFORE UPDATE ON clipyantra.renders
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

CREATE TRIGGER update_clips_updated_at BEFORE UPDATE ON clipyantra.clips
    FOR EACH ROW EXECUTE FUNCTION clipyantra.update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE clipyantra.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.media ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.renders ENABLE ROW LEVEL SECURITY;
ALTER TABLE clipyantra.clips ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY users_own_data ON clipyantra.users
    FOR ALL USING (id = current_user_id());

CREATE POLICY projects_own_data ON clipyantra.projects
    FOR ALL USING (user_id = current_user_id());

CREATE POLICY media_own_data ON clipyantra.media
    FOR ALL USING (user_id = current_user_id());

CREATE POLICY transcriptions_own_data ON clipyantra.transcriptions
    FOR ALL USING (user_id = current_user_id());

CREATE POLICY tasks_own_data ON clipyantra.tasks
    FOR ALL USING (user_id = current_user_id());

CREATE POLICY analyses_own_data ON clipyantra.analyses
    FOR ALL USING (user_id = current_user_id());

CREATE POLICY renders_own_data ON clipyantra.renders
    FOR ALL USING (user_id = current_user_id());

CREATE POLICY clips_own_data ON clipyantra.clips
    FOR ALL USING (user_id = current_user_id());

-- Function to get current user ID from session variable
CREATE OR REPLACE FUNCTION clipyantra.current_user_id()
RETURNS UUID AS $$
DECLARE
    user_id UUID;
BEGIN
    -- Try to get from session variable (set by application)
    SELECT current_setting('app.current_user_id', true)::UUID INTO user_id;
    RETURN user_id;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute on function
GRANT EXECUTE ON FUNCTION clipyantra.current_user_id() TO clipyantra;

-- Comments
COMMENT ON TABLE clipyantra.users IS 'Application users';
COMMENT ON TABLE clipyantra.projects IS 'User projects';
COMMENT ON TABLE clipyantra.media IS 'Uploaded media files';
COMMENT ON TABLE clipyantra.transcriptions IS 'Speech-to-text transcriptions';
COMMENT ON TABLE clipyantra.tasks IS 'Background task tracking';
COMMENT ON TABLE clipyantra.analyses IS 'Media analysis results';
COMMENT ON TABLE clipyantra.renders IS 'Video rendering jobs';
COMMENT ON TABLE clipyantra.clips IS 'Generated clips';
COMMENT ON TABLE analytics.daily_metrics IS 'Aggregated daily metrics';
COMMENT ON TABLE analytics.events IS 'User event tracking';