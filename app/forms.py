from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from wtforms.widgets.core import CheckboxInput


class GenresCheckboxField(BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', CheckboxInput())
        super().__init__(*args, **kwargs)


class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description', validators=[Optional(), Length(min=1, max=100)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1, max=10000)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=70)])
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=100)])
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png'])])
    year = IntegerField('Year', validators=[DataRequired()], )
    book_txt = FileField('Txt_file', validators=[FileAllowed(['txt'])])

    Romance = GenresCheckboxField('Romance')
    Fiction = GenresCheckboxField('Fiction')
    Mystery = GenresCheckboxField('Mystery')
    Fantasy = GenresCheckboxField('Fantasy')
    Horror = GenresCheckboxField('Horror')
    Biography = GenresCheckboxField('Biography')
    Comedy = GenresCheckboxField('Comedy')
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
