from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=2000)])
    due_date = DateTimeField('Due Date (YYYY-mm-dd HH:MM)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    priority = SelectField('Priority', choices=[('Low','Low'), ('Medium','Medium'), ('High','High')], validators=[Optional()])
    category = StringField('Category', validators=[Optional(), Length(max=100)])
    reminder = DateTimeField('Reminder (YYYY-mm-dd HH:MM)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    submit = SubmitField('Save')
