#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from cmath import e
from time import timezone
from unittest import result
from urllib import response
from xmlrpc.client import DateTime
from sqlalchemy.ext.associationproxy import association_proxy
from enum import unique
import json
import dateutil.parser
import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, url_for, jsonify, abort
from sqlalchemy.ext.associationproxy import association_proxy
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.sql import func
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/fyyur'
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
genre_venue = db.Table('genre_venue',
                       db.Column('genres', db.String(50), db.ForeignKey(
                           'genres.name'), primary_key=True),
                       db.Column('venue_id', db.Integer, db.ForeignKey(
                           'venue.id'), primary_key=True))




# Create Area Models
class Genre(db.Model):
    __tablename__ = 'genres'
    name = db.Column(db.String(50), primary_key=True)
    genre_venue = db.relationship('Venue', secondary=genre_venue,
                                  backref=db.backref('genres', lazy=True))
    genre_artist = db.relationship('Artist', secondary=genre_artist,
                                  backref=db.backref('genres', lazy=True))

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

    id = db.Column(db.Integer, primary_key=True)
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
    # artist_rel = db.relationship('Shows',  backref="venue", lazy=True)
    artist = association_proxy("artists.id", "artist")

    def __repr__(self) -> str:
       return super().__repr__()

# Create Artist Models
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
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
    # venues_rel = db.relationship('Shows',  backref="artist", lazy=True)
    venue = association_proxy("venues.id", "venue")

    def __repr__(self) -> str:
       return super().__repr__()



# Create Show Models, this model containt the many to many relationship between Venues and Artists
class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='SET NULL'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete='SET NULL'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venues = db.relationship("Venue", backref="shows")
    artists = db.relationship("Artist", backref="shows")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
home = 'pages/home.html'
@app.route('/')
def index():
  return render_template(home)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  results=Area.query.join(Venue).all()
  areas = []
  current_time = datetime.now()
  for result in results:
    venues = []
    for venue in result.venues:
      upcomming_shows = db.session.query(Venue).join(Shows).filter(
          Shows.venue_id == venue.id, Shows.start_time > current_time).count()
      venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": upcomming_shows,
      })
    areas.append({
        "city": result.venues[0].city,
      "state": result.state,
      "venues": venues 
    })

  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(Venue.name.ilike("%{}%".format(search_term))).all()
  data = []
  current_time = datetime.now()
  for result in results:
    data.append(
      {
      "id": result.id,
      "name": result.name,
          "num_upcoming_shows": len(db.session.query(Shows).filter(
      Shows.venue_id == result.id, Shows.start_time > current_time).all()),
    }
    )
  response={
    "count": len(results),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  current_time = datetime.now()
  upcomming_shows = db.session.query(Artist).join(Shows).filter(
      Shows.venue_id == venue.id, Shows.start_time > current_time).all()
  upcomming = []
  for artist in upcomming_shows:
    upcomming.append(
        {
            "artist_id":  artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": artist.shows[0].start_time.isoformat()
        }
    )

  past_shows = db.session.query(Venue).join(Shows).filter(
      Shows.venue_id == venue.id, Shows.start_time <= current_time).all()
  past = []
  for artist in past_shows:
    past.append(
        {
            "artist_id":  artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": artist.shows[0].start_time.isoformat()
        }
    )
  data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "city": venue.city,
      "state": venue.area.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past,  # list of object
      "upcoming_shows": upcomming,  # list of object
      "past_shows_count": len(past),
      "upcoming_shows_count": len(upcomming),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  if form.validate_on_submit():
    name = form.name.data
    address = form.address.data
    city = form.city.data
    state = form.state.data
    genres = form.genres.data
    phone = form.phone.data
    website = form.website_link.data
    facebook_link = form.facebook_link.data
    seeking_talent = form.seeking_talent.data
    seeking_description = form.seeking_description.data
    image_link = form.image_link.data
    new_venue = Venue(
      name = name,
      address = address,
      phone = phone,
      website = website,
      image_link = image_link,
      facebook_link = facebook_link,
      seeking_talent = seeking_talent,
      seeking_description = seeking_description,
    )
    # new_venue.
    # form.populate_obj(new_venue)
    db.session.add(new_venue)
    db.session.commit()


  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template(home)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue_id + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue_id + ' could not be deleted.')
  finally:
    db.session.close()
  return jsonify({ 'success': True })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(
      Artist.name.ilike("%{}%".format(search_term))).all()
  data = []
  current_time = datetime.now()
  for result in results:
    data.append(
        {
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": len(db.session.query(Shows).filter(
                Shows.venue_id == result.id, Shows.start_time > current_time).all()),
        }
    )
  response = {
      "count": len(results),
      "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist ' + artist_id + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + artist_id + ' could not be deleted.')
  finally:
    db.session.close()
  return jsonify({ 'success': True })


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  current_time = datetime.now()
  upcomming_shows = db.session.query(Venue).join(Shows).filter(
      Shows.artist_id == artist.id, Shows.start_time > current_time).all()
  upcomming = []    
  for venue in upcomming_shows:
    upcomming.append(
      {
          "venue_id":  venue.id,
          "venue_name": venue.name,
          "venue_image_link": venue.image_link,
          "start_time": venue.shows[0].start_time.isoformat()
        }
    )
  
  past_shows = db.session.query(Venue).join(Shows).filter(
      Shows.artist_id == artist.id, Shows.start_time <= current_time).all()
  past = []
  for venue in past_shows:
    past.append(
        {
            "venue_id":  venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": venue.shows[0].start_time.isoformat()
        }
    )
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.area.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past,  # list of object
    "upcoming_shows": upcomming,  # list of object
    "past_shows_count": len(past),
    "upcoming_shows_count": len(upcomming),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  result = Artist.query.get(artist_id)
  artist={
    "id": result.id,
    "name": result.name,
    "genres": result.genres,
    "city": result.area.city,
    "state": result.area.state,
    "phone": result.phone,
    "website": result.website,
    "facebook_link": result.facebook_link,
    "seeking_venue": result.seeking_venue,
    "seeking_description": result.seeking_description,
    "image_link": result.image_link
  }
  form = ArtistForm(data=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  result = Venue.query.get(venue_id)
  venue={
    "id": result.id,
    "name": result.name,
    "genres": result.genres,
    "address": result.address,
    "city": result.area.city,
    "state": result.area.state,
    "phone": result.phone,
    "website": result.website,
    "facebook_link": result.facebook_link,
    "seeking_talent": result.seeking_talent,
    "seeking_description": result.seeking_description,
    "image_link": result.image_link
  }
  form = VenueForm(data=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template(home)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  results = db.session.query(Shows).join(Artist).join(Venue).all()
  shows_datas = []
  for result in results:
    shows_datas.append({
        "venue_id": result.venues.id,
        "venue_name": result.venues.name,
        "artist_id": result.artists.id,
        "artist_name": result.artists.name,
        "artist_image_link": result.artists.image_link,
        "start_time": result.start_time.isoformat()
    })
  return render_template('pages/shows.html', shows=shows_datas)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template(home)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
