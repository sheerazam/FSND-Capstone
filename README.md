# Casting Agency API

## Capstone Project for Udacity's Full Stack Web Developer Nanodegree
Heroku Link: https://fathomless-dusk-96984.herokuapp.com/

## You may find the jwts in `jwts.txt` for each role.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

## Running the server

Before running the application locally, make the following changes in the `app.py` file in root directory:

- Also, uncomment the line `db_drop_and_create_all()` on the initial run to setup the required tables in the database.

To run the server, execute:

```bash
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

Using the `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started
Base URL: This application can be run locally. The hosted version is at `https://fathomless-dusk-96984.herokuapp.com/`.

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, except the root (or health) endpoint, that are passed via the `Bearer` token.

The application has three different types of roles:
- Casting Assistant
  - can only view the list of artist and movies and can view complete information for any actor or movie
  - has `get:actors, get:actor-details, get:movies, get:movie-details` permissions
- Casting Director
  - can perform all the actions that `Casting Assistant` can
  - can also create an actor and movie and also update respective information
  - has `patch:actor, patch:movie, create:actor, create:movie` permissions in addition to all the permissions that `Casting Assistant` has
- Executive Producer
  - can perform all the actions that `Casting Director` can
  - can also delete an actor or a movie
  - has `delete:actor, delete:movie` permissions in addition to all the permissions that `Casting Director` has

## Endpoints

#### GET /actors
 - General
   - gets the list of all the actors
   - requires `get:actors` permission
 
#### GET /actors/{actor_id}
 - General
   - gets the complete info for an actor
   - requires `get:actors-details` permission

#### POST /actors
 - General
   - creates a new actor
   - requires `create:actors` permission

#### PATCH /actors/{actor_id}
 - General
   - updates the info for an actor
   - requires `patch:actor` permission

#### DELETE /actors/{actor_id}
 - General
   - deletes the actor
   - requires `delete:actor` permission
   - will also delete the mapping to the movie but will not delete the movie from the database

#### GET /movies
 - General
   - gets the list of all the movies
   - requires `get:movies` permission

#### GET /movies/{movie_id}
 - General
   - gets the complete info for a movie
   - requires `get:movies-details` permission
 
 - Sample Request
   - `https://ry-fsnd-capstone.herokuapp.com/movies/1`

#### POST /movies
 - General
   - creates a new movie
   - requires `create:movie` permission
 
#### PATCH /movies/{movie_id}
 - General
   - updates the info for a movie
   - requires `patch:movie` permission
 

#### DELETE /movies/{movie_id}
 - General
   - deletes the movie
   - requires `delete:movie` permission
   - will not affect the actors present in the database

## Testing
For testing the backend, run the following commands (in the exact order):
```
dropdb casting_agency
createdb casting_agency
psql casting_agency < casting_agency.sql
python test.py
```