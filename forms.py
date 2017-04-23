from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, \
    IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
         EqualTo('password', message='Passwords must match')]
    )


class CreateProject(Form):
    name = TextField(
        'Project Name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    short_desc = TextField(
        'Short Description', validators=[DataRequired(), Length(min=6, max=40)]
    )
    long_desc = TextAreaField(
        'Long Description', validators=[DataRequired(), Length(min=6, max=500)]
    )
    goal_amount = IntegerField(
        'Funding Goal', validators=[DataRequired(), Length(min=6, max=500)]
    )
    time_end = DateField(
        'Funding End Date', validators=[DataRequired(), Length(min=6, max=500)]
    )


class NewPledge(Form):

    amount = TextField(
        'Pledge Amount', validators=[DataRequired(), Length(min=6, max=40)]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class ForgotForm2(Form):
    username = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=40)]
    )
