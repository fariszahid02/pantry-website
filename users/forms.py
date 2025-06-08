# Authored by: Yat Nam, Faris
# forms for registering as a user and changing password
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email


# Form for user registration
class RegisterForm(FlaskForm):
    # Date of Birth field with validation for DD/MM/YYYY format
    dob_regexp = Regexp(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$',
                        message="Invalid date format, must be DD/MM/YYYY")
    dob = StringField('Date of Birth', validators=[DataRequired(), dob_regexp])

    # Email field with validation for proper email format
    email = EmailField('Email', validators=[DataRequired(), Email(
        message="Invalid email address")])

    # Firstname and Lastname: Exclude specified characters
    name_regexp = Regexp(r'^[^*?!\'^+%&/()=}]{3,}$',
                         message="Invalid characters in name")
    first_name = StringField('Firstname',
                             validators=[DataRequired(), name_regexp])
    last_name = StringField('Lastname', validators=[DataRequired(), name_regexp])

    # Password: Specific length and character requirements
    password_regexp = Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,12}$',
                             message="Password must be 6-12 characters long, include digits, lowercase, uppercase, and special characters")
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=12),
                                         password_regexp])

    # Confirm Password: Must match Password
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message="Passwords must match")])

    submit = SubmitField('Register')


# Form for user login
class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


# Form for changing the user's password
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    show_password = BooleanField('Show Password')
    submit = SubmitField('Change Password')
