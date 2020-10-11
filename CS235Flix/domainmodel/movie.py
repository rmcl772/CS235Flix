from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.director import Director

class Movie:
    def __init__(self, title: str, year: int, id_num: int):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()

        if type(year) is int and year >= 1900:
            self._year = year
        else:
            self._year = None

        self._id = id_num
        self._description = None
        self._director = None
        self._actors = []
        self._genres = []
        self._runtime_minutes = None

        self._external_rating = None
        self._rating_votes = None
        self._revenue = None
        self._metascore = None

        self._poster_url = None

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year: int):
        if type(year) is int and year > 1900:
            self._year = year
        else:
            self._year = None

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        if description == "" or type(description) is not str:
            self._description = None
        else:
            self._description = description

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, director: Director):
        if type(director) is Director:
            self._director = director
        else:
            self._director = None

    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, actors: list):
        if type(actors) is list:
            for actor in actors:
                self.add_actor(actor)

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres: list):
        if type(genres) is list:
            for genre in genres:
                self.add_genre(genre)

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes: int):
        if type(runtime_minutes) is not int or runtime_minutes <= 0:
            raise ValueError
        else:
            self._runtime_minutes = runtime_minutes

    def runtime_formatted(self):
        hours = self._runtime_minutes // 60
        minutes = self._runtime_minutes % 60

        hours = f"{hours}h " if hours > 0 else ""

        return f"{hours}{minutes}m"

    @property
    def external_rating(self):
        return self._external_rating

    @external_rating.setter
    def external_rating(self, rating: float):
        if type(rating) in (float, int) and 0 <= rating <= 10:
            self._external_rating = rating

    @property
    def rating_votes(self):
        return self._rating_votes

    @rating_votes.setter
    def rating_votes(self, vote_count: int):
        if type(vote_count) is int and vote_count >= 0:
            self._rating_votes = vote_count

    @property
    def revenue(self):
        return self._revenue

    @revenue.setter
    def revenue(self, revenue: float):
        if type(revenue) is float and revenue >= 0:
            self._revenue = revenue

    @property
    def metascore(self):
        return self._metascore

    @metascore.setter
    def metascore(self, score: int):
        if type(score) is int and 0 <= score <= 100:
            self._metascore = score

    @property
    def poster_url(self):
        return self._poster_url

    @poster_url.setter
    def poster_url(self, url: str):
        self._poster_url = url

    def add_actor(self, actor: Actor):
        if type(actor) is Actor and actor not in self.actors:
            self._actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self._actors:
            self._actors.remove(actor)

    def add_genre(self, genre: Genre):
        if type(genre) is Genre and genre not in self._genres:
            self._genres.append(genre)

    def remove_genre(self, genre: Genre):
        if genre in self._genres:
            self._genres.remove(genre)

    def __repr__(self):
        return f"<Movie {self._title}, {self._year}>"

    def __eq__(self, other):
        return self.title == other.title and self.year == other.year

    def __lt__(self, other):
        if self.title == other.title:
            return self.year < other.year
        else:
            return sorted((self.title, other.title))[0] == self.title

    def __hash__(self):
        return hash(self._title + str(self._year))
