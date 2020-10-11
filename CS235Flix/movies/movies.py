from flask import Blueprint, request, render_template, redirect, url_for
import CS235Flix.adapters.memory_repository as repo
from .services import grid_layout, alphabetical_list


movies_blueprint = Blueprint("movies_bp", __name__)


@movies_blueprint.route("/movies", methods=["GET"])
def movies():
    search_by = request.args.get("search_by").lower()
    query = request.args.get("query").lower()

    if search_by == "year":
        matching_movies = repo.repo_instance.get_movies_by_year(query)
        title = f"Movies from {query}"
    elif search_by == "genre":
        matching_movies = repo.repo_instance.get_movies_by_genre(query)
        title = f"{query.capitalize()} movies"
    elif search_by == "director":
        matching_movies = repo.repo_instance.get_movies_by_director(query)
        title = f"Movies by {query.capitalize()}"
    elif search_by == "actor":
        matching_movies = repo.repo_instance.get_movies_by_actor(query)
        title = f"Movies featuring {query.capitalize()}"
    elif search_by == "title":
        matching_movies = repo.repo_instance.get_movies_by_title(query)
        title = f"Movies called {query.capitalize()}"
    else:
        raise ValueError

    if len(matching_movies) == 0 and search_by in ("genre", "actor", "director"):
        return redirect(url_for("movies_bp.category", cat=search_by, query=query))

    if len(matching_movies) == 1:
        movie_id = matching_movies[0].id
        return redirect(url_for(f"movie_bp.movie", movie_id=movie_id))

    movie_grid = grid_layout(matching_movies, 3)

    return render_template("movies/movies.html", repo=repo.repo_instance, movies=movie_grid, title=title)


@movies_blueprint.route("/category/<cat>", methods=["GET"])
def category(cat):
    search_query = request.args.get("query")

    file = None

    formatted_data = None
    if cat == "genre":
        formatted_data = grid_layout(repo.repo_instance.get_all_genres(), 3)
        file = "genre"

    elif cat == "actor":
        formatted_data = alphabetical_list(repo.repo_instance.get_all_actors(), grid=4)
        file = "people"

    elif cat == "director":
        formatted_data = alphabetical_list(repo.repo_instance.get_all_directors(), grid=3)
        file = "people"

    if file is None:
        return redirect(url_for("home_bp.home"))

    return render_template(f"categories/{file}.html",
                           repo=repo.repo_instance,
                           data=formatted_data,
                           query=search_query,
                           type=cat)
