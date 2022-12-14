from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.movie_model import Movie
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if User.validate_session():
        return redirect ("/dashboard")
    else:
        return render_template("login.html")
    
@app.route('/register')
def register():
    if User.validate_session():
        return redirect ("/dashboard")
    else:
        return render_template("register.html")

@app.route("/user/new", methods=["POST"])
def create_user():
    if User.validate_register(request.form) == True:
        data = {
            "email" : request.form ['email']
        }
        result = User.get_one_by_email ( data )

        if result == None:
            data = {
                "email" : request.form ['email'],
                "first_name" : request.form['first_name'],
                "last_name" : request.form['last_name'],
                "password" : bcrypt.generate_password_hash( request.form['password'])
            }
            user_id = User.create(data)
            session['email'] = request.form['email']
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['user_id'] = user_id
            return redirect("/dashboard")

        else:
            flash("That email already exists.", "error_register_email")
            return redirect("/register")

    else:
        return redirect("/register")

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email" : request.form['email']
    }
    result = User.get_one_by_email(data)

    if result == None:
        flash ("Account not found in our system", "error_login")
        return redirect("/")
    else:
        if not bcrypt.check_password_hash(result.password, request.form['password']):
            flash("Password invalid.", "error_login")
            return redirect("/")
        else:
            session['email'] = result.email
            session['first_name'] = result.first_name
            session['last_name'] = result.last_name
            session['user_id'] = result.id
            return redirect("/dashboard")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/join/movie", methods=['POST'])
def join_movie():
    data = {
        'user_id': request.form['user_id'],
        'movie_id': request.form['movie_id']
    }
    User.add_favorite(data)
    return redirect(f"/user/{request.form['user_id']}")