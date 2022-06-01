from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask
import os

# database_name = "casting_agency.db"
# database_path = "postgres://{}:{}@{}/{}".format(
#     'postgres', 'root', 'localhost:5432', database_name)
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/casting_agency'

# app = Flask(__name__)
# moment = Moment(app)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

db = SQLAlchemy()

'''
 setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):
    uri = os.environ.get('DATABASE_URL')

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.String(80), nullable=False)
    cast = db.relationship('Actor', secondary='movie_actors')

    def __repr__(self):
        return '<Movie id: {}, title: {}>'.format(self.id, self.title)

    '''
    short()
        short form representation of the Movie model
    '''
    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


    '''
    long()
        short form representation of the Movie model
    '''
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': [actor.long() for actor in self.cast]
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique id
        the model must have a not nullable name and release date
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

'''
Actor
a persistent actor entity, extends the base SQLAlchemy Model
'''

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Actor id: {}, name: {}>'.format(self.id, self.name)

    '''
    short()
        short form representation of the Actor model
    '''
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
        }

    '''
    long()
        short form representation of the Actor model
    '''
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender' : self.gender
        }
    
    '''
    insert()
        inserts a new model into a database
        the model must have a unique id
        the model must have a not nullable name and release date
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()


movie_actors = db.Table('movie_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)
    
