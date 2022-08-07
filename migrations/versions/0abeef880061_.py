"""empty message

Revision ID: 0abeef880061
Revises: 30050a7e5440
Create Date: 2022-08-07 23:08:50.433812

"""
from alembic import op
import sqlalchemy as sa

# from xmlrpc.client import Boolean
from alembic import op
import sqlalchemy as sa
# from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, Boolean, DateTime

# from app import venues


# revision identifiers, used by Alembic.
revision = '0abeef880061'
down_revision = '30050a7e5440'
branch_labels = None
depends_on = None


# Create an ad-hoc table to use for the insert statement.
area = table('area',
             column('id', Integer),
             column('state', String),
             column('city', String)
             )

genres = table('genres',
               column('name', String)
               )
genres = table('genres',
               column('name', String)
               )
genre_venue = table('genre_venue',
                    column('name', String),
                    column('venue_id', Integer)
                    )
genre_artist = table('genre_artist',
                     column('name', String),
                     column('artist_id', Integer)
                     )
venues = table('venues',
               column('id', Integer),
               column('area', Integer),
               column('name', String),
               column('address', String),
               column('phone', String),
               column('website', String),
               column('facebook_link', String),
               column('seeking_talent', Boolean),
               column('seeking_description', String),
               column('image_link', String)
               )

artists = table('artists',
                column('id', Integer),
                column('area', Integer),
                column('name', String),
                column('phone', String),
                column('facebook_link', String),
                column('seeking_venue', Boolean),
                column('image_link', String)
                )

