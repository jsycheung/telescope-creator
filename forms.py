from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from custom_field import MultiCheckboxField
from wtforms.validators import DataRequired
from lists import class_list, location_list, wavelength_list, temperature_list, design_list, optics_list, fov_list, instrument_list, extras_list


class CreateForm(FlaskForm):
    class_name = RadioField(
        "Select class: ", choices=class_list, validators=[DataRequired()])
    location = RadioField("Select location: ",
                          choices=location_list, validators=[DataRequired()])
    wavelength = MultiCheckboxField("Select wavelength range: ",
                                    choices=wavelength_list, validators=[DataRequired()])
    temperature = MultiCheckboxField(
        "Select operating temperature: ", choices=temperature_list, validators=[DataRequired()])
    design = RadioField(
        "Select design: ", choices=design_list, validators=[DataRequired()])
    optics = RadioField(
        "Select optics: ", choices=optics_list, validators=[DataRequired()])
    fov = MultiCheckboxField("Select field of view: ",
                             choices=fov_list, validators=[DataRequired()])
    instrument = MultiCheckboxField(
        "Select instrument: ", choices=instrument_list, validators=[DataRequired()])
    extras = MultiCheckboxField("Select add-ons: ",
                                choices=extras_list, validators=[DataRequired()])
    submit = SubmitField("Submit")
