from flask import Flask, render_template, redirect, url_for
from forms import CreateForm
from model import db, Telescope, connect_to_db
from lists import class_list, location_list, wavelength_list, design_list, optics_list, fov_list, instrument_list, extras_list

app = Flask(__name__)
app.secret_key = "keep this secret"


@app.route("/")
def home():
    create_form = CreateForm()
    return render_template("home.html", create_form=create_form)

# @app.route("/info")
# def info():
#     team_list, project_list = get_team_project_list()
#     return render_template("info.html", team_list=team_list, project_list=project_list)


@app.route("/create-telescope", methods=["POST"])
def create_telescope():
    create_form = CreateForm()
    if create_form.validate_on_submit():
        class_name = class_list[int(create_form.class_name.data)][1]
        location = location_list[int(create_form.location.data)][1]
        wavelength = wavelength_list[int(create_form.wavelength.data)][1]
        design = design_list[int(create_form.design.data)][1]
        optics = optics_list[int(create_form.optics.data)][1]
        fov = fov_list[int(create_form.fov.data)][1]
        instrument = instrument_list[int(create_form.instrument.data)][1]
        extras = extras_list[int(create_form.extras.data)][1]
        new_telescope = Telescope(
            class_name, location, wavelength, design, optics, fov, instrument, extras)
        db.session.add(new_telescope)
        db.session.commit()
        print("Telescope created successfully!")
        return redirect(url_for("home"))
    else:
        print("Telescope not created")
        return redirect(url_for("home"))


@app.route("/summary")
def show_summary():
    pass


@app.route("/telescopes")
def show_telescopes():
    telescopes = Telescope.query.all()  # List of objects
    return render_template("telescopes.html", telescopes=telescopes)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
