from flask import Blueprint, render_template, redirect, url_for, session
import CS235Flix.adapters.memory_repository as repo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from CS235Flix.auth.auth import login_required
from CS235Flix.domainmodel.review import Review


movie_blueprint = Blueprint("movie_bp", __name__)


class ReviewForm(FlaskForm):
    review_text = StringField("", validators=[DataRequired(message="Review must contain text")],
                              render_kw={"placeholder": "Write a review..."})
    rating = IntegerField("", validators=[DataRequired("Rating must be a number 0 - 10"),
                                          NumberRange(min=0, max=10, message="Rating must be a number between 0 and 10")],
                          render_kw={"placeholder": "Rating"})
    submit = SubmitField("Review")


@movie_blueprint.route("/movie/<movie_id>", methods=["GET", "POST"])
def movie(movie_id):
    selected_movie = repo.repo_instance.get_movie(int(movie_id))
    movie_reviews = repo.repo_instance.get_reviews_of_movie(selected_movie)

    review_form = ReviewForm()

    session["redirect_url"] = url_for("movie_bp.movie", movie_id=movie_id)

    if review_form.validate_on_submit():
        session["review_text"] = review_form.review_text.data
        session["rating"] = review_form.rating.data
        session["redirect_url"] = url_for("movie_bp.submit_review", movie_id=movie_id)
        return redirect(url_for("movie_bp.submit_review", movie_id=movie_id))

    return render_template("movie/movie.html",
                           repo=repo.repo_instance,
                           form=review_form,
                           movie=selected_movie,
                           movie_reviews=movie_reviews,
                           title=selected_movie.title)


@movie_blueprint.route("/movie/<movie_id>/submit_review", methods=["GET", "POST"])
@login_required
def submit_review(movie_id):
    user = repo.repo_instance.get_user(session["username"])
    reviewed_movie = repo.repo_instance.get_movie(movie_id)

    review = Review(reviewed_movie, session["review_text"], session["rating"], user.user_name)

    user.add_review(review)
    repo.repo_instance.add_review(review)

    del session["review_text"]
    del session["rating"]

    return redirect(url_for("movie_bp.movie", movie_id=movie_id))


@movie_blueprint.route("/movie/<movie_id>/add_to_watchlist", methods=["GET"])
@login_required
def add_to_watchlist(movie_id):
    user = repo.repo_instance.get_user(session['username'])
    selected_movie = repo.repo_instance.get_movie(movie_id)

    user.watchlist.add_movie(selected_movie)

    repo.repo_instance.update_files(users=True)

    return redirect(url_for("movie_bp.movie", movie_id=movie_id))


@movie_blueprint.route("/movie/<movie_id>/remove_from_watchlist", methods=["GET"])
@login_required
def remove_from_watchlist(movie_id):
    user = repo.repo_instance.get_user(session['username'])
    selected_movie = repo.repo_instance.get_movie(movie_id)

    user.watchlist.remove_movie(selected_movie)

    repo.repo_instance.update_files(users=True)

    return redirect(url_for("movie_bp.movie", movie_id=movie_id))

