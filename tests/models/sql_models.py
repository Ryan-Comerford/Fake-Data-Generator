from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    bio = Column(String(500))
    profile_picture_url = Column(String(255))
    user = relationship("User", back_populates="profile")

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=True)
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    posts = relationship('Post', backref='author')
    comments = relationship('Comment', backref='author')

class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    posts = relationship("Post", backref="category")

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    body = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('Category.id'))
    comments = relationship('Comment', backref='post')
    tags = relationship('Tag', secondary='Post_Tag', back_populates='posts')

class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)

class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    posts = relationship('Post', secondary='Post_Tag', back_populates='tags')

class PostTag(Base):
    __tablename__ = 'Post_Tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('Post.id'))
    tag_id = Column(Integer, ForeignKey('Tag.id'))
    post = relationship(Post, backref="post_tag_associations")
    tag = relationship(Tag, backref="tag_post_associations")

class PostLike(Base):
    __tablename__ = 'PostLike'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('Post.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    post = relationship(Post, backref="likes")
    user = relationship(User, backref="liked_posts")

class CommentLike(Base):
    __tablename__ = 'CommentLike'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(Integer, ForeignKey('Comment.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    comment = relationship(Comment, backref="likes")
    user = relationship(User, backref="liked_comments")
