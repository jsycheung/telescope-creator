from flask import Flask, render_template, redirect, url_for, flash
from forms import CreateForm, LoginForm, SignupForm
from model import db, Telescope, connect_to_db, User
from lists import class_list, location_list, wavelength_list, temperature_list, design_list, optics_list, fov_list, instrument_list, extras_list, class_list_cost, location_list_cost, wavelength_list_cost, temperature_list_cost, design_list_cost, optics_list_cost, fov_list_cost, instrument_list_cost, extras_list_cost
from crud import get_user_by_email, get_user_by_username, create_user
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
    return render_template("home.html", create_form=create_form, class_list_cost=class_list_cost, location_list_cost=location_list_cost, wavelength_list_cost=wavelength_list_cost, temperature_list_cost=temperature_list_cost, design_list_cost=design_list_cost, optics_list_cost=optics_list_cost, fov_list_cost=fov_list_cost, instrument_list_cost=instrument_list_cost, extras_list_cost=extras_list_cost)


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
                flash("Wrong password.", "danger")
        else:
            flash("Email is not registered.", "danger")
    return render_template("login.html", login_form=login_form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        if get_user_by_email(email):
            flash("Email already registered. Please log in.", "danger")
        elif get_user_by_username(username):
            flash("Username is used. Please select a new username.", "danger")
        else:
            hashed_password = bcrypt.generate_password_hash(
                signup_form.password.data).decode('utf-8')
            user = create_user(username, email, hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account successfully created. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html", signup_form=signup_form)

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
        wavelength = [wavelength_list[i][1]
                      for i in create_form.wavelength.data]
        print(wavelength)
        temperature = [temperature_list[i][1]
                       for i in create_form.temperature.data]
        design = design_list[int(create_form.design.data)][1]
        optics = optics_list[int(create_form.optics.data)][1]
        fov = [fov_list[i][1] for i in create_form.fov.data]
        instrument = [instrument_list[i][1]
                      for i in create_form.instrument.data]
        extras = [extras_list[i][1] for i in create_form.extras.data]
        cost = 100
        new_telescope = Telescope(
            class_name=class_name, location=location, wavelength=wavelength, temperature=temperature, design=design, optics=optics, fov=fov, instrument=instrument, extras=extras, cost=cost, user=current_user)
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
