import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from models import setup_db, Actor, Movie
from flask import Flask
from flask_moment import Moment
from app import create_app


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant_token = os.environ['ASSISTANT_TOKEN']
        self.director_token = os.environ['DIRECTOR_TOKEN']
        self.producer_token = os.environ['PRODUCER_TOKEN']
        setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Mark Alex",
            "age": 20,
            "gender": "male"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Christin"
        }

        self.VALID_UPDATE_ACTOR = {
            "name": "Tyrion"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Game of Thrones",
            "release_date": "2022",
            "cast": ["Tyron"]
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Squid Games",
            "release_date": "2021",
            "cast": ["Tyron"]
        }

        self.VALID_UPDATE_MOVIE = {
            "release_date": "2020"
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_should_return_401_when_no_token(self):
        """GET /actors should return 401 if no token is provided"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_actors_should_return_actors(self):
        """GET /actors should return all actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertTrue(data['actors'] != null)

    def test_create_actorshould_create_new_actor(self):
        """POST /actors should create a new actor"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_get_actor_details_by_id_should_return_single_actor(self):
        """GET /actors-detail/<id> should return a single actor"""
        res = self.client().get('/actors-detail/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data['actor'] != null)

    def test_get_actors_by_id_should_return_404_if_actor_not_found(self):
        """GET /actors-detail/<id> should return 404 if actor is not found"""
        res = self.client().get('/actors-detail/500', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'] != null)

    def test_create_actor_with_director_token(self):
        """POST /actors should create a new actor"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue('actors' != null)

    def test_400_create_actor_if_actor_not_valid(self):
        """POST /actors should return 400 if actor is not valid"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_actor_with_director_token(self):
        """PATCH /actors/<id> should update an actor"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data['actors'] != null)
        self.assertEqual(data["actors"][0]["name"],
                         self.VALID_UPDATE_ACTOR["name"])

    def test_404_update_actor_if_actor_not_found(self):
        """PATCH /actors/<id> should return 404 if actor is not found"""
        res = self.client().patch('/actors/101', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_with_assistant_token(self):
        """DELETE /actors/<id> with assistant should not delete an actor"""
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

    def test_delete_actor_with_producer_token(self):
        """DELETE /actors/<id> with producer token should delete an actor"""
        res = self.client().delete('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('delete', data)

    def test_404_delete_actor_if_actor_not_found(self):
        """DELETE /actors/<id> with producer token should return 404 if actor is not found"""
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies_should_return_movies(self):
        """GET /movies should return all movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id_should_return_movie_details(self):
        """GET /movies/<id> should return a single movie"""
        res = self.client().get('/movie-detail/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertIn('cast', data['movie'])
        self.assertTrue(len(data["movie"]["cast"]))

    def test_404_get_movie_by_id_if_movie_not_found(self):
        """Get /movie-detail/<movie_id> should return 404 if movie is not found"""
        res = self.client().get('/movie-detail/100', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_movie_with_assistant_token_should_return_false(self):
        """POST /movies with user token should not create a new movie"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_movie_success_with_producer_token(self):
        """POST /movies with producer token should create a new movie"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue('movies' != null)

    def test_403_create_movie_with_director_token(self):
        """POST /movies with director token should return 403"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_with_producer_token(self):
        """PATCH /movies/<id> should update a movie"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.VALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movie"][0]["title"] != null)
        self.assertEqual(data["movie"][0]["release_date"],
                         self.VALID_UPDATE_MOVIE["release_date"])

    def test_404_update_movie_info_if_movie_not_found(self):
        """PATCH /movies/<id> should return 404 if movie is not found"""
        res = self.client().patch('/movies/66', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_director_token_should_return_false(self):
        """DELETE /movies/<id> with director token should not delete a movie"""
        res = self.client().delete('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_movie_with_producer_token_should_return_true(self):
        """DELETE /movies/<id> with producer token should delete a movie """
        res = self.client().delete('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('delete', data)

    def test_404_delete_movie_if_movie_not_found(self):
        """DELETE /movies/<id> with producer token should return 404 if movie is not found"""
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
