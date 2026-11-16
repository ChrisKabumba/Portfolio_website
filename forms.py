from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    name = StringField('User name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])

class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[InputRequired(), Length(min=8, max=100)])
    description = CKEditorField('Project Description', validators=[InputRequired()])