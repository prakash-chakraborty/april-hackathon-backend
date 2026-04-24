CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);

CREATE TABLE IF NOT EXISTS pages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_pages_id ON pages (id);

CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    page_id INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    metric_title VARCHAR(200) NOT NULL,
    metric_value VARCHAR(200) NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_cards_id ON cards (id);
CREATE INDEX IF NOT EXISTS ix_cards_page_id ON cards (page_id);
