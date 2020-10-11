from typing import List
from bisect import insort
from os.path import join
from CS235Flix.adapters.repository import AbstractRepo
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.review import Review
from CS235Flix.domainmodel.user import User
import csv
from random import choices
from os import environ
import requests

repo_instance = None


class MemoryRepo(AbstractRepo):
    def __init__(self, user_file, reviews_file):
        # for adding more users / reviews after initialisation
        self._user_file = user_file
        self._review_file = reviews_file

        self._movies = list()
        self._movies_index = dict()
        self._users = list()
        self._actors = list()
        self._genres = list()
        self._directors = list()
        self._reviews = list()

    def add_actor(self, actor: Actor):
        if not isinstance(actor, Actor): return
        if actor not in self._actors:
            insort(self._actors, actor)

    def get_actor(self, actor_full_name: str) -> Actor:
        return next((actor for actor in self._actors if actor.actor_full_name == actor_full_name), None)

    def get_all_actors(self) -> List[Actor]:
        return self._actors

    def add_director(self, director: Director):
        if not isinstance(director, Director): return
        if director not in self._directors:
            insort(self._directors, director)

    def get_director(self, director_name: str) -> Director:
        return next((director for director in self._directors if director.director_full_name == director_name), None)

    def get_all_directors(self) -> List[Director]:
        return self._directors

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre): return
        if genre not in self._genres:
            insort(self._genres, genre)

    def get_all_genres(self) -> List[Genre]:
        return self._genres

    def add_movie(self, movie: Movie):
        if not isinstance(movie, Movie): return
        insort(self._movies, movie)
        self._movies_index[str(movie.id)] = movie

    def get_movie(self, movie_id: int or str) -> Movie:
        return self._movies_index[str(movie_id)]

    def get_movies_by_title(self, title: str) -> List[Movie]:
        title = title.lower()
        return [movie for movie in self._movies if movie.title.lower() == title]

    def get_movies_by_year(self, year: int or str) -> List[Movie]:
        if isinstance(year, str): year = int(year)
        return [movie for movie in self._movies if movie.year == year]

    def get_movies_by_actor(self, actor: Actor) -> List[Movie]:
        return [movie for movie in self._movies if actor in movie.actors]

    def get_movies_by_director(self, director: Director) -> List[Movie]:
        return [movie for movie in self._movies if movie.director == director]

    def get_movies_by_genre(self, genre: Genre) -> List[Movie]:
        return [movie for movie in self._movies if genre in movie.genres]

    def get_popular_movies(self, count: int = 3) -> List[Movie]:
        popular = sorted(self._movies, key=lambda movie: movie.external_rating if movie.external_rating else
                         1 * movie.metascore if movie.metascore else 1)[-100:]

        return choices(popular, k=count)

    def add_user(self, user: User, from_file=False):
        if not isinstance(user, User): return
        insort(self._users, user)

        if not from_file:
            self.update_files(users=True)

    def get_user(self, username: str) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_review(self, review: Review, from_file=False):
        if not isinstance(review, Review): return
        if review not in self._reviews:
            if review.id is None:
                review.id = len(self._reviews)
            self._reviews.append(review)

        if not from_file:
            self.update_files(users=True, reviews=True)

    def get_reviews_of_movie(self, movie: Movie) -> List[Review]:
        return [review for review in self._reviews if review.movie == movie]

    def movie_review_count(self, movie):
        return len(self.get_reviews_of_movie(movie))

    def get_review(self, review_id: int) -> Review:
        return next((review for review in self._reviews if review.id == review_id), None)

    def update_files(self, users=False, reviews=False):
        """ Updates the data files with the current repo data
            This is just so entries are persistent for this project, this wouldn't be needed with a database """

        if users:
            with open(self._user_file, "w") as users_file:
                fields = ["Name", "Password", "Reviews", "Watchlist", "Watched Movies"]
                users = csv.DictWriter(users_file, fieldnames=fields)
                users.writeheader()

                for user in self._users:
                    users.writerow({
                        "Name": user.user_name,
                        "Password": user.password,
                        "Reviews": ",".join([str(review.id) for review in user.reviews]),
                        "Watchlist": ",".join([str(movie.id) for movie in user.watchlist]),
                        "Watched Movies": ",".join([str(movie.id) for movie in user.watched_movies])
                    })

        if reviews:
            with open(self._review_file, "w") as reviews_file:
                fields = ["Movie id", "Text", "Rating", "User", "Timestamp", "id"]
                reviews = csv.DictWriter(reviews_file, fieldnames=fields)
                reviews.writeheader()

                for review in self._reviews:
                    reviews.writerow({
                        "Movie id": review.movie.id,
                        "Text": review.review_text,
                        "Rating": review.rating,
                        "User": review.user,
                        "Timestamp": review.timestamp.strftime("%Y-%m-%d_%H-%M-%S"),
                        "id": review.id
                    })


