#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
from datetime import datetime
from flask import Flask
from sqlalchemy.ext.associationproxy import association_proxy
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



# Create genre_associations Models, this model containt the many to many relationship between Venues/Artist and genres
genre_artist = db.Table('genre_artist',
                        db.Column('genres', db.String(50), db.ForeignKey(
                     'genres.name'), primary_key=True),
                        db.Column('artist_id', db.Integer, db.ForeignKey(
                     'artist.id'), primary_key=True),
                 )

                 
# Create Area Models
class GenreArtist():
  def __init__(self, genres, artist_id):
    self.venue = artist_id,
    self.genres = genres
db.mapper(GenreArtist, genre_artist)

genre_venue = db.Table('genre_venue',
                       db.Column('genres', db.String(50), db.ForeignKey(
                           'genres.name'), primary_key=True),
                       db.Column('venue_id', db.Integer, db.ForeignKey(
                           'venue.id'), primary_key=True))


# Create Area Models
class GenreVenue():
  def __init__(self, genres, venue_id):
    self.venue = venue_id,
    self.genres = genres
db.mapper(GenreVenue, genre_venue)


# Create Area Models
class Genre(db.Model):
    __tablename__ = 'genres'
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self) -> str:
       return f'{self.name}'

# Create Area Models
class Area(db.Model):
    __tablename__ = 'area'
    state = db.Column(db.String(2), primary_key=True)
    venues = db.relationship('Venue', backref='area', lazy=True)
    artists = db.relationship('Artist', backref='area', lazy=True)

    def __repr__(self) -> str:
       return f'{self.state}'

# Create Venue Models
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), db.ForeignKey(
        'area.state'), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(255))
    facebook_link = db.Column(db.String(255), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(255), nullable=True)
    image_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    genres = db.relationship('Genre', secondary=genre_venue, backref=db.backref('venues', lazy=True))
    artist = association_proxy("artists.id", "artist")

    def __repr__(self) -> str:
       return super().__repr__()

# Create Artist Models
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), db.ForeignKey(
        'area.state'), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(255), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    genres = db.relationship('Genre', secondary=genre_artist,backref=db.backref('artists', lazy=True))
    venue = association_proxy("venues.id", "venue")

    def __repr__(self) -> str:
       return super().__repr__()



# Create Show Models, this model containt the many to many relationship between Venues and Artists
class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='SET NULL'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete='SET NULL'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venues = db.relationship("Venue", backref="shows")
    artists = db.relationship("Artist", backref="shows")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)