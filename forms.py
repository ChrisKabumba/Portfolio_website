from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import Length, InputRequired, Email
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    email = StringField('User name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])
    submit = SubmitField('Submit')

class NewProjectForm(FlaskForm):
    email = EmailField('Project name', validators=[InputRequired(), Length(min=8, max=100), Email()])
    description = CKEditorField('Project Description', validators=[InputRequired()])
    #TODO