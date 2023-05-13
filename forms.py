from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from pony.orm import db_session
from db_storage import User


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        with db_session:
            email = User.get(email=email.data)
        if email:
            raise ValidationError('This Email already \
                    exists, please log in instead')


class LoginForm(FlaskForm):
    """ A class that defines a registration form for users """
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    """Add menu"""

    name = StringField("Name", validators=[DataRequired()])
    price = IntegerField("Price")
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField("Add")


class PostCategoryForm(FlaskForm):
    """Add category"""

    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add")