# installed flask-wtf using pip
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskblog.models import User
from flask_login import current_user

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


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), 
                                        Length(min=2, max=20)])
                                        
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])

    picture = FileField('Update Profile Picture', 
                        validators=[FileAllowed(['jpg', 'png', 'gif'])])

    submit = SubmitField('Update')

    # custom wtforms validator
    def validate_username(self, username):
        if username.data == current_user.username:
            return

        existing_user = User.query.filter_by(username=username.data).first()
        
        if existing_user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data == current_user.email:
            return

        existing_email = User.query.filter_by(email=email.data).first()
        
        if existing_email:
            raise ValidationError('This email is already taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        
        if existing_email is None:
            raise ValidationError('No Account uses this email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                            validators=[DataRequired()])

    password_confirm = PasswordField('Confirm Password', 
                            validators=[DataRequired(),
                                        EqualTo('password')])

    submit = SubmitField('Reset Password')