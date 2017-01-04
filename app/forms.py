from flask.ext.wtf import Form 
from wtforms import Form, BooleanField, StringField, PasswordField,FileField, validators
from app.models import Admin
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES


images = UploadSet('images', IMAGES)
   
class LoginForm(Form):
	nickname = StringField('Username',[validators.Required()],render_kw={"placeholder": "Enter your username"})
	password = PasswordField('Password',[validators.Required()],render_kw={"placeholder": "Enter your password"})
    

class MailForm(Form):
	name = StringField('name',[validators.Required()],render_kw={"placeholder": "Full name"})
	email =StringField('name',[validators.Required()],render_kw={"placeholder": "email"})
	comment =StringField('name',[validators.Required()],render_kw={"placeholder": "your comment"})
 

class BlogForm(Form):
	art_name = StringField('name',[validators.Required()],render_kw={"placeholder": "Article name"})
 	short_name = StringField('short_name',[validators.Length(min=6, max=20)],render_kw={"placeholder": "name for link"})
 	review = StringField('review',[validators.Length(max=200)],render_kw={"placeholder": "review your article"})
 	cover = FileField('file',validators=[FileRequired(),FileAllowed(images, 'Images only!')],render_kw={"placeholder": "add cover"})