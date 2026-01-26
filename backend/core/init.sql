CREATE TABLE users (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    nickname TEXT NOT NULL,
    avatar_url TEXT
);

CREATE TABLE chats (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    last_message_text TEXT DEFAULT '_Чат создан_',
    last_message_time TIMESTAMP DEFAULT now(),
    last_message_author INT DEFAULT 0,
    permissions JSONB DEFAULT '{}'::JSONB
);