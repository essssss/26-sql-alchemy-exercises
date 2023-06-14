"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
app.app_context().push()
db.create_all()


@app.route("/")
def list_users():
    """show a list of users"""

    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/", methods=["POST"])
def create_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


@app.route("/form")
def show_form():
    """show a form to add a new user"""

    return render_template("form.html")


@app.route("/<int:user_id>")
def show_user(user_id):
    """show a user's details"""
    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)


@app.route("/<int:user_id>/edit")
def edit_user(user_id):
    """edit a user's details"""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)
