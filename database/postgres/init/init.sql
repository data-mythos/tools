-- Create social media database
CREATE DATABASE IF NOT EXISTS social_media;

-- Switch to the database
USE social_media;

-- Create users table
CREATE TABLE IF NOT EXISTS users
(
    user_id UUID DEFAULT generateUUIDv4(),
    username String,
    email String,
    full_name String,
    created_at DateTime DEFAULT now(),
    last_login DateTime DEFAULT now(),
    is_active UInt8 DEFAULT 1
) ENGINE = MergeTree()
ORDER BY (user_id);

-- Create posts table
CREATE TABLE IF NOT EXISTS posts
(
    post_id UUID DEFAULT generateUUIDv4(),
    user_id UUID,
    content String,
    created_at DateTime DEFAULT now(),
    likes UInt32 DEFAULT 0,
    shares UInt32 DEFAULT 0,
    is_deleted UInt8 DEFAULT 0
) ENGINE = MergeTree()
ORDER BY (created_at, user_id);

-- Create comments table
CREATE TABLE IF NOT EXISTS comments
(
    comment_id UUID DEFAULT generateUUIDv4(),
    post_id UUID,
    user_id UUID,
    content String,
    created_at DateTime DEFAULT now(),
    likes UInt32 DEFAULT 0,
    is_deleted UInt8 DEFAULT 0
) ENGINE = MergeTree()
ORDER BY (created_at, post_id);

-- Insert sample users
INSERT INTO users (username, email, full_name) VALUES
    ('john_doe', 'john@example.com', 'John Doe'),
    ('jane_smith', 'jane@example.com', 'Jane Smith'),
    ('bob_wilson', 'bob@example.com', 'Bob Wilson'),
    ('alice_brown', 'alice@example.com', 'Alice Brown'),
    ('charlie_davis', 'charlie@example.com', 'Charlie Davis');

-- Insert sample posts
INSERT INTO posts (user_id, content, likes, shares)
SELECT
    user_id,
    multiIf(
        username = 'john_doe', 'Just had an amazing weekend! #blessed',
        username = 'jane_smith', 'New project starting today! #excited',
        username = 'bob_wilson', 'Check out my new photo collection',
        username = 'alice_brown', 'Great meeting with the team today',
        'Beautiful sunset at the beach #nature'
    ),
    rand() % 100,
    rand() % 20
FROM users;

-- Insert sample comments
INSERT INTO comments (post_id, user_id, content, likes)
SELECT
    post_id,
    (SELECT user_id FROM users ORDER BY rand() LIMIT 1),
    multiIf(
        rand() % 5 = 0, 'Great post!',
        rand() % 5 = 1, 'Thanks for sharing!',
        rand() % 5 = 2, 'Awesome content!',
        rand() % 5 = 3, 'Looking forward to more!',
        'This is amazing!'
    ),
    rand() % 50
FROM posts
WHERE rand() % 2 = 1;

-- Create materialized view for post analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS post_analytics
ENGINE = SummingMergeTree()
ORDER BY (created_date, user_id)
AS SELECT
    toDate(created_at) as created_date,
    user_id,
    count() as total_posts,
    sum(likes) as total_likes,
    sum(shares) as total_shares
FROM posts
GROUP BY created_date, user_id;

-- Create materialized view for user engagement
CREATE MATERIALIZED VIEW IF NOT EXISTS user_engagement
ENGINE = SummingMergeTree()
ORDER BY (username, engagement_date)
AS SELECT
    u.username,
    toDate(p.created_at) as engagement_date,
    count(distinct p.post_id) as posts_count,
    count(distinct c.comment_id) as comments_count,
    sum(p.likes) as received_likes
FROM users u
LEFT JOIN posts p ON u.user_id = p.user_id
LEFT JOIN comments c ON u.user_id = c.user_id
GROUP BY u.username, engagement_date; 