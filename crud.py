from model import User, Telescope


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
