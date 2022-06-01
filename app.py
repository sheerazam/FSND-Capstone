from crypt import methods
import os
from shutil import move
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc, true
import json
from flask_cors import CORS
import sys

from models import Movie, Actor, db_drop_and_create_all, setup_db
from auth import AuthError, requires_auth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask

# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/casting_agency'
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# app = Flask(__name__)
# moment = Moment(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# app = Flask(__name__)
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    '''
    @DONE uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this function will add one
    '''
    # db_drop_and_create_all()

    # ROUTES

    '''
    @DONE implement endpoint
        GET /actors
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            return jsonify({
                'success': True,
                'actors': [actor.short() for actor in actors]
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)

    '''
    @DONE implement endpoint
        GET /actors-detail
            it should require the 'get:actor-detail' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actor": actor} where actor is actor details
    '''
    @app.route('/actors-detail/<int:actor_id>', methods=['GET'])
    @requires_auth("get:actor-details")
    def get_actor_details(payload, actor_id):    
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor:
            return jsonify({
                'success': True,
                'actor': actor.long()
            }), 200
        else:
            print(f'Error: {sys.exc_info()[0]}')
            abort(404)


    '''
    @DONE implement endpoint
        POST /actors
            it should create a new row in the actors table
            it should require the 'post:actors' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actors": actor} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth("create:actor")
    def post_actor(payload):
        body = request.get_json()
        if body is None:
            abort(400)
        if 'name' not in body:
            abort(400)
        if 'age' not in body:
            abort(400)
        if 'gender' not in body:
            abort(400)
        try:
            actor = Actor(name=body['name'], age=body['age'], gender = body['gender'])
            actor.insert()

            return jsonify({
                'success': True,
                'actors': actor.id
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)

    '''
    @DONE implement endpoint
        PATCH /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actors' permission
            it should contain the actors.long() data representation
        returns status code 200 and json {"success": True, "actors": actor} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def patch_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        body = request.get_json()
        if actor is None:
            abort(404)
        if body is None:
            abort(400)
        if 'name' in body:
            actor.name = body['name']
        if 'age' in body:
            actor.age = body['age']
        if 'gender' in body:
            actor.gender = body['gender']
        try:
            actor.update()
            return jsonify({
                'success': True,
                'actors': [actor.long()]
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)

    '''
    @DONE implement endpoint
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)

    '''
    @DONE implement endpoint
        GET /movies
            it should be a public endpoint
            it should contain only the movies.short() data representation
        returns status code 200 and json {"success": True, "movies": actors} where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.short() for movie in movies]
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)


    '''
    @DONE implement endpoint
        GET /movie-detail
            it should require the 'get:movie-detail' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movie": movie} where movie is movie details
    '''
    @app.route('/movie-detail/<int:movie_id>', methods=['GET'])
    @requires_auth("get:movie-details")
    def get_movie_details(payload, movie_id):    
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie:
            return jsonify({
                'success': True,
                'movie': movie.long()
            }), 200
        else:
            print(f'Error: {sys.exc_info()[0]}')
            abort(404)


    '''
    @DONE implement endpoint
        POST /movies
            it should create a new row in the movie table
            it should require the 'post:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movie": movie} where movie an array containing only the newly created movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth("create:movie")
    def post_movie(payload):
        body = request.get_json()
        if body is None:
            abort(400)
        if 'title' not in body:
            abort(400)
        if 'release_date' not in body:
            abort(400)
        if 'cast' not in body:
            abort(400)

        try:
            movie = Movie(title=body['title'], release_date=body['release_date'])
            actors = Actor.query.filter(Actor.name.in_(body['cast'])).all()
            movie.cast = actors
            movie.insert()
            return jsonify({
                'success': True,
                'movies': movie.id
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)

    '''
    @DONE implement endpoint
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission
            it should contain the movies.long() data representation
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def patch_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(400)
        if 'title' in body:
            movie.title = body['title']
        if 'release_date' in body:
            movie.release_date = body['release_date']

        if 'cast' in body:
            actors = Actor.query.filter(Actor.name.in_(body['cast'])).all()
            movie.cast = actors

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': [movie.short()]
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)


    '''
    @DONE implement endpoint
        DELETE /movie/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            }), 200
        except:
            print(f'Error: {sys.exc_info()[0]}')
            abort(422)


    '''
    @DONE implement endpoint
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''

    '''
    Error handling for unprocessable entity
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    '''
    @DONE implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    '''
    @DONE implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    '''
    @DONE implement error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()
if __name__ == "__main__":
        app.debug = True
        app.run()

# if __name__ == "__main__":
#     app.debug = True
#     app.run()
