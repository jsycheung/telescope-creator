'''
Contains the backbone of the Flask app - all view functions necessary to the app.
'''
from flask import Flask, render_template, redirect, url_for, flash
from forms import CreateForm, LoginForm, SignupForm, EditForm
from model import db, Telescope, User
from lists import class_list, location_list, wavelength_list, temperature_list, design_list, optics_list, fov_list, instrument_list, extras_list, class_list_cost, location_list_cost, wavelength_list_cost, temperature_list_cost, design_list_cost, optics_list_cost, fov_list_cost, instrument_list_cost, extras_list_cost
from crud import get_user_by_email, get_user_by_username, create_user, crud_create_telescope, get_telescope_by_id
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
import os

# Create a Flask application object.
app = Flask(__name__)
# Define app secret key.
app.secret_key = "keep this secret"
# Create a LoginManager object for login functionality.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
# login_view sets the endpoint to direct to if the page requires login but the user is not logged in yet.
login_manager.login_view = "login"
# Set login_message to an empty string so that message does not pop up every time user is redirected to login page.
login_manager.login_message = ''
login_manager.login_message_category = "info"
# Create a Bcrypt object for hashing passwords.
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    '''Get current user in the session.'''
    return db.session.get(User, user_id)


@app.route("/")
@login_required
def home():
    '''Render homepage for creating telescopes.'''
    create_form = CreateForm()
    return render_template("home.html", create_form=create_form, class_list=class_list, class_list_cost=class_list_cost, location_list_cost=location_list_cost, wavelength_list_cost=wavelength_list_cost, temperature_list_cost=temperature_list_cost, design_list_cost=design_list_cost, optics_list_cost=optics_list_cost, fov_list_cost=fov_list_cost, instrument_list_cost=instrument_list_cost, extras_list_cost=extras_list_cost)


@app.route("/logout")
@login_required
def logout():
    '''Log out user and redirect to login page.'''
    logout_user()
    flash("You have logged out successfully!", "successful")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    '''Renders log in page and contains logic for logging in user.'''
    login_form = LoginForm()
    if login_form.validate_on_submit():
        '''Handle logic after submitting login form.'''
        email = login_form.email.data
        user = get_user_by_email(email)
        if user:
            '''If user with specified email exists, proceed. If not, flash email not registered.'''
            password = login_form.password.data.encode("utf-8")
            if bcrypt.check_password_hash(user.hashed_password, password):
                '''If user with specified email exists and the password is correct, log in user and redirect to home page for creating telescope. If not, flash wrong password.'''
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Wrong password.", "dangerous")
                return render_template("login.html", login_form=login_form), 401
        else:
            flash("Email is not registered.", "dangerous")
            return render_template("login.html", login_form=login_form), 409
    return render_template("login.html", login_form=login_form)


