from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired
from lists import class_list, location_list, wavelength_list, design_list, optics_list, fov_list, instrument_list, extras_list


class CreateForm(FlaskForm):
    class_name = SelectField(
        "Select class: ", choices=class_list, validators=[DataRequired()], coerce=int)
    location = SelectField("Select location: ",
                           choices=location_list, validators=[DataRequired()])
    wavelength = SelectField("Select wavelength range: ",
                             choices=wavelength_list, validators=[DataRequired()])
    design = SelectField(
        "Select design: ", choices=design_list, validators=[DataRequired()])
    optics = SelectField(
        "Select optics: ", choices=optics_list, validators=[DataRequired()])
    fov = SelectField("Select field of view: ",
                      choices=fov_list, validators=[DataRequired()])
    instrument = SelectField(
        "Select instrument: ", choices=instrument_list, validators=[DataRequired()])
    extras = SelectField("Select add-ons: ",
                         choices=extras_list, validators=[DataRequired()])
    submit = SubmitField("Submit")
