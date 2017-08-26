DROP TABLE IF EXISTS sequences;

CREATE TABLE sequences (
  id BIGSERIAL PRIMARY KEY,
  sequence_id VARCHAR(255) NOT NULL UNIQUE,
  updater VARCHAR(36) NOT NULL UNIQUE,
  current_value BIGINT NOT NULL DEFAULT 0,
  start_value BIGINT NOT NULL DEFAULT 1,
  range_size BIGINT,
  alert_threshold REAL,

  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
