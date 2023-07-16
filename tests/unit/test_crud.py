# Unit test script for crud.py, which contains functions for querying and creating database entry
# Terminal script to run unit tests: python -m pytest tests/unit/
import pytest
import os
from crud import get_user_by_email, get_user_by_username, create_user, crud_create_telescope, get_telescope_by_id
from app import app


@pytest.fixture(scope="module")
def email_user(email="guest@guest.com"):
    with app.app_context():
        user = get_user_by_email(email)
        return user


def test_get_user_by_email(email_user):
    '''
    GIVEN a User model and a database entry with a particular email
    WHEN we get a user by email
    THEN check that the user is correctly identified, that the user_id username, email, hashed_password fields are correct
    '''
    assert email_user.user_id == 1
    assert email_user.username == "guest"
    assert email_user.email == "guest@guest.com"
    assert email_user.hashed_password == "$2b$12$nV9rb5WgdFI9fIFFg7HwKerSov33lNwpTe3DA2kYy8/p0oiN4MEOC"


@pytest.fixture(scope="module")
def username_user(username="guest"):
    with app.app_context():
        user = get_user_by_username(username)
        return user


def test_get_user_by_username(username_user):
    '''
    GIVEN a User model and a database entry with a particular username
    WHEN we get a user by username
    THEN check that the user is correctly identified, that the user_id username, email, hashed_password fields are correct
    '''
    assert username_user.user_id == 1
    assert username_user.username == "guest"
    assert username_user.email == "guest@guest.com"
    assert username_user.hashed_password == "$2b$12$nV9rb5WgdFI9fIFFg7HwKerSov33lNwpTe3DA2kYy8/p0oiN4MEOC"


@pytest.fixture(scope="module")
def create_user_user(username="hello123", email="hello123@gmail.com", hashed_password="hellohellohello"):
    user = create_user(username, email, hashed_password)
    return user


def test_create_user(create_user_user):
    '''
    GIVEN a User model
    WHEN a new User is created using the create_user function
    THEN check the username, email, hashed_password fields are defined correctly
    '''
    assert create_user_user.username == "hello123"
    assert create_user_user.email == "hello123@gmail.com"
    assert create_user_user.hashed_password == "hellohellohello"


@pytest.fixture(scope="module")
def create_telescope_telescope(telescope_name="example telescope", class_name="Flagship", location="L2 [JWST]", wavelength=["UV"], temperature=["No Cooling"],
                               design="Standard tube [Hubble]", optics="Standard mirror [Hubble]", fov=["Narrow [Hubble]"], instrument=["Imager (camera)", "Polarimeters"], extras=["Coronograph"], cost=1000, user=create_user("hello123", "hello123@gmail.com", "hellohellohello")):
    telescope = crud_create_telescope(telescope_name, class_name, location,
                                      wavelength, temperature, design, optics, fov, instrument, extras, cost, user)
    return telescope


def test_crud_create_telescope(create_telescope_telescope, create_user_user):
    '''
    GIVEN a Telescope model
    WHEN a new Telescope is created using crud_create_telescope function
    THEN check the telescope_name, class_name, location, wavelength, temperature, design, optics, fov,
    instrument, extras, cost, and user fields are defined correctly
    '''
    assert create_telescope_telescope.telescope_name == "example telescope"
    assert create_telescope_telescope.class_name == "Flagship"
    assert create_telescope_telescope.location == "L2 [JWST]"
    assert create_telescope_telescope.wavelength == ["UV"]
    assert create_telescope_telescope.temperature == ["No Cooling"]
    assert create_telescope_telescope.design == "Standard tube [Hubble]"
    assert create_telescope_telescope.optics == "Standard mirror [Hubble]"
    assert create_telescope_telescope.fov == ["Narrow [Hubble]"]
    assert create_telescope_telescope.instrument == [
        "Imager (camera)", "Polarimeters"]
    assert create_telescope_telescope.extras == ["Coronograph"]
    assert create_telescope_telescope.cost == 1000
    assert create_telescope_telescope.user == create_user_user


@pytest.fixture(scope="module")
def id_telescope(telescope_id=1):
    with app.app_context():
        telescope = get_telescope_by_id(telescope_id)
        return telescope


def test_get_telescope_by_id(id_telescope):
    '''
    GIVEN a Telescope model and a database entry with a particular telescope_id
    WHEN we get a telescope by telescope_id
    THEN check that the telescope is correctly identified, and that the telescope_name, class_name, location, wavelength, temperature, design, optics, fov,
    instrument, extras, cost, and user fields are correct
    '''
    assert id_telescope.telescope_id == 1
    assert id_telescope.telescope_name == "Example"
    assert id_telescope.class_name == "Flagship"
    assert id_telescope.location == "Other Solar System Orbit [Spitzer]"
    assert id_telescope.wavelength == ["Gamma Ray"]
    assert id_telescope.temperature == ["No Cooling"]
    assert id_telescope.design == "Standard tube [Hubble]"
    assert id_telescope.optics == "No Mirror [Fermi]"
    assert id_telescope.fov == ["Narrow [Hubble]"]
    assert id_telescope.instrument == ["Imager (camera)"]
    assert id_telescope.extras == ["Coronograph"]
    assert id_telescope.cost == 900
    assert id_telescope.user_id == 1
