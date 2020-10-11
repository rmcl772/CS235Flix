from flask import Blueprint, session, url_for, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps
import CS235Flix.auth.services as services
import CS235Flix.adapters.memory_repository as repo

auth_blueprint = Blueprint("auth_bp", __name__)


class PasswordValid:
    def __init__(self, msg=None):
        if not msg:
            msg = "Password requires at least 8 characters, must have at least one of each: uppercase, lowercase, digit"
        self.message = msg

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()

        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Please enter a username"),
                                        Length(min=3, message="Username is too short!")],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [DataRequired(message="Please enter a password"), PasswordValid()],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    errors = {
        "username": None,
        "password": None
    }

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data)
            return redirect(url_for("auth_bp.login"))
        except services.NameTakenException:
            errors["username"] = "This username is already in use"

    return render_template("auth/credentials.html",
                           repo=repo.repo_instance,
                           form=form,
                           form_type="Register",
                           errors=errors,
                           handler_url=url_for("auth_bp.register"))


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Please enter a username")],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [DataRequired(message="Please enter a password")],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = {
        "username": None,
        "password": None
    }

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data)
            services.auth_user(user, form.password.data)

            redirect_url = None
            if "redirect_url" in session:
                redirect_url = session["redirect_url"]

            review_text, rating = None, None
            if "review_text" in session:
                review_text = session["review_text"]
                rating = session["rating"]

            session.clear()
            session['username'] = user.user_name

            if review_text:
                session["review_text"] = review_text
                session["rating"] = rating

            if redirect_url is not None:
                return redirect(redirect_url)
            return redirect(url_for('home_bp.home'))

        except services.InvalidUserException:
            errors["username"] = f"User '{form.username.data}' does not exist! Click here to register"
        except services.IncorrectPasswordException:
            errors["password"] = "Incorrect password!"

    return render_template("auth/credentials.html",
                           repo=repo.repo_instance,
                           form=form,
                           form_type="Login",
                           errors=errors,
                           handler_url=url_for("auth_bp.login"))


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)

    return wrapped_view
