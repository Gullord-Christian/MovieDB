from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
from flask_app.models.movie_model import Movie
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one( cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) > 0:
            return cls( result [0] )
        else:
            return None

    @classmethod
    def get_one_by_email( cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) > 0:
            return cls( result [0] )
        else:
            return None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password)"
        query += "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_with_movies(cls, data):
        query = "SELECT * FROM users JOIN movies ON users.id = moviess.user_id WHERE users.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len (result) > 0:
            current_user = cls(result[0])
            movie_list = []
            for row in result:
                current_movie = {
                    "id": row["movies.id"],
                    "title" : row["title"],
                    "genre" : row["genre"],
                    "year" : row["year"],
                    "review" : row["review"],
                    "you_should_watch" : row["you_should_watch"],
                    "rating" : row["rating"],
                    "user_id" : row["user_id"],
                    "created_at" : row['created_at'],
                    "updated_at" : row['updated_at'],
                }
                movie = Movie(current_movie)
                movie_list.append(movie)
            current_user.movie_list = movie_list
            return current_user
        return None


    @staticmethod
    def validate_login(data):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) >= 1:
            flash("Email is not found.")
            isValid = False
        return isValid


    @staticmethod
    def validate_register(data):
        isValid = True

        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid.", "error_register_email")
            isValid = False

        if len(data['first_name']) < 2:
            isValid = False
            flash("Please provide your first name. Must be at least 3 characters", "error_register_first_name") 
        
        if len(data['last_name']) < 2:
            isValid = False
            flash("Please provide your last name. Must be at least 3 characters", "error_register_last_name") 

        if data['email'] == "":
            isValid = False
            flash("Please provide your email.", "error_register_email")
    
        if data['password'] == "":
            isValid = False
            flash("Please provide a password, must be at least 8 characters.", "error_register_password")

        if data['password_confirmation'] == "":
            isValid = False
            flash("Please provide a password confirmation.", "error_register_password_confirmation")

        if data['password'] != data['password_confirmation']:
            isValid = False
            flash("Your passwords do not match.", "error_register_password_confirmation")

        return isValid
    
    @staticmethod
    def validate_session():
        ## only need to validate one of the provided 
        if "user_id" in session:
            return True
        else:
            return False

