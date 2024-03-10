from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Many-to-many association table for Post and Tag
post_tags = Table('Post_Tag', Base.metadata,
                  Column('post_id', Integer, ForeignKey('Post.id'), primary_key=True),
                  Column('tag_id', Integer, ForeignKey('Tag.id'), primary_key=True))

class User(Base):
    __tablename__ = 'User'  # Changed to match the class name
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    posts = relationship('Post', backref='author', lazy='dynamic')

class Post(Base):
    __tablename__ = 'Post'  # Changed to match the class name
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    body = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    comments = relationship('Comment', backref='post', lazy='dynamic')
    tags = relationship('Tag', secondary=post_tags, back_populates='posts')

class Comment(Base):
    __tablename__ = 'Comment'  # Changed to match the class name
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)

class Tag(Base):
    __tablename__ = 'Tag'  # Changed to match the class name
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    posts = relationship('Post', secondary=post_tags, back_populates='tags')
