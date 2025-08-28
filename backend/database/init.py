-- Initialize database schema
CREATE DATABASE IF NOT EXISTS whatsapp_clone;

USE whatsapp_clone;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    phone_number VARCHAR(20),
    country CHAR(2) DEFAULT 'US',
    avatar VARCHAR(200),
    credits INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_online BOOLEAN DEFAULT FALSE,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read BOOLEAN DEFAULT FALSE,
    is_ai_generated BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id),
    INDEX idx_sender (sender_id),
    INDEX idx_receiver (receiver_id),
    INDEX idx_timestamp (timestamp)
);

-- Chat rooms table
CREATE TABLE IF NOT EXISTS chat_rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    credit_cost INT DEFAULT 0,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_name (name)
);

-- User chat rooms junction table
CREATE TABLE IF NOT EXISTS user_chat_rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    chat_room_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (chat_room_id) REFERENCES chat_rooms(id),
    UNIQUE KEY unique_user_chat (user_id, chat_room_id)
);

-- Insert sample data
INSERT INTO users (username, email, password_hash, phone_number, country, credits) VALUES
('john_doe', 'john@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '+1234567890', 'US', 100),
('jane_smith', 'jane@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '+0987654321', 'UK', 50),
('alice_johnson', 'alice@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '+1122334455', 'CA', 75);

INSERT INTO messages (sender_id, receiver_id, content, message_type, timestamp) VALUES
(1, 2, 'Hey Jane, how are you?', 'text', NOW() - INTERVAL 10 MINUTE),
(2, 1, 'Hi John! I''m good, thanks for asking. How about you?', 'text', NOW() - INTERVAL 9 MINUTE),
(1, 2, 'I''m doing great! Just working on this new chat app.', 'text', NOW() - INTERVAL 8 MINUTE),
(3, 1, 'Hello John, this is Alice!', 'text', NOW() - INTERVAL 5 MINUTE);

INSERT INTO chat_rooms (name, description, is_private, created_by, credit_cost) VALUES
('General Chat', 'A place for general discussion', FALSE, 1, 0),
('Premium Lounge', 'Exclusive chat room for premium members', TRUE, 2, 10),
('Tech Talk', 'Discuss the latest in technology', FALSE, 3, 5);

INSERT INTO user_chat_rooms (user_id, chat_room_id, is_admin) VALUES
(1, 1, TRUE),
(2, 1, FALSE),
(3, 1, FALSE),
(2, 2, TRUE),
(1, 3, FALSE),
(3, 3, TRUE);
