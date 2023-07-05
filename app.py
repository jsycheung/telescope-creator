from flask import Flask, render_template, redirect, url_for, flash, request
from forms import CreateForm, LoginForm, SignupForm, EditForm
from model import db, Telescope, connect_to_db, User
from lists import class_list, location_list, wavelength_list, temperature_list, design_list, optics_list, fov_list, instrument_list, extras_list, class_list_cost, location_list_cost, wavelength_list_cost, temperature_list_cost, design_list_cost, optics_list_cost, fov_list_cost, instrument_list_cost, extras_list_cost
from crud import get_user_by_email, get_user_by_username, create_user, crud_create_telescope, get_telescope_by_id
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, current_user, logout_user, login_required


app = Flask(__name__)
app.secret_key = "keep this secret"
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = ''
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route("/")
@login_required
def home():
    create_form = CreateForm()
    return render_template("home.html", create_form=create_form, class_list=class_list, class_list_cost=class_list_cost, location_list_cost=location_list_cost, wavelength_list_cost=wavelength_list_cost, temperature_list_cost=temperature_list_cost, design_list_cost=design_list_cost, optics_list_cost=optics_list_cost, fov_list_cost=fov_list_cost, instrument_list_cost=instrument_list_cost, extras_list_cost=extras_list_cost)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully!", "successful")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        user = get_user_by_email(email)
        if user:
            password = login_form.password.data.encode("utf-8")
            if bcrypt.check_password_hash(user.hashed_password, password):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Wrong password.", "dangerous")
        else:
            flash("Email is not registered.", "dangerous")
    return render_template("login.html", login_form=login_form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        if get_user_by_email(email):
            flash("Email already registered. Please log in.", "dangerous")
        elif get_user_by_username(username):
            flash("Username is used. Please select a new username.", "dangerous")
        else:
            hashed_password = bcrypt.generate_password_hash(
                signup_form.password.data).decode('utf-8')
            user = create_user(username, email, hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account successfully created. Please log in.", "successful")
            return redirect(url_for("login"))
    return render_template("signup.html", signup_form=signup_form)

# @app.route("/info")
# def info():
#     team_list, project_list = get_team_project_list()
#     return render_template("info.html", team_list=team_list, project_list=project_list)


@app.route("/create-telescope", methods=["POST"])
@login_required
def create_telescope():
    create_form = CreateForm()
    if create_form.validate_on_submit():
        telescope_name = create_form.telescope_name.data
        class_name = class_list[int(create_form.class_name.data)][1]
        location = location_list[int(create_form.location.data)][1]
        wavelength = [wavelength_list[i][1]
                      for i in create_form.wavelength.data]
        temperature = [temperature_list[i][1]
                       for i in create_form.temperature.data]
        design = design_list[int(create_form.design.data)][1]
        optics = optics_list[int(create_form.optics.data)][1]
        fov = [fov_list[i][1] for i in create_form.fov.data]
        instrument = [instrument_list[i][1]
                      for i in create_form.instrument.data]
        extras = [extras_list[i][1] for i in create_form.extras.data]
        cost = int(create_form.cost_value.data)
        if cost > class_list_cost[int(create_form.class_name.data)]:
            flash("Your budget is exceeded, telescope cannot be created.", "dangerous")
            return redirect(url_for("home"))
        new_telescope = crud_create_telescope(telescope_name, class_name, location, wavelength, temperature,
                                              design, optics, fov, instrument, extras, cost, current_user)
        db.session.add(new_telescope)
        db.session.commit()
        flash("Telescope created successfully!", "successful")
        return redirect(url_for("home"))
    else:
        flash("Telescope not created", "dangerous")
        return redirect(url_for("home"))


@app.route("/edit/<int:telescope_id>", methods=["GET", "POST"])
@login_required
def edit(telescope_id):
    current_telescope = get_telescope_by_id(telescope_id)
    if current_user != current_telescope.user:
        flash("Sorry, you don't have access to this telescope.", "dangerous")
        return redirect(url_for("inventory"))
    edit_form = EditForm()

    # Have to make sure the validate_on_submit block come first, otherwise if we make a post request, the new data will be overwritten by the existing one.
    if edit_form.validate_on_submit():
        current_telescope.telescope_name = edit_form.telescope_name.data
        print(edit_form.telescope_name.data)
        current_telescope.class_name = class_list[int(
            edit_form.class_name.data)][1]
        current_telescope.location = location_list[int(
            edit_form.location.data)][1]
        current_telescope.wavelength = [wavelength_list[i][1]
                                        for i in edit_form.wavelength.data]
        current_telescope.temperature = [temperature_list[i][1]
                                         for i in edit_form.temperature.data]
        current_telescope.design = design_list[int(edit_form.design.data)][1]
        current_telescope.optics = optics_list[int(edit_form.optics.data)][1]
        current_telescope.fov = [fov_list[i][1] for i in edit_form.fov.data]
        current_telescope.instrument = [instrument_list[i][1]
                                        for i in edit_form.instrument.data]
        current_telescope.extras = [extras_list[i][1]
                                    for i in edit_form.extras.data]
        current_telescope.cost = int(edit_form.cost_value.data)
        if current_telescope.cost > class_list_cost[int(edit_form.class_name.data)]:
            flash("Your budget is exceeded, telescope cannot be updated.", "dangerous")
            return redirect(url_for("edit", telescope_id=current_telescope.telescope_id))
        db.session.merge(current_telescope)
        db.session.commit()
        flash(
            f"Telescope {current_telescope.telescope_name} updated!", "successful")
        return redirect(url_for("inventory"))
    edit_form.telescope_name.data = current_telescope.telescope_name
    edit_form.class_name.data = [item[1] for item in class_list].index(
        current_telescope.class_name)
    edit_form.location.data = [item[1] for item in location_list].index(
        current_telescope.location)
    edit_form.wavelength.data = [[item[1] for item in wavelength_list].index(
        wavelength_item) for wavelength_item in current_telescope.wavelength]
    edit_form.temperature.data = [[item[1] for item in temperature_list].index(
        temperature_item) for temperature_item in current_telescope.temperature]
    edit_form.design.data = [item[1] for item in design_list].index(
        current_telescope.design)
    edit_form.optics.data = [item[1] for item in optics_list].index(
        current_telescope.optics)
    edit_form.fov.data = [[item[1] for item in fov_list].index(
        fov_item) for fov_item in current_telescope.fov]
    edit_form.instrument.data = [[item[1] for item in instrument_list].index(
        instrument_item) for instrument_item in current_telescope.instrument]
    edit_form.extras.data = [[item[1] for item in extras_list].index(
        extras_item) for extras_item in current_telescope.extras]

    return render_template("edit.html", edit_form=edit_form, current_telescope=current_telescope, class_list=class_list, class_list_cost=class_list_cost, location_list_cost=location_list_cost, wavelength_list_cost=wavelength_list_cost, temperature_list_cost=temperature_list_cost, design_list_cost=design_list_cost, optics_list_cost=optics_list_cost, fov_list_cost=fov_list_cost, instrument_list_cost=instrument_list_cost, extras_list_cost=extras_list_cost)


@app.route("/inventory")
@login_required
def inventory():
    telescopes = Telescope.query.filter_by(
        user=current_user)  # List of objects
    return render_template("inventory.html", telescopes=telescopes)


@app.route("/delete/<int:telescope_id>")
@login_required
def delete(telescope_id):
    telescope = get_telescope_by_id(telescope_id)
    db.session.delete(telescope)
    db.session.commit()
    flash(
        f"Telescope {telescope.telescope_name} deleted successfully!", "successful")
    return redirect(url_for("inventory"))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
