import pytest
import csv
import os
from CS235Flix.adapters.memory_repository import MemoryRepo
from CS235Flix.domainmodel.actor import Actor
from CS235Flix.domainmodel.director import Director
from CS235Flix.domainmodel.genre import Genre
from CS235Flix.domainmodel.movie import Movie
from CS235Flix.domainmodel.user import User
from CS235Flix.domainmodel.review import Review


def create_repo_data():
    movie_data_file = os.path.join(os.getcwd(), "data", "Data1000Movies.csv")
    user_data_file = os.path.join(os.getcwd(), "data", "users.csv")
    review_data_file = os.path.join(os.getcwd(), "data", "reviews.csv")
    if not os.path.exists(movie_data_file):
        movie_data_file = os.path.join(os.getcwd(), "tests", "data", "Data1000Movies.csv")
        user_data_file = os.path.join(os.getcwd(), "tests", "data", "users.csv")
        review_data_file = os.path.join(os.getcwd(), "tests", "data", "reviews.csv")

    movies = []
    actors = []
    directors = []
    genres = []
    reviews = []
    users = []

    with open(movie_data_file, "r") as data:
        movie_data = csv.DictReader(data)
        for row in movie_data:
            if len(movies) > 5: break

            movie_director = Director(row["Director"])
            movie_actors = [Actor(actor) for actor in row["Actors"].split(",")]
            movie_genres = [Genre(genre) for genre in row["Genre"].split(",")]

            movie = Movie(row["Title"], int(row["Year"]), len(movies))

            movie.director = movie_director
            directors.append(movie_director)

            movie.actors = movie_actors
            actors.extend(movie_actors)

            movie.genres = movie_genres
            genres.extend(movie_genres)

            movie.description = row["Description"]
            movie.runtime_minutes = int(row["Runtime (Minutes)"])
            movie.external_rating = float(row["Rating"])
            movie.rating_votes = int(row["Votes"])
            movie.revenue = float(row["Revenue (Millions)"])
            movie.metascore = int(row["Metascore"])

            movies.append(movie)

    with open(review_data_file, "r") as data:
        review_data = csv.DictReader(data)
        for row in review_data:
            movie = movies[int(row["Movie id"])]
            text = row["Text"]
            rating = float(row["Rating"])
            user = row["User"]
            timestamp = row["Timestamp"]
            review_id = int(row["id"])

            reviews.append(Review(movie, text, rating, user, timestamp, review_id))

    with open(user_data_file, "r") as data:
        user_data = csv.DictReader(data)
        for row in user_data:
            user = User(row["Name"], row["Password"])

            if row["Reviews"] not in (None, ""):
                for review in row["Reviews"].split(","):
                    user.add_review(reviews[int(review)])

            users.append(user)

    # remove duplicate genres
    genres = list(set(genres))

    return movies, actors, directors, genres, users, reviews, user_data_file, review_data_file


def test_actor():
    movies, actors, directors, genres, users, reviews, user_file, review_file = create_repo_data()

    repo = MemoryRepo(user_file, review_file)
    for actor in actors:
        repo.add_actor(actor)

    # all actors were successfully added
    assert len(repo.get_all_actors()) == len(actors)

    # duplicate actor ignored
    repo.add_actor(actors[0])
    assert len(repo.get_all_actors()) == len(actors)

    # incorrect type ignored
    repo.add_actor(Director("Shouldn't be added"))
    assert directors[0] not in repo.get_all_actors()

    # successful retrieval of actor in repo
    retrieved_actor = repo.get_actor(actors[0].actor_full_name)
    assert retrieved_actor == actors[0]

    # retrieval of actor not in repo returns None
    retrieved_actor = repo.get_actor("Not in repo")
    assert retrieved_actor is None


def test_director():
    movies, actors, directors, genres, users, reviews, user_file, review_file = create_repo_data()

    repo = MemoryRepo(user_file, review_file)
    for director in directors:
        repo.add_director(director)

    # all directors were successfully added
    assert len(repo.get_all_directors()) == len(directors)

    # duplicate director ignored
    repo.add_director(directors[0])
    assert len(repo.get_all_directors()) == len(directors)

    # incorrect type ignored
    repo.add_director(Actor("Shouldn't be added"))
    assert actors[0] not in repo.get_all_directors()

    # successful retrieval of director in repo
    retrieved_director = repo.get_director(directors[0].director_full_name)
    assert retrieved_director == directors[0]

    # retrieval of director not in repo returns None
    retrieved_director = repo.get_director("Not in repo")
    assert retrieved_director is None


