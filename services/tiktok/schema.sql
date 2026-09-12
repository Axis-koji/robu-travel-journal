PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS oauth_states (
  state_hash TEXT PRIMARY KEY,
  expires INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS oauth_expiry ON oauth_states(expires);
CREATE TABLE IF NOT EXISTS accounts (
  open_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  sealed_tokens TEXT NOT NULL,
  lock_id TEXT NOT NULL DEFAULT '',
  lock_until INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sessions (
  session_hash TEXT PRIMARY KEY,
  open_id TEXT NOT NULL REFERENCES accounts(open_id) ON DELETE CASCADE,
  csrf TEXT NOT NULL,
  expires INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS session_expiry ON sessions(expires);
CREATE INDEX IF NOT EXISTS session_account ON sessions(open_id);
CREATE TABLE IF NOT EXISTS uploads (
  open_id TEXT NOT NULL REFERENCES accounts(open_id) ON DELETE CASCADE,
  article_id TEXT NOT NULL,
  publish_id TEXT,
  status TEXT NOT NULL,
  created INTEGER NOT NULL,
  checked INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(open_id, article_id)
);
