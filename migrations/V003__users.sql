CREATE SEQUENCE users_seq START 101;

CREATE TABLE IF NOT EXISTS userstable (
    user_id bigint PRIMARY KEY,
    username TEXT,
    password TEXT
);
