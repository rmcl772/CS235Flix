from datetime import datetime
from CS235Flix.domainmodel.movie import Movie


class Review:
    def __init__(self, movie: Movie, review_text: str, rating: float, user: str, timestamp: str = None,
                 id_num: int = None):
        if type(movie) is not Movie:
            self._movie = None
        else:
            self._movie = movie

        if type(review_text) is not str:
            self._text = None
        else:
            self._text = review_text

        if type(rating) not in (int, float) or not 0 <= rating <= 10:
            self._rating = None
        else:
            self._rating = rating

        if type(user) != str:
            self._user = None
        else:
            self._user = user

        if timestamp is not None:
            self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S")
        else:
            self._timestamp = datetime.now()

        if type(id_num) is not int:
            self._id_num = None
        else:
            self._id_num = id_num

    @property
    def id(self):
        return self._id_num

    @id.setter
    def id(self, id_num: int):
        if type(id_num) != int:
            raise ValueError
        else:
            self._id_num = id_num

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if type(user) not in ("User", str):
            self._user = None
        elif type(user) == "User":
            self._user = user.user_name
        else:
            self._user = user

    @property
    def movie(self):
        return self._movie

    @movie.setter
    def movie(self, movie: Movie):
        if type(movie) is Movie:
            self._movie = movie

    @property
    def review_text(self):
        return self._text

    @review_text.setter
    def review_text(self, text: str):
        if type(text) is str:
            self._text = text

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating: float):
        if type(rating) not in (int, float) or not 0 <= rating <= 10:
            self._rating = None
        else:
            self._rating = rating

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        if type(timestamp) is datetime:
            self._timestamp = timestamp

    def formatted_time(self):
        return self._timestamp.strftime("%d %b %Y at %I:%M%p")

    def __repr__(self):
        return f'<Review of {self._movie.title} ({self._movie.year}): {self._rating} - "{self._text}">'

    def __eq__(self, other):
        if not isinstance(other, Review): return False
        return self.movie == other.movie and self.review_text == other.review_text and self.rating == other.rating and \
               self.timestamp == other.timestamp
