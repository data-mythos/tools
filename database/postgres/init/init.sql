-- Create tables for users, posts, and followers

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Posts Table
CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INT DEFAULT 0
);

-- Create Followers Table
CREATE TABLE IF NOT EXISTS followers (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    follower_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    follow_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, follower_id)
);

-- Insert Sample Data into Users Table
INSERT INTO users (username, email, full_name)
VALUES
('john_doe', 'john@example.com', 'John Doe'),
('jane_smith', 'jane@example.com', 'Jane Smith'),
('alice_jones', 'alice@example.com', 'Alice Jones'),
('bob_martin', 'bob@example.com', 'Bob Martin');

-- Insert Sample Data into Posts Table
INSERT INTO posts (user_id, content, likes)
VALUES
((SELECT user_id FROM users WHERE username = 'john_doe'), 'Hello, this is my first post!', 10),
((SELECT user_id FROM users WHERE username = 'jane_smith'), 'Just joined this platform!', 5),
((SELECT user_id FROM users WHERE username = 'alice_jones'), 'Loving the new features!', 3),
((SELECT user_id FROM users WHERE username = 'bob_martin'), 'Hey everyone!', 8);

-- Insert Sample Data into Followers Table
INSERT INTO followers (user_id, follower_id)
VALUES
((SELECT user_id FROM users WHERE username = 'john_doe'), (SELECT user_id FROM users WHERE username = 'jane_smith')),
((SELECT user_id FROM users WHERE username = 'jane_smith'), (SELECT user_id FROM users WHERE username = 'john_doe')),
((SELECT user_id FROM users WHERE username = 'alice_jones'), (SELECT user_id FROM users WHERE username = 'john_doe')),
((SELECT user_id FROM users WHERE username = 'bob_martin'), (SELECT user_id FROM users WHERE username = 'alice_jones'));

-- Create Admin Role and Grant Privileges
CREATE ROLE admin_role LOGIN PASSWORD 'adminpassword';
GRANT ALL PRIVILEGES ON DATABASE social_media TO admin_role;

-- Assign Admin Role to the Admin User
ALTER USER admin WITH SUPERUSER;