@app.route("/guest-login")
def guest_login():
    '''For quick access to webpage using guest account. Automatically log into guest account without entering email and password.'''
    user = get_user_by_email("guest@guest.com")
    login_user(user)
    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    '''Renders sign up page and contains logic for creating a new user.'''
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        '''Handle logic after submitting sign up form.'''
        username = signup_form.username.data
        email = signup_form.email.data
        if get_user_by_email(email):
            '''If the email is registered, flash warning message.'''
            flash("Email already registered. Please log in.", "dangerous")
            return render_template("signup.html", signup_form=signup_form), 409
        elif get_user_by_username(username):
            '''Make sure the username is not used already in existing users.'''
            flash("Username is used. Please select a new username.", "dangerous")
            return render_template("signup.html", signup_form=signup_form), 409
        else:
            '''If the email is not registered before and the username is unique, then create a new user in the database and redirect to log in page.'''
            hashed_password = bcrypt.generate_password_hash(
                signup_form.password.data).decode('utf-8')
            user = create_user(username, email, hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account successfully created. Please log in.", "successful")
            return redirect(url_for("login"))
    return render_template("signup.html", signup_form=signup_form)


@app.route("/create-telescope", methods=["POST"])
@login_required
def create_telescope():
    '''Contains form and logic for creating a new telescope.'''
    create_form = CreateForm()
    if create_form.validate_on_submit():
        '''Handle logic after submitting create form.'''
        telescope_name = create_form.telescope_name.data
        '''Get the item tuple in corresponding list by index, and access the name of the item using index 1.'''
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
            '''If the cost of the telescope exceeds the budget of the class of telescope, don't let the user create the telescope.'''
            flash("Your budget is exceeded, telescope cannot be created.", "dangerous")
            return redirect(url_for("home"))
        # Create a new telescope object and add to database.
        new_telescope = crud_create_telescope(telescope_name, class_name, location, wavelength, temperature,
                                              design, optics, fov, instrument, extras, cost, current_user)
        db.session.add(new_telescope)
        db.session.commit()
        flash("Telescope created successfully!", "successful")
        return redirect(url_for("home"))


@app.route("/edit/<int:telescope_id>", methods=["GET", "POST"])
@login_required
def edit(telescope_id):
    '''Renders edit page and contains logic for editing telescope entry in the database.'''
    current_telescope = get_telescope_by_id(
        telescope_id)  # Get the telescope for editing.
    if current_user != current_telescope.user:
        '''If a user try to access a telescope id that is not created by the user, they will be denied access.'''
        flash("Sorry, you don't have access to this telescope.", "dangerous")
        return redirect(url_for("inventory"))
    edit_form = EditForm()

    # Have to make sure the validate_on_submit block come first, otherwise if we make a post request, the new data will be overwritten by the existing one.
    if edit_form.validate_on_submit():
        '''Handles logic after submitting edit form.'''
        current_telescope.telescope_name = edit_form.telescope_name.data
        '''Get the item tuple in corresponding list by index, and access the name of the item using index 1. Change the telescope attribute accordingly.'''
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
            '''If the cost of the updated telescope exceeds the budget of the updated class of the telescope, do not allow user to update the telescope.'''
            flash("Your budget is exceeded, telescope cannot be updated.", "dangerous")
            return redirect(url_for("edit", telescope_id=current_telescope.telescope_id))
        # Update telescope entry in database.
        db.session.add(current_telescope)
        db.session.commit()
        flash(
            f"Telescope {current_telescope.telescope_name} updated!", "successful")
        return redirect(url_for("inventory"))
    '''When first rendering the edit form, pre-fill it with existing data of the telescope.'''
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
    '''Renders inventory page and contains logic that retrieves all telescope entries in the database to display on the webpage.'''
    telescopes = Telescope.query.filter_by(
        user=current_user)  # List of objects
    return render_template("inventory.html", telescopes=telescopes)


@app.route("/delete/<int:telescope_id>")
@login_required
def delete(telescope_id):
    '''Contains logic to handle deletion of telescope entry in the database.'''
    telescope = get_telescope_by_id(telescope_id)
    if current_user != telescope.user:
        # If a user tries to access the endpoint corresponding to a telescope created by a different user, deny access.
        flash("Sorry, you don't have access to this telescope.", "dangerous")
        return redirect(url_for("inventory"))
    # Delete telescope entry in database.
    db.session.delete(telescope)
    db.session.commit()
    flash(
        f"Telescope {telescope.telescope_name} deleted successfully!", "successful")
    return redirect(url_for("inventory"))


if __name__ == "__main__" or __name__ == "app":
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        db.create_all()
        username = "guest"
        email = "guest@guest.com"
        hashed_password = bcrypt.generate_password_hash(
            "12345678").decode('utf-8')
        user = create_user(username, email, hashed_password)
        if get_user_by_email(email) is None:
            '''Pre-populate the database with guest user.'''
            db.session.add(user)
            db.session.commit()
    app.run()
