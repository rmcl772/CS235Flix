from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.watchlist import WatchList


class User:
    def __init__(self, user_name: str, password: str):
        self._name = user_name.strip().lower()
        self._password = password.strip()

        self._watched_movies = []
        self._reviews = []
        self._watchlist = WatchList()
        self._watch_time = 0

    @property
    def user_name(self):
        return self._name

    @user_name.setter
    def user_name(self, name:str):
        self._name = name.strip().lower() if type(name) is str else None

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def watchlist(self):
        return self._watchlist

    @property
    def time_spent_watching_movies_minutes(self):
        return self._watch_time

    def watch_time_formatted(self):
        hours = self._watch_time // 60
        mins = self._watch_time % 60

        hours = f"{hours}h " if hours > 0 else ""

        return f"{hours}{mins}m"

    def watched_movies_count(self):
        return len(self._watched_movies)

    def reviews_count(self):
        return len(self._reviews)

    def watch_movie(self, movie: Movie):
        if type(movie) is Movie:
            self._watch_time += movie.runtime_minutes

            if movie not in self._watched_movies:
                self._watched_movies.append(movie)

    def add_review(self, review: Review):
        if type(review) is Review and review not in self._reviews:
            self._reviews.append(review)

    def __repr__(self):
        return f"<User {self._name}>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_name == other.user_name
        elif isinstance(other, str):
            return self.user_name == other.lower()
        else:
            return False

    def __lt__(self, other):
        return sorted((self.user_name, other.user_name))[0] == self.user_name

    def __hash__(self):
        return hash(self._name)
