from model import User, Telescope, db


def get_user_by_email(email):
    '''return a user by email'''
    return User.query.filter(User.email == email).first()


def get_user_by_username(username):
    '''return a user by username'''
    return User.query.filter(User.username == username).first()


def create_user(username, email, hashed_password):
    '''Create and return a new user.'''
    user = User(username=username, email=email,
                hashed_password=hashed_password)
    return user


def crud_create_telescope(telescope_name, class_name, location, wavelength, temperature, design, optics, fov, instrument, extras, cost, current_user):
    '''Create and return a new telescope'''
    new_telescope = Telescope(telescope_name=telescope_name, class_name=class_name, location=location, wavelength=wavelength, temperature=temperature,
                              design=design, optics=optics, fov=fov, instrument=instrument, extras=extras, cost=cost, user=current_user)
    return new_telescope


def get_telescope_by_id(telescope_id):
    # telescope = Telescope.query.filter_by(telescope_id=telescope_id).first()
    telescope = db.session.query(Telescope).filter(
        Telescope.telescope_id == telescope_id).first()
    return telescope
