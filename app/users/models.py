from datetime import datetime
from pytz import timezone
from app import db, bcrypt, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    about_me = db.Column(db.Text, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Kyiv')))

    def __repr__(self):
        return f"User('{self.email}')"

    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def change_password(self, new_password):
        self.password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def update_last_seen(self):
        self.last_seen = datetime.now(timezone('Europe/Kyiv'))


@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, user_id)
    if user:
        user.update_last_seen()
        db.session.commit()
    return user
