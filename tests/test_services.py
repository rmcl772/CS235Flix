import pytest

from CS235Flix.auth import services as auth_services
from CS235Flix.movies import services as movies_services


def test_auth(repo):
    # adds user correctly (already 6 users in repo)
    auth_services.add_user("username", "password", testing=True)
    assert repo.get_user("username") is not None

    # duplicate user raises NameTakenException
    with pytest.raises(auth_services.NameTakenException):
        auth_services.add_user("username", "password")

    # get user correctly
    user = auth_services.get_user("username")
    assert user is not None

    # invalid user raises InvalidUserException
    with pytest.raises(auth_services.InvalidUserException):
        auth_services.get_user("Invalid_user")

    # should not raise error
    auth_services.auth_user(user, "password")

    # should raise error
    with pytest.raises(auth_services.IncorrectPasswordException):
        auth_services.auth_user(user, "wrong_password")


def test_movies():
    # hard to really test these ones, easier to see visually on the website

    data = [chr(i) for i in range(97, 97 + 26)]

    # turn data into 4 x n array
    grid = movies_services.grid_layout(data, 4)

    # should be 7 rows
    assert len(grid) == 7
    # with 4 items
    assert len(grid[0]) == 4
    # apart from the las one which fits only 2
    assert len(grid[-1]) == 2

    alpha_list = movies_services.alphabetical_list(data)
    # split into lists by alphabet letter
    assert len(alpha_list) == 26
    # each contains 1 letter
    assert all([len(row) == 1 for row in alpha_list])
