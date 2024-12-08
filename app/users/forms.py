from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=14),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_-]*$',
                                                          message="Username must start with a letter and contain only "
                                                                  "letters, numbers, dots or underscores.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least "
                                                                                           "6 characters long")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already registered.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    about_me = TextAreaField('About Me', validators=[Length(max=750)])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered.')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already registered.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password',
                                     validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[
                                     DataRequired(),
                                     Length(min=6, message='Password must be at least 6 characters')
                                 ])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('new_password', message='Passwords must match')
                                     ])
    submit = SubmitField('Change Password')

    def validate_current_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Current password is incorrect')
