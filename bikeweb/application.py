from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bikeweb.models import Applicant, User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Contact Number', validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        applicant = Applicant.query.filter_by(username=username.data).first()
        if applicant:
            raise ValidationError("This username is already exist, please set another one")

    def validate_email(self,email):
        applicant = Applicant.query.filter_by(email=email.data).first()
        if applicant:
            raise ValidationError("This email is already exist, please enter another one")

class RefistrationAsUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already exist, please set another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already exist, please enter another one")



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BulletItems(FlaskForm):
    item = StringField("Model Name", validators=[DataRequired()])
    submit = SubmitField("Get Information")
