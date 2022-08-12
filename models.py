#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
from datetime import datetime
from enum import unique
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

#Association table between Genre and Artist
genre_artist = db.Table('genre_artist',
                        db.Column('genres', db.String(50), db.ForeignKey(
                     'genres.name'), primary_key=True),
                        db.Column('artist_id', db.Integer, db.ForeignKey(
                     'artist.id'), primary_key=True),
                 )


class GenreArtist():
    """ Map the relation table genre_artist between Genre and Artist object

    ------------
        parameters:
            -artist: map the table artist
            -genres: map the table genres

    """
    def __init__(self, genres, artist_id):
        self.artist = artist_id,
        self.genres = genres
db.mapper(GenreArtist, genre_artist)

#Association table between Genre and Venue
genre_venue = db.Table('genre_venue',
                       db.Column('genres', db.String(50), db.ForeignKey(
                           'genres.name'), primary_key=True),
                       db.Column('venue_id', db.Integer, db.ForeignKey(
                           'venue.id'), primary_key=True))



class GenreVenue():
    """Map the relation table genre_venue between Genre and Venue object

    ------------
        schema:
            -venue: integerforeign key ref venue.id
            -genres: foreign key ref genre.name

    """
    def __init__(self, genres, venue_id):
        self.venue = venue_id,
        self.genres = genres
db.mapper(GenreVenue, genre_venue)



class Genre(db.Model):
    """Represent the genre table. It store the music genre. It has only one parameter which is also a primary key

    ------------
        schema:
            -name: string(50), primary key

    """
    __tablename__ = 'genres'
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self) -> str:
       return f'{self.name}'

# Create Area Models
class Area(db.Model):
    """Represent the area table.

    ------------
        schema:
            -state: string(2), primary key
            -venues: map one to many relationship between Area and Venue (Area[1]-----[n]Venue)
            -artist: map one to many relationship between Area and Artist (Area[1]-----[n]Artist)

    """
    __tablename__ = 'area'
    state = db.Column(db.String(2), primary_key=True)
    venues = db.relationship('Venue', backref='area', lazy=True)
    artists = db.relationship('Artist', backref='area', lazy=True)

    def __repr__(self) -> str:
       return f'{self.state}'

# Create Venue Models
class Venue(db.Model):
    """Represent the venue table.

    ------------
        schema:
            -id: Integer, primary_key
            -name: String(50), nullable=False
            -address: String(255), nullable=False
            -state: String(2), ForeignKey('area.state')
            -city: String(50), nullable=True
            -phone: String(50), nullable=True
            -website: db.String(255)
            -facebook_link: String(255), nullable=True
            -seeking_talent: Boolean, nullable=False, default=False, if true this mean -the venue is looking for an artist to play
            -seeking_description: String(255), nullable=True
            -image_link: String(255), nullable=True
            -created_at: DateTime, default=datetime.utcnow
            -updated_at: DateTime, default=datetime.utcnow
            -genres = map many to many relationship between Genre and Venue (Genre[1]---[n]genre_venue[n]---[1]Venue)
            -artist = association proxy, point to artist.id to facilitate data fetching as we have relation many to many between Artist and Venue (Venue[1]---[n]Shows[n]---[1]Venue)

    """
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), db.ForeignKey(
        'area.state'), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True, unique=True)
    website = db.Column(db.String(255), unique=True)
    facebook_link = db.Column(db.String(255), nullable=True, unique=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(255), nullable=True)
    image_link = db.Column(db.String(255), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    genres = db.relationship(
        'Genre', secondary=genre_venue, backref=db.backref('venues', lazy=True))
    # artist_id = db.Column(db.Integer, db.ForeignKey(
    #     'artist.id'), nullable=True)
    shows = db.relationship(
        "Shows", cascade='all, delete-orphan', backref="venues")
    # artist = association_proxy("artists.id", "artists")

    def __repr__(self) -> str:
       return super().__repr__()


# Create Artist Models

class Artist(db.Model):
    """Represent the artist table.

    ------------
        schema:
            -id: Integer, primary_key
            -name: String(50), nullable=False
            -state: String(2), ForeignKey('area.state')
            -city: String(50), nullable=True
            -phone: String(50), nullable=True
            -website: db.String(255), nullable=True
            -facebook_link: String(255), nullable=True
            -seeking_venue: Boolean, nullable=False, default=False, if true this mean -the artist is looking for venue where to play
            -seeking_description: String(255), nullable=True
            -image_link: String(255), nullable=True
            -created_at: DateTime, default=datetime.utcnow
            -updated_at: DateTime, default=datetime.utcnow
            -genres = map many to many relationship between Genre and Venue (Genre[1]---[n]genre_venue[n]---[1]Venue)
            -artist = association proxy, point to venue.id to facilitate data fetching as we have relation many to many between Artist and Venue (Venue[1]---[n]Shows[n]---[1]Venue)

    """
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), db.ForeignKey(
        'area.state'), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(120), nullable=True, unique=True)
    website = db.Column(db.String(120), nullable=True, unique=True)
    facebook_link = db.Column(db.String(120), nullable=True, unique=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(255), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    genres = db.relationship('Genre', secondary=genre_artist,backref=db.backref('artists', lazy=True))
    availability = db.relationship('ArtistAvailability', backref='artist', lazy=True)
    shows = db.relationship(
        "Shows", cascade='all, delete-orphan', backref="artists")

    # venue_id = db.Column(db.Integer, db.ForeignKey(
    #     'venue.id'), nullable=True)
    # shows = db.relationship(
    #     "Shows", cascade='all, delete-orphan', backref="artists")
    # venue = association_proxy("venue_id", "shows")
    # artist = association_proxy("artists.id", "artist")


    def __repr__(self) -> str:
       return super().__repr__()


# db.mapper(Venue.id, Artist.venue)
class Shows(db.Model):
    """Represent the artist table.

    ------------
        schema:
            -id: Integer, primary_key
            -artist_id: Integer, db.ForeignKey('artist.id', ondelete='SET NULL'), nullable=True
            -venue_id: Integer, db.ForeignKey('venue.id', ondelete='SET NULL'), nullable=True
            -start_time: DateTime, nullable=False, default=datetime.utcnow
            -created_at:DateTime, default=datetime.utcnow, creation date
            -updated_at:DateTime, default=datetime.utcnow, update date

    """
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    # artists = db.relationship(
    #     "Artist", backref="shows")
    # venues = db.relationship(
    #     "Venue",  backref="shows")


# db.mapper(Venue.id, Artist.venue)
class ArtistAvailability(db.Model):
    """Represent the artist_availability table.

    ------------
        schema:
            -id: Integer, primary_key
            -artist_id: Integer, db.ForeignKey('artist.id', ondelete='SET NULL'), nullable=True
            -begin_date: DateTime, nullable=False, Start date when artist is available
            -end_date: DateTime, nullable=False, End date when artist is available
            -created_at:DateTime, default=datetime.utcnow, creation date
            -updated_at:DateTime, default=datetime.utcnow, update date

    """
    __tablename__ = 'artist_availability'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=True)
    begin_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
