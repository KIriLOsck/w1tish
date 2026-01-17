CREATE TABLE users (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE users_data (
    id INT PRIMARY KEY,
    nickname TEXT NOT NULL,
    avatar_url TEXT,
    chats JSONB DEFAULT '[]'::JSONB,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);