from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import SelectField


class RegisterForm(Form):
    role = SelectField(
        'Account Type', choices=[
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('user', 'User')])

    userid = TextField(
        'Username', validators=[DataRequired(), Length(min=2, max=25)]
    )

    name = TextField(
        'Name', validators=[DataRequired(), Length(min=6, max=25)]
    )

    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=2, max=40)]
    )

    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
         EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
