import abc
from typing import List
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.review import Review


class RepoException(Exception):
    def __init__(self):
        pass


class AbstractRepo(abc.ABC):
    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds an actor to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name: str) -> Actor:
        """ Returns the actor with the given full name if in the repo, else None """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_actors(self) -> List[Actor]:
        """ Returns all actors in the repo """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a director to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_dull_name: str) -> Director:
        """ Returns the director with the given full name if in the repo, else None """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_directors(self) -> List[Director]:
        """ Returns all actors in the repo """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a genre to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_genres(self) -> List[Genre]:
        """ Returns all genres in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, movie_id: int) -> Movie:
        """ Returns the movie with the specified id """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_title(self, title: str) -> List[Movie]:
        """ Returns a list of movie(s) which match the given title """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, year: int) -> List[Movie]:
        """ Returns a list of movies created in the given year """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor: Actor) -> List[Movie]:
        """ Returns a list of movies which feature the given actor """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, genre: Genre) -> List[Movie]:
        """ Returns a list of movies directed by the given director """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre: Genre) -> List[Movie]:
        """ Returns a list of movies which fit the given genre """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a user to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """ Returns the user of the given username """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_of_movie(self, movie: Movie) -> List[Review]:
        """ Returns all the reviews of the specified movie """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self, review_id: int) -> Review:
        """ Returns the review with the specified id """
        raise NotImplementedError