def test_genre():
    movies, actors, directors, genres, users, reviews, user_file, review_file = create_repo_data()

    repo = MemoryRepo(user_file, review_file)
    for genre in genres:
        repo.add_genre(genre)

    # all genres were successfully added
    assert len(repo.get_all_genres()) == len(genres)

    # duplicate genre ignored
    repo.add_genre(genres[0])
    assert len(repo._genres) == len(genres)

    # incorrect type ignored
    repo.add_actor(Director("Shouldn't be added"))
    assert directors[0] not in repo.get_all_genres()

    # successful retrieval of genres, order does not matter
    retrieved_genres = repo.get_all_genres()
    assert len(retrieved_genres) == len(genres)
    assert all([genre in retrieved_genres for genre in genres])


def test_movie():
    movies, actors, directors, genres, users, reviews, user_file, review_file = create_repo_data()

    repo = MemoryRepo(user_file, review_file)
    for movie in movies:
        repo.add_movie(movie)

    # repo should ignore invalid additions
    assert len(repo._movies) == len(movies)
    repo.add_movie(Director("Shouldn't be added"))
    assert len(repo._movies) == len(movies)

    # get a specific movie by its id
    retrieved_by_id = repo.get_movie('2')
    assert retrieved_by_id == movies[2]

    # requesting a nonexistent id returns None
    retrieved_by_id = repo.get_movie('100')
    assert retrieved_by_id is None

    temp_movie = Movie("Sing", 2012, 6)
    temp_movie.add_actor(Actor("Chris Pratt"))
    temp_movie.director = Director("James Gunn")
    temp_movie.add_genre(Genre("Action"))
    repo.add_movie(temp_movie)

    # get all movies with a specific title
    retrieved_by_title = repo.get_movies_by_title("Sing")
    assert len(retrieved_by_title) == 2
    assert all([movie.title == "Sing" for movie in retrieved_by_title])
    assert temp_movie in retrieved_by_title

    # get all movies from a specific year
    retrieved_by_year = repo.get_movies_by_year(2012)
    assert len(retrieved_by_year) == 2
    assert all([movie.year == 2012 for movie in retrieved_by_year])
    assert temp_movie in retrieved_by_year

    # get all movies from a specific year, input is string
    retrieved_by_year = repo.get_movies_by_year("2012")
    assert len(retrieved_by_year) == 2
    assert all([movie.year == 2012 for movie in retrieved_by_year])
    assert temp_movie in retrieved_by_year

    # get all movies with a specific actor
    retrieved_by_actor = repo.get_movies_by_actor(Actor("Chris Pratt"))
    assert len(retrieved_by_actor) == 2
    assert all([Actor("Chris Pratt") in movie.actors for movie in retrieved_by_actor])
    assert temp_movie in retrieved_by_actor

    # get all movies directed by a specific director
    retrieved_by_director = repo.get_movies_by_director(Director("James Gunn"))
    assert len(retrieved_by_director) == 2
    assert all([movie.director == Director("James Gunn") for movie in retrieved_by_director])
    assert temp_movie in retrieved_by_director

    # get all movies in a specific genre
    retrieved_by_genre = repo.get_movies_by_genre(Genre("Action"))
    assert len(retrieved_by_genre) == 4
    assert all([Genre("Action") in movie.genres for movie in retrieved_by_genre])
    assert temp_movie in retrieved_by_genre


def test_user():
    movies, actors, directors, genres, users, reviews, user_file, review_file = create_repo_data()

    repo = MemoryRepo(user_file, review_file)
    for movie in movies:
        repo.add_movie(movie)

    for user in users:
        repo.add_user(user)

    # users were added correctly
    assert len(repo._users) == len(users)

    # repo ignores invalid user input
    repo.add_user(reviews[0])
    assert reviews[0] not in repo._users

    # repo does not duplicate users
    repo.add_user(users[0])
    assert len(repo._users) == len(users)

    # repo retrieves user by name
    user = repo.get_user("user1")
    assert user == users[0]

    # nonexistent user returns None
    user = repo.get_user("Nonexistent")
    assert user is None


def test_review():
    movies, actors, directors, genres, users, reviews, user_file, review_file = create_repo_data()

    repo = MemoryRepo(user_file, review_file)
    for movie in movies:
        repo.add_movie(movie)

    for user in users:
        repo.add_user(user)

    for review in reviews:
        repo.add_review(review)

    # reviews were added correctly
    assert len(repo._reviews) == len(reviews)

    # repo ignores invalid input
    repo.add_review(users[0])
    assert users[0] not in repo._reviews

    # repo doesn't duplicate reviews
    repo.add_review(reviews[0])
    assert len(repo._reviews) == len(reviews)

    # repo gets all reviews of movie
    retrieved_reviews = repo.get_reviews_of_movie(movies[1])
    assert len(retrieved_reviews) == 2
    assert all([review.movie == movies[1] for review in retrieved_reviews])

    # repo gets review by id
    retrieved_review = repo.get_review(2)
    assert retrieved_review == reviews[2]
