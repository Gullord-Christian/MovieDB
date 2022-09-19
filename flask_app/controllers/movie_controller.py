from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.movie_model import Movie
from flask_app.models.user_model import User



@app.route ("/dashboard")
def get_movies():
    if User.validate_session():
        movies = Movie.get_all()
        return render_template("dashboard.html", movies = movies)
    else:
        return redirect("/")

@app.route("/new/movie")
def display_movie():
    if User.validate_session():
        return render_template("add_movie.html")
    else:
        return redirect("/")

@app.route ("/new/movie", methods = ["POST"])
def create_movie():
    if not Movie.validate_movie(request.form):
        return redirect ("/new/movie")
    data = {
        "title" : request.form['title'],
        "genre" : request.form['genre'],
        "year" : request.form['year'],
        "review" : request.form['review'], 
        "you_should_watch" : request.form['you_should_watch'],
        "rating" : request.form['rating'],
        "trailer" : request.form['trailer'],
        "user_id" : session['user_id'],
    }
    Movie.create(data)
    return redirect("/dashboard")

@app.route("/view/movie/<int:id>")
def movie_get_one(id):
    if User.validate_session():
        data = {
            'id' : id
        }
        movies = Movie.get_one(data)
        return render_template("view_movie.html", movies = movies)
    else:
        return redirect("/")

@app.route("/delete/movie/<int:id>")
def delete(id):
    data = {
        'id' : id
    }
    Movie.delete(data)
    return redirect("/dashboard")

@app.route("/edit/movie/<int:id>")
def get_one_movie(id):
    if User.validate_session():
        data = {
            "id" : id
        }
        movies = Movie.get_one(data)
        return render_template("edit_movie.html", movies = movies)
    else:
        return redirect("/")

@app.route("/edit/movie/<int:id>", methods=["POST"])
def edit_movie (id):
    if Movie.validate_movie(request.form) == True:
        data = {
        "id" : id,
        'title' : request.form['title'],
        'genre' : request.form['genre'],
        'year' : request.form['year'],
        "review" : request.form['review'],
        "you_should_watch" : request.form['you_should_watch'],
        "trailer" : request.form['trailer'],
        "rating" : request.form['rating'],
        }
        Movie.update_one(data)
        return redirect("/dashboard")
    else:
        return redirect(f"/edit/movie/{id}")

@app.route("/join/user", methods=['POST'])
def join_user():
    data = {
        'user_id': request.form['user_id'],
        'movie_id': request.form['movie_id']
    }
    User.add_favorite(data)
    return redirect(f"/movies/{request.form['movie_id']}")