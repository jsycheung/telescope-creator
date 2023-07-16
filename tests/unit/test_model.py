# Unit test script for model.py, which contains the SQLAlchemy interface to the postgreSQL database on AWS RDS
# Terminal script to run unit tests: python -m pytest tests/unit/
import pytest
from model import User, Telescope


@pytest.fixture(scope="module")
def new_user():
    user = User(username="hello123", email="hello123@gmail.com",
                hashed_password="hellohellohello")
    return user


def test_new_user(new_user):
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, hashed_password fields are defined correctly
    '''
    assert new_user.username == "hello123"
    assert new_user.email == "hello123@gmail.com"
    assert new_user.hashed_password == "hellohellohello"


@pytest.fixture(scope="module")
def new_telescope(new_user):
    telescope = Telescope(telescope_name="example telescope", class_name="Flagship", location="L2 [JWST]", wavelength=["UV"], temperature=["No Cooling"],
                          design="Standard tube [Hubble]", optics="Standard mirror [Hubble]", fov=["Narrow [Hubble]"], instrument=["Imager (camera)", "Polarimeters"], extras=["Coronograph"], cost=1000, user=new_user)
    return telescope


def test_new_telescope(new_telescope, new_user):
    '''
    GIVEN a Telescope model
    WHEN a new Telescope is created
    THEN check the telescope_name, class_name, location, wavelength, temperature, design, optics, fov,
    instrument, extras, cost, and user fields are defined correctly
    '''
    assert new_telescope.telescope_name == "example telescope"
    assert new_telescope.class_name == "Flagship"
    assert new_telescope.location == "L2 [JWST]"
    assert new_telescope.wavelength == ["UV"]
    assert new_telescope.temperature == ["No Cooling"]
    assert new_telescope.design == "Standard tube [Hubble]"
    assert new_telescope.optics == "Standard mirror [Hubble]"
    assert new_telescope.fov == ["Narrow [Hubble]"]
    assert new_telescope.instrument == ["Imager (camera)", "Polarimeters"]
    assert new_telescope.extras == ["Coronograph"]
    assert new_telescope.cost == 1000
    assert new_telescope.user == new_user
