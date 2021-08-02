from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired


class Login_form(FlaskForm):
    user = TextField(validators=[DataRequired()])
    password = TextField()
    submit = SubmitField('LogIn')




