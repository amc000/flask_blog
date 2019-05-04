from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_blog import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
    # Audio_file is similar to image_file in that it is a filename which is appended to the appropriate directory
    # when it is used. You should be able to access a file with the same filename from audio_snippets or audio_files.
    audio_file = db.Column(db.String(20), unique=False, nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Prices of tracks are stored in USD and the integer is total USD cents.
    price = db.Column(db.Integer, unique=False, nullable=False, default=500)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.image_file}')"
