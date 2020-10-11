import CS235Flix.adapters.memory_repository as repo
from CS235Flix.domainmodel.user import User
from passlib.hash import sha256_crypt


class NameTakenException(Exception): pass
class InvalidUserException(Exception): pass
class IncorrectPasswordException(Exception): pass


def add_user(username, password, testing=False):
    if repo.repo_instance.get_user(username) is not None:
        raise NameTakenException

    # encrypt user password
    password = sha256_crypt.hash(password)

    user = User(username, password)
    repo.repo_instance.add_user(user, from_file=testing)


def get_user(username):
    user = repo.repo_instance.get_user(username)

    if user is None:
        raise InvalidUserException

    return user


def auth_user(user, password):
    # verify password against encrypted password
    if not sha256_crypt.verify(password, user.password):
        raise IncorrectPasswordException

