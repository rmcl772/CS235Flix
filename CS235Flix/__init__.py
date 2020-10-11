from flask import Flask, url_for
from CS235Flix.adapters import memory_repository as repo
from os.path import join
from os import stat


def create_app(test_config=None):
    app = Flask(__name__)

    # app config
    app.config.from_object('config.Config')
    data_path = join("CS235Flix", "adapters", "data")

    # test config override
    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config["TEST_DATA_PATH"]

    # repo init
    repo.repo_instance = repo.init_repo(data_path)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from .movie import movie
        app.register_blueprint(movie.movie_blueprint)

        from .auth import auth
        app.register_blueprint(auth.auth_blueprint)

    return app
