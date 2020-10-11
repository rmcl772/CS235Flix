from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import CS235Flix.adapters.memory_repository as repo


class MovieSearchForm(FlaskForm):
    query = StringField("", validators=[DataRequired()], render_kw={"placeholder": "search"})
    submit = SubmitField("Go")
    search_by = SelectField("", choices=["Title", "Year", "Genre", "Director", "Actor"])


home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route("/", methods=["get", "post"])
def home():
    search_form = MovieSearchForm()

    if search_form.validate_on_submit():
        query = search_form.query.data.lower()
        search_by = search_form.search_by.data.lower()

        return redirect(url_for("movies_bp.movies", search_by=search_by, query=query))

    return render_template("home/home.html", repo=repo.repo_instance, form=search_form)
