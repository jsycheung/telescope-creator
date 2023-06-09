from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, PasswordField, HiddenField
from custom_field import MultiCheckboxField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from lists import class_list, location_list, wavelength_list, temperature_list, design_list, optics_list, fov_list, instrument_list, extras_list


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        InputRequired(), Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[
                             InputRequired()])
    submit = SubmitField("Sign In")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired()])
    email = StringField("Email", validators=[
                        InputRequired(), Email("Please enter a valid email.")])
    password = PasswordField("Password (at least 8 characters long)", validators=[InputRequired(), Length(
        min=8, message="Password must be at least 8 characters long."), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField("Confirm password")
    submit = SubmitField("Sign Up")


class CreateForm(FlaskForm):
    cost_value = HiddenField("cost-value")
    telescope_name = StringField(
        "Telescope name", validators=[InputRequired()])
    class_name = RadioField(
        "Class", choices=class_list, coerce=int, validators=[InputRequired()])
    location = RadioField("Location",
                          choices=location_list, coerce=int, validators=[InputRequired()])
    wavelength = MultiCheckboxField("Wavelength Range (multiple allowed)",
                                    choices=wavelength_list, coerce=int, validators=[InputRequired()])
    temperature = MultiCheckboxField(
        "Operating Temperature (multiple allowed)", choices=temperature_list, coerce=int, validators=[InputRequired()])
    design = RadioField(
        "Design", choices=design_list, coerce=int, validators=[InputRequired()])
    optics = RadioField(
        "Optics", choices=optics_list, coerce=int, validators=[InputRequired()])
    fov = MultiCheckboxField("Field of View (multiple allowed)",
                             choices=fov_list, coerce=int, validators=[InputRequired()])
    instrument = MultiCheckboxField(
        "Instrument (multiple allowed)", choices=instrument_list, coerce=int, validators=[InputRequired()])
    extras = MultiCheckboxField("Add-ons (optional, multiple allowed)",
                                choices=extras_list, coerce=int)
# cannot validate multicheckboxfield


class EditForm(CreateForm):
    pass
