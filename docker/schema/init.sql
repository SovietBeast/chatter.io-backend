CREATE DATABASE chatterio;
\c  chatterio;

CREATE TABLE users (
    user_id SERIAL NOT NULL,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    PRIMARY KEY (user_id)
);

-- chatrooms 1:M users
CREATE TABLE chatrooms (
    chatroom_id SERIAL NOT NULL,
    name varchar(255) NOT NULL,
    private boolean NOT NULL,
    passcode varchar(255),
    PRIMARY KEY (chatroom_id)
);

-- message M:1 users
-- message M:1 chatrooms
CREATE TABLE messages (
    message_id SERIAL NOT NULL,
    message_text TEXT NOT NULL,
    user_id int NOT NULL,
    chatroom_id int NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (chatroom_id) REFERENCES chatrooms(chatroom_id)
);

CREATE TABLE test(
    test_id SERIAL NOT NULL
)