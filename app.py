#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


import dateutil.parser
from datetime import datetime
import babel
from flask import render_template, request, flash, redirect, url_for, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from forms import ShowForm, VenueForm, ArtistForm
from models import Area, Venue, Genre, Artist, Shows, app, moment, db, migrate

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
  form = VenueForm()
  # print("about to validate", file=sys.stderr)
  if form.validate_on_submit():  
    new_venue = Venue(
      name = form.name.data,
      address = form.address.data,
      city = form.city.data,
      phone = form.phone.data,
      website = form.website_link.data,
      image_link = form.image_link.data,
      facebook_link = form.facebook_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description = form.seeking_description.data,
    )
    new_venue.state = form.state.data
    genres = []
    
    for genre in form.genres.data:
      if Genre.query.filter_by(name=genre).one():
        genres.append(Genre.query.filter_by(name=genre).one())
      else:
        genres.append(genre)

    new_venue.genres = genres
    try:
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' +
            form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    flash('Form must be correctly filled')
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


#  ----------------------------------------------------------------
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
    "city": result.city,
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

  form = ArtistForm()
  if form.validate_on_submit():
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.phone = form.phone.data
    artist.website = form.website_link.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    artist.state = form.state.data
    genres = []
    for genre in form.genres.data:
      if Genre.query.filter_by(name=genre).one():
        genres.append(Genre.query.filter_by(name=genre).one())
      else:
        genres.append(genre)

    artist.genres = genres
    try:
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully updated!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Artist ' +
            form.name.data + ' could not be updated.')
    finally:
      db.session.close()
  else:
    flash('Form must be correctly filled')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  result = Venue.query.get(venue_id)
  venue={
    "id": result.id,
    "name": result.name,
    "genres": result.genres,
    "address": result.address,
    "city": result.city,
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
  form = VenueForm()
  if form.validate_on_submit():
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data,
    venue.address = form.address.data
    venue.city = form.city.data
    venue.phone = form.phone.data
    venue.website = form.website_link.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.seeking_talent=form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.state = form.state.data
    genres = []
    for genre in form.genres.data:
      if Genre.query.filter_by(name=genre).one():
        genres.append(Genre.query.filter_by(name=genre).one())
      else:
        genres.append(genre)

    venue.genres = genres
    try:
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully updated!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' +
            form.name.data + ' could not be updated.')
    finally:
      db.session.close()
  else:
    flash('Form must be correctly filled')

  return redirect(url_for('show_venue', venue_id=venue_id))


#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  # print("about to validate", file=sys.stderr)
  if form.validate_on_submit():
    new_artist = Artist(
        name=form.name.data,
        city=form.city.data,
        phone=form.phone.data,
        website=form.website_link.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data,
    )
    new_artist.state = form.state.data
    genres = []

    for genre in form.genres.data:
      if Genre.query.filter_by(name=genre).one():
        genres.append(Genre.query.filter_by(name=genre).one())
      else:
        genres.append(genre)

    new_artist.genres = genres
    try:
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Artist ' +
            form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    flash('Form must be correctly filled')
  return render_template(home)



#  ----------------------------------------------------------------
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
  form = ShowForm()
  if form.validate_on_submit():
    new_shows = Shows(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
    )
    
    try:
      db.session.add(new_shows)
      db.session.commit()
      flash('Show was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
  else:
    flash('Form must be correctly filled')
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
