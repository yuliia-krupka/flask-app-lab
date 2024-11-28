from app import db
from datetime import datetime as dt
from sqlalchemy.orm import backref

# Асоціативна таблиця для зв'язку "багато до багатьох"
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    posted = db.Column(db.DateTime, default=dt.now())
    is_active = db.Column(db.Boolean, nullable=True, default=True)
    category = db.Column(db.String, nullable=True)
    # author = db.Column(db.String(20), nullable=True) to remove
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    author = db.relationship('User', backref=backref("posts", lazy="dynamic"), lazy="joined")

    # Зв'язок "багато до багатьох" з тегами.
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    def __repr__(self):
        return f"<Post(title={self.title})>"


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Зв'язок "багато до багатьох" з постами
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')



