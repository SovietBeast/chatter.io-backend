from tokenize import String
from xmlrpc.client import Boolean
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Boolean, String
from sqlalchemy.orm import declarative_base
from config.database import meta

# These is model from database this descibes database table

chatrooms = Table(
    'chatrooms', meta,
    Column('chatroom_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('name', String(255), nullable=False),
    Column('private', Boolean, nullable=False),
    Column('passcode', String(255))
)

messages = Table(
    'messages', meta,
    Column('message_id', Integer, primary_key=True, nullable=False),
    Column('message_text', String(255), nullable=False),
    Column('user_id', ForeignKey('users.user_id')),
    Column('chatroom_id', ForeignKey('chatrooms.chatroom_id')),
)


users = Table(
    'users', meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('username', String(255), nullable=False),
    Column('password', String(255), nullable=False),
    Column('email', String(255), nullable=False),
)

users_chat = Table(
    'users_chats', meta,
    Column('row_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('chat_id', Integer, ForeignKey('chatrooms.chatroom_id')),
)