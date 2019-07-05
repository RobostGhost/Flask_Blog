# installed flask-wtf using pip
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), 
                                        Length(min=2, max=20)])
                                        
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])

    password = PasswordField('Password', 
                            validators=[DataRequired()])

    password_confirm = PasswordField('Confirm Password', 
                            validators=[DataRequired(),
                                        EqualTo('password')])

    submit = SubmitField('Sign Up')

    # custom wtforms validator
    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        
        if existing_user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        
        if existing_email:
            raise ValidationError('This email is already taken. Please choose a different one.')


class LoginForm(FlaskForm):                                 
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])

    password = PasswordField('Password', 
                            validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
