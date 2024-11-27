from app import db
from datetime import datetime as dt


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
    author = db.relationship('User', backref='posts', lazy="select")


    def __repr__(self):
        return f"<Post(title={self.title})>"
