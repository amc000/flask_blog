import os

class Config:
    SECRET_KEY = os.environ.get('FlaskBlogSecretKey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('FlaskBlogMailUsername')
    MAIL_PASSWORD = os.environ.get('FlaskBlogMailPassword')