shows = table('shows',
              column('venue_id', Integer),
              column('artist_id', Integer),
              column('start_time', DateTime)
              )

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre_artist',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.name'], ),
    sa.PrimaryKeyConstraint('genre_id', 'artist_id')
    )
    op.create_table('genre_venue',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.name'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('genre_id', 'venue_id')
    )
    # ### end Alembic commands ###
    op.bulk_insert(area,
                   [
                       {'id': 1, 'state': 'AL', 'city': ''},
                       {'id': 2, 'state': 'AK', 'city': ''},
                       {'id': 3, 'state': 'AZ', 'city': ''},
                       {'id': 4, 'state': 'AR', 'city': ''},
                       {'id': 5, 'state': 'CA', 'city': 'San Francisco'},
                       {'id': 6, 'state': 'CO', 'city': ''},
                       {'id': 7, 'state': 'CT', 'city': ''},
                       {'id': 8, 'state': 'DE', 'city': ''},
                       {'id': 9, 'state': 'DC', 'city': ''},
                       {'id': 10, 'state': 'FL', 'city': ''},
                       {'id': 11, 'state': 'GA', 'city': ''},
                       {'id': 12, 'state': 'HI', 'city': ''},
                       {'id': 13, 'state': 'ID', 'city': ''},
                       {'id': 14, 'state': 'ID', 'city': ''},
                       {'id': 15, 'state': 'IL', 'city': ''},
                       {'id': 16, 'state': 'IN', 'city': ''},
                       {'id': 17, 'state': 'IA', 'city': ''},
                       {'id': 18, 'state': 'KS', 'city': ''},
                       {'id': 19, 'state': 'KY', 'city': ''},
                       {'id': 20, 'state': 'LA', 'city': ''},
                       {'id': 21, 'state': 'ME', 'city': ''},
                       {'id': 22, 'state': 'MT', 'city': ''},
                       {'id': 23, 'state': 'NE', 'city': ''},
                       {'id': 24, 'state': 'NV', 'city': ''},
                       {'id': 25, 'state': 'NH', 'city': ''},
                       {'id': 26, 'state': 'NJ', 'city': ''},
                       {'id': 27, 'state': 'NM', 'city': ''},
                       {'id': 28, 'state': 'NY', 'city': 'New York'},
                       {'id': 29, 'state': 'NC', 'city': ''},
                       {'id': 30, 'state': 'ND', 'city': ''},
                       {'id': 31, 'state': 'OH', 'city': ''},
                       {'id': 32, 'state': 'OK', 'city': ''},
                       {'id': 33, 'state': 'OR', 'city': ''},
                       {'id': 34, 'state': 'MD', 'city': ''},
                       {'id': 35, 'state': 'MA', 'city': ''},
                       {'id': 36, 'state': 'MA', 'city': ''},
                       {'id': 37, 'state': 'MI', 'city': ''},
                       {'id': 38, 'state': 'MN', 'city': ''},
                       {'id': 39, 'state': 'MS', 'city': ''},
                       {'id': 40, 'state': 'MO', 'city': ''},
                       {'id': 41, 'state': 'PA', 'city': ''},
                       {'id': 42, 'state': 'RI', 'city': ''},
                       {'id': 43, 'state': 'SC', 'city': ''},
                       {'id': 44, 'state': 'SD', 'city': ''},
                       {'id': 45, 'state': 'TN', 'city': ''},
                       {'id': 46, 'state': 'TX', 'city': ''},
                       {'id': 47, 'state': 'UT', 'city': ''},
                       {'id': 48, 'state': 'VT', 'city': ''},
                       {'id': 49, 'state': 'VA', 'city': ''},
                       {'id': 50, 'state': 'WA', 'city': ''},
                       {'id': 51, 'state': 'WV', 'city': ''},
                       {'id': 52, 'state': 'WI', 'city': ''},
                       {'id': 53, 'state': 'WY', 'city': ''},
                   ]
                   )

    op.bulk_insert(genres,
                   [
                       {'name': 'Alternative'},
                       {'name': 'Blues'},
                       {'name': 'Classical'},
                       {'name': 'Country'},
                       {'name': 'Electronic'},
                       {'name': 'Folk'},
                       {'name': 'Funk'},
                       {'name': 'Hip-Hop'},
                       {'name': 'Heavy Metal'},
                       {'name': 'Instrumental'},
                       {'name': 'Jazz'},
                       {'name': 'Musical Theatre'},
                       {'name': 'Pop'},
                       {'name': 'Punk'},
                       {'name': 'R&B'},
                       {'name': 'Reggae'},
                       {'name': 'Rock n Roll'},
                       {'name': 'Soul'},
                       {'name': 'Other'},
                   ]
                   )

    op.bulk_insert(genre_venue,
                   [
                       {'name': 'Jazz', 'venue_id': 1},
                       {'name': 'Reggae', 'venue_id': 1},
                       {'name': 'Swing', 'venue_id': 1},
                       {'name': 'Classical', 'venue_id': 1},
                       {'name': 'Folk', 'venue_id': 1},
                       {'name': 'Classical', 'venue_id': 2},
                       {'name': 'R&B', 'venue_id': 2},
                       {'name': 'Hip-Hop', 'venue_id': 2},
                       {'name': 'Rock n Roll', 'venue_id': 3},
                       {'name': 'Jazz', 'venue_id': 3},
                       {'name': 'Classical', 'venue_id': 3},
                       {'name': 'Folk', 'venue_id': 3},
                   ]
                   )

    op.bulk_insert(genre_artist,
                   [
                       {'name': 'Rock n Roll', 'artist_id': 4},
                       {'name': 'Jazz', 'artist_id': 5},
                       {'name': 'Jazz', 'artist_id': 6},
                       {'name': 'Classical', 'artist_id': 6},
                   ]
                   )

    op.bulk_insert(venues,
                   [
                       {'id': 1, 'area': 5, 'name': "The Musical Hop", "address": "1015 Folsom Street", "phone": "123-123-1234", "website": "https://www.themusicalhop.com", "facebook_link": "https://www.facebook.com/TheMusicalHop", "seeking_talent": True,
                        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.", "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60", },
                       {'id': 2, 'area': 28, 'name': "The Dueling Pianos Bar", "address": "335 Delancey Street", "phone": "914-003-1132",
                        "website": "https://www.theduelingpianos.com", "facebook_link": "https://www.facebook.com/theduelingpianos",
                        "seeking_talent": False, "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"},
                       {'id': 3, 'area': 5, 'name': "Park Square Live Music & Coffee", "address": "34 Whiskey Moore Ave", "phone": "415-000-1234",
                        "website": "https://www.parksquarelivemusicandcoffee.com",
                        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
                        "seeking_talent": False, "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"},
                   ]
                   )

    op.bulk_insert(artists, [
        {"id": 4, "name": "Guns N Petals", "area": 5, "phone": "326-123-5000", "website": "https://www.gunsnpetalsband.com", "facebook_link": "https://www.facebook.com/GunsNPetals", "seeking_venue": True, "seeking_description":
            "Looking for shows to perform at in the San Francisco Bay Area!", "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80", },
        {"id": 5, "name": "Matt Quevedo", "area": 28, "phone": "300-400-5000", "facebook_link": "https://www.facebook.com/mattquevedo923251523",
         "seeking_venue": False, "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80", },
        {"id": 6, "name": "The Wild Sax Band", "area": 5, "phone": "432-325-5432",
         "seeking_venue": False,
         "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80", }
    ]
    )

    op.bulk_insert(shows,
                   [
                       {"venue_id": 1, "artist_id": 4,
                           "start_time": "2019-05-21T21:30:00.000Z"},
                       {"venue_id": 3, "artist_id": 5,
                        "start_time": "2019-06-15T23:00:00.000Z"},
                       {"venue_id": 3, "artist_id": 6,
                        "start_time": "2035-04-01T20:00:00.000Z"},
                       {"venue_id": 3, "artist_id": 6,
                        "start_time": "2035-04-08T20:00:00.000Z"},
                       {"venue_id": 3, "artist_id": 6,
                        "start_time": "2035-04-15T20:00:00.000Z"}
                   ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genre_venue')
    op.drop_table('genre_artist')
    # ### end Alembic commands ###