def init_repo(data_dir: str):
    reviews_file = join(data_dir, "reviews.csv")
    users_file = join(data_dir, "users.csv")

    repo = MemoryRepo(users_file, reviews_file)

    # movies
    movie_id = 0
    movies_file = join(data_dir, "Data1000Movies.csv")

    if environ["REFRESH_OMDB_POSTERS"] == "False":
        print("To refresh / update the posters from OMDB, set REFRESH_OMDB_POSTERS in the .env file to True")

    with open(movies_file, "r") as movies:
        data_list = list(csv.DictReader(movies))

    with open(movies_file, "r") as movies:
        movie_data = csv.DictReader(movies)
        updated = False

        # initialise movie with given data
        for i, item in enumerate(movie_data):
            movie = Movie(item["Title"], int(item["Year"]), movie_id)
            movie_id += 1

            # add genres to both movie and repo
            genres = item["Genre"].split(",")
            for genre in genres:
                genre = Genre(genre)
                repo.add_genre(genre)
                movie.add_genre(genre)

            # add director to both movie and repo
            director = Director(item["Director"])
            movie.director = director
            repo.add_director(director)

            # add actors to both movie and repo
            actors = item["Actors"].split(",")
            for actor in actors:
                actor = Actor(actor)
                repo.add_actor(actor)
                movie.add_actor(actor)

            # other movie data
            movie.description = item["Description"]
            movie.runtime_minutes = int(item["Runtime (Minutes)"])
            movie.external_rating = float(item["Rating"]) if item["Rating"] != "N/A" else None
            movie.rating_votes = int(item["Votes"]) if item["Votes"] != "N/A" else None
            movie.revenue = float(item["Revenue (Millions)"]) if item["Revenue (Millions)"] != "N/A" else None
            movie.metascore = int(item["Metascore"]) if item["Metascore"] != "N/A" else None

            if environ["REFRESH_OMDB_POSTERS"] == "True":
                if item["Poster url"] in (None, ""):
                    # movie poster form OMDB
                    print(f"Getting poster for {movie.title}")

                    api_key = environ["OMDB_KEY"]
                    data = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&t={movie.title}").json()

                    try:
                        movie.poster_url = data["Poster"]
                        data_list[i]["Poster url"] = data["Poster"]
                        updated = True
                    except KeyError:
                        print(f"Couldn't get poster for {movie.title}!")

                else:
                    movie.poster_url = item["Poster url"]

            movie.poster_url = item["Poster url"]

            repo.add_movie(movie)

    if updated:
        with open(join(data_dir, "Data1000Movies.csv"), "w") as movies:
            fields = ["Rank", "Title", "Genre", "Description", "Director", "Actors", "Year", "Runtime (Minutes)",
                      "Rating", "Votes", "Revenue (Millions)", "Metascore", "Poster url"]

            movie_data = csv.DictWriter(movies, fieldnames=fields)
            movie_data.writeheader()

            for movie in data_list:
                movie_data.writerow(movie)

    # reviews
    with open(reviews_file, "r") as reviews:
        reviews_data = csv.DictReader(reviews)

        for item in reviews_data:
            review = Review(repo.get_movie(int(item["Movie id"])),
                            item["Text"],
                            float(item["Rating"]),
                            item["User"],
                            item["Timestamp"],
                            int(item["id"])
                            )

            repo.add_review(review, from_file=True)

    # users
    with open(users_file, "r") as users:
        users_data = csv.DictReader(users)

        for item in users_data:
            user = User(item["Name"], item["Password"])

            for review_id in item["Reviews"].split(","):
                if review_id == "": break
                user.add_review(repo.get_review(int(review_id)))

            for movie_id in item["Watchlist"].split(","):
                if movie_id == "": break
                user.watchlist.add_movie(repo.get_movie(int(movie_id)))

            for movie_id in item["Watched Movies"].split(","):
                if movie_id == "": break
                user.watch_movie(repo.get_movie(int(movie_id)))

            repo.add_user(user, from_file=True)

    return repo
