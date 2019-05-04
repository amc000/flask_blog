#imports here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture = FileField('Attach Image', validators=[FileAllowed(['jpg', 'png'])])
    track = FileField('Attach Audio', validators=[FileAllowed(['mp3', 'wav', 'ogg'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    price = IntegerField('Price (USD Cents)', validators=[DataRequired()])
    submit = SubmitField('Post')
