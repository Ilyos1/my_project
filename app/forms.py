from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    description = StringField('Description', validators=[Optional(), Length(min=4, max=100)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(max=10000)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=70)])
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=100)])
    genres = StringField('Genres', validators=[DataRequired(), Length(min=4, max=100)])
    year = StringField('Genres', validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('Create')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
