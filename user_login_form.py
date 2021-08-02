from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, InputRequired


class LoginForm(FlaskForm):
    user = StringField(validators=[InputRequired(), Length(min=5, max=20, message='Must Be 5-10 characters')])
    password = PasswordField()
    rec = RecaptchaField()
    submit = SubmitField('LogIn')
