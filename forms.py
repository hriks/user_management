from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms import SelectField


# Registration WTF form when logged in
# as Admin or Manager
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


# Registration WTF form without logging.
class RegistrationForm(Form):
    role = SelectField(
        'Account Type', choices=[
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


# Login WTF LoginForm
class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


# Post Message WTF form
class PostMessage(Form):
    message = TextField('Message', [DataRequired()])


# Update WTF form
class UpdateForm(Form):
    role = SelectField(
        'Account Type', choices=[
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('user', 'User')])

    userid = TextField(
        'New Username', validators=[DataRequired(), Length(min=2, max=25)]
    )

    name = TextField(
        'New Name', validators=[Length(min=6, max=25)]
    )

    email = TextField(
        'New Email', validators=[Length(min=6, max=40)]
    )

    password = PasswordField(
        'New Password', validators=[Length(min=2, max=40)]
    )
