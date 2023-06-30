from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, PasswordField
from custom_field import MultiCheckboxField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from lists import class_list, location_list, wavelength_list, temperature_list, design_list, optics_list, fov_list, instrument_list, extras_list


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(
        "Field required."), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[
                             InputRequired("Field required.")])
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired("Field required.")])
    email = StringField("Email", validators=[InputRequired(
        "Field required."), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[InputRequired(
        "Field required."), Length(min=8, message="Password must be at least 8 characters long."), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField("Confirm password")
    submit = SubmitField("Submit")


class CreateForm(FlaskForm):
    class_name = RadioField(
        "Select class: ", choices=class_list, validators=[InputRequired()])
    location = RadioField("Select location: ",
                          choices=location_list, validators=[InputRequired()])
    wavelength = MultiCheckboxField("Select wavelength range: ",
                                    choices=wavelength_list, validators=[InputRequired()])
    temperature = MultiCheckboxField(
        "Select operating temperature: ", choices=temperature_list, validators=[InputRequired()])
    design = RadioField(
        "Select design: ", choices=design_list, validators=[InputRequired()])
    optics = RadioField(
        "Select optics: ", choices=optics_list, validators=[InputRequired()])
    fov = MultiCheckboxField("Select field of view: ",
                             choices=fov_list, validators=[InputRequired()])
    instrument = MultiCheckboxField(
        "Select instrument: ", choices=instrument_list, validators=[InputRequired()])
    extras = MultiCheckboxField("Select add-ons: ",
                                choices=extras_list, validators=[InputRequired()])
    submit = SubmitField("Submit")
