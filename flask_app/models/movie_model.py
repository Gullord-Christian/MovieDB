from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
from flask_app.models import user_model

class Movie: 
    def __init__ (self, data):
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.year = data['year']
        self.review = data['review']
        self.you_should_watch = data['you_should_watch']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO movies(title, genre, year, review, you_should_watch, rating, user_id)"
        query += "VALUES (%(title)s, %(genre)s, %(year)s, %(review)s, %(you_should_watch)s, %(rating)s, %(user_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movies JOIN users ON users.id = movies.user_id;"

        result = connectToMySQL(DATABASE).query_db(query)
        movies = []

        if len(result) > 0:
            for row in result:
                movie = cls(row)
                user_data = {
                    "id": row["users.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "email" : row["email"],
                    "password" : row["password"],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at'],
                }
                movie.created_by = user_model.User(user_data)
                movies.append(movie)
        return movies

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM movies JOIN users ON users.id = movies.user_id WHERE movies.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len (result) > 0:
            row = result[0]
            movie = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
            }
            movie.created_by = user_model.User(user_data)
            return movie
        else:
            return None

    @classmethod
    def get_from_user_id (cls, data):
        query = "SELECT * FROM movies WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        all_movies = []
        for row in results:
            all_movies.append(cls(row))
        return all_movies

    @classmethod
    def update_one (cls, data):
        query = "UPDATE movies SET title = %(title)s, genre = %(genre)s, year = %(year)s, review = %(review)s, you_should_watch = %(you_should_watch)s, rating = %(rating)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def get_movies_by_id(cls, data):
    #     query = "SELECT * FROM movies WHERE id in ($ids);"
    #     return connectToMySQL(DATABASE).query_db(query, data)


    @staticmethod
    def validate_movie(data):
        isValid = True

        if data['title']  == "":
            isValid = False
            flash("Title must be submitted", "error_title") 
        
        if data['genre'] == "":
            isValid = False
            flash("Must select genre", "error_genre") 

        if data['year'] == "":
            isValid = False
            flash("Must provide a year.", "error_year")

        if len(data['review']) < 10:
            isValid = False
            flash("Review must be at least 10 characters.", "error_review")

        if len(data['you_should_watch']) < 10:
            isValid = False
            flash("This must be at least 10 characters", "error_you_should_watch") 

        if data['rating'] == "":
            isValid = False
            flash("You must provide a rating.")

        return isValid