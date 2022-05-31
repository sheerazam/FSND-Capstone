from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask
import os

# database_name = "casting_agency.db"
# # database_path = "postgres://{}:{}@{}/{}".format(
# #     'postgres', 'root', 'localhost:5432', database_name)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# app = Flask(__name__)
# moment = Moment(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from crypt import methods
# import os
# from flask import Flask, request, jsonify, abort
# from sqlalchemy import exc, true
# import json
# from flask_cors import CORS
# import sys
# from . import Movie, Actor
# from auth.auth import AuthError, requires_auth

# app = Flask(__name__)
# # setup_db(app)
# CORS(app)

# '''
# @DONE uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this function will add one
# '''
# # db_drop_and_create_all()

# # ROUTES

# '''
# @DONE implement endpoint
#     GET /actors
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/actors', methods=['GET'])
# def get_actors():
#     try:
#         actors = Actor.query.all()
#         return jsonify({
#             'success': True,
#             'actors': [actor.short() for actor in actors]
#         }), 200
#     except:
#         abort(422)

# '''
# @DONE implement endpoint
#     GET /actors-detail
#         it should require the 'get:actor-detail' permission
#         it should contain the actor.long() data representation
#     returns status code 200 and json {"success": True, "actor": actor} where actor is actor details
# '''
# @app.route('/actors/<int:id>', methods=['GET'])
# def get_actor_details():
#     try:
#         actor = Actor.query.get(id)
#         if actor:
#             return jsonify({
#                 'success': True,
#                 'actor': actor.long()
#             }), 200
#         else:
#             abort(404)
#     except:
#         abort(422)

# '''
# @DONE implement endpoint
#     POST /actors
#         it should create a new row in the actors table
#         it should require the 'post:actors' permission
#         it should contain the actor.long() data representation
#     returns status code 200 and json {"success": True, "actors": actor} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/actors', methods=['POST'])
# def post_actor():
#     try:
#         body = request.get_json()
#         if body is None:
#             abort(400)
#         if 'name' not in body:
#             abort(400)
#         if 'age' not in body:
#             abort(400)
#         if 'gender' not in body:
#             abort(400)
#         actor = Actor(name=body['name'], age=body['age'], gender = body['gender'])
#         actor.insert()

#         return jsonify({
#             'success': True,
#             'actors': actor.id
#         }), 200
#     except:
#         abort(422)

# '''
# @DONE implement endpoint
#     PATCH /actors/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:actors' permission
#         it should contain the actors.long() data representation
#     returns status code 200 and json {"success": True, "actors": actor} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/actors/<int:id>', methods=['PATCH'])
# def patch_actor():
#     try:
#         actor = Actor.query.filter(Actor.id == id).one_or_none()
#         body = request.get_json()
#         if body is None:
#             abort(400)
#         if 'name' in body:
#             actor.name = body['name']
#         if 'age' in body:
#             actor.age = body['age']
#         if 'gender' in body:
#             actor.gender = body['gender']
#         actor.update()
#         return jsonify({
#             'success': True,
#             'actors': [actor.long()]
#         }), 200
#     except:
#         abort(422)

# '''
# @DONE implement endpoint
#     DELETE /actors/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:actors' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/actors/<int:id>', methods=['DELETE'])
# def delete_actor():
#     try:
#         actor = Actor.query.filter(Actor.id == id).one_or_none()
#         if actor is None:
#             abort(404)
#         actor.delete()
#         return jsonify({
#             'success': True,
#             'delete': id
#         }), 200
#     except:
#         abort(422)

# '''
# @DONE implement endpoint
#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''
# # @app.route('/drinks', methods=['GET'])
# # def get_drinks():
# #     try:
# #         drinks = Drink.query.all()
# #         drinks_short = [drink.short() for drink in drinks]
# #         return jsonify({
# #             'success': True,
# #             'drinks': drinks_short
# #         }), 200
# #     except:
# #         print(f'Error: {sys.exc_info()[0]}')
# #         abort(422)

# '''
# @DONE implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''
# # @app.route('/drinks-detail', methods=['GET'])
# # @requires_auth('get:drinks-detail')
# # def get_drinks_detail(payload):
# #     try:
# #         drinks = Drink.query.all()
# #         return jsonify({
# #             'success': True,
# #             'drinks': [drink.long() for drink in drinks]
# #         }), 200
# #     except:
# #         print(f'Error: {sys.exc_info()[0]}')
# #         abort(422)


# '''
# @DONE implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''
# # @app.route('/drinks', methods=['POST'])
# # @requires_auth('post:drinks')
# # def post_drinks(payload):
# #     # try:
# #         body = request.get_json()
# #         title = body.get('title', None)
# #         recipe = body.get('recipe', None)
# #         if title is None or recipe is None:
# #             abort(422)
# #         drink = Drink(title=title, recipe = """{}""".format(recipe))
# #         drink.insert()
# #         drink.recipe = recipe
# #         return jsonify({
# #             'success': True,
# #             'drinks': drink.id
# #         }), 200
#     # except:
#         # abort(422)


# '''
# @DONE implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''
# # @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
# # @requires_auth('patch:drinks')
# # def patch_drinks(payload, drink_id):
# #     try:
# #         drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
# #         if drink is None:
# #             abort(404)
# #         body = request.get_json()
# #         title = body.get('title', None)
# #         recipe = body.get('recipe', None)
# #         if title is not None:
# #             drink.title = title
# #         if recipe is not None:
# #             drink.recipe = json.dumps(recipe)
# #         drink.update()
# #         return jsonify({
# #             'success': True,
# #             'drinks': [drink.long()]
# #         }), 200
# #     except:
# #         abort(422)


# '''
# @DONE implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
# '''
# # @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
# # @requires_auth('delete:drinks')
# # def delete_drinks(payload, drink_id):
# #     try:
# #         drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
# #         if drink is None:
# #             abort(404)
# #         drink.delete()
# #         return jsonify({
# #             'success': True,
# #             'delete': drink_id
# #         }), 200
# #     except:
# #         abort(422)


# # Error Handling
# '''
# Example error handling for unprocessable entity
# '''

# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "unprocessable"
#     }), 422


# '''
# @DONE implement error handlers using the @app.errorhandler(error) decorator
#     each error handler should return (with approprate messages):
#              jsonify({
#                     "success": False,
#                     "error": 404,
#                     "message": "resource not found"
#                     }), 404

# '''
# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({
#         "success": False,
#         "error": 400,
#         "message": "bad request"
#     }), 400


# '''
# @DONE implement error handler for 404
#     error handler should conform to general task above
# '''
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         "error": 404,
#         "message": "resource not found"
#     }), 404


# '''
# @DONE implement error handler for AuthError
#     error handler should conform to general task above
# '''
# @app.errorhandler(AuthError)
# def auth_error(error):
#     return jsonify({
#         "success": False,
#         "error": error.status_code,
#         "message": error.error['description']
#     }), error.status_code

# if __name__ == "__main__":
#     app.debug = True
#     app.run()

# # if __name__ == "__main__":
# #     app.debug = True
# #     app.run()
