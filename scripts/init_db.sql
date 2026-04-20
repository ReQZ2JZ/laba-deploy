CREATE TABLE IF NOT EXISTS video_cards (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

TRUNCATE video_cards RESTART IDENTITY;

INSERT INTO video_cards (name, price, description, created_at) VALUES
('RTX 5090', 230000.00, 'Флагман', NOW()),
('RTX 4090', 165000.00, 'Мощная', NOW()),
('RTX 5080', 130000.00, '4K', NOW());