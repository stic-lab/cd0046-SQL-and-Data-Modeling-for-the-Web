"""empty message

Revision ID: 69eaafad22a9
Revises: 
Create Date: 2022-08-11 05:26:30.315269

"""
from alembic import op
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa
from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, Boolean, DateTime


# revision identifiers, used by Alembic.
revision = '69eaafad22a9'
down_revision = None
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
genre_venue = table('genre_venue',
                    column('genres', String),
                    column('venue_id', Integer)
                    )
genre_artist = table('genre_artist',
                     column('genres', String),
                     column('artist_id', Integer)
                     )
venue = table('venue',
              column('id', Integer),
              column('area_id', Integer),
              column('name', String),
              column('address', String),
              column('phone', String),
              column('website', String),
              column('facebook_link', String),
              column('seeking_talent', Boolean),
              column('seeking_description', String),
              column('image_link', String)
              )

artist = table('artist',
               column('id', Integer),
               column('area_id', Integer),
               column('name', String),
               column('phone', String),
               column('facebook_link', String),
               column('seeking_venue', Boolean),
               column('image_link', String)
               )

shows = table('shows',
              column('id', Integer),
              column('venue_id', Integer),
              column('artist_id', Integer),
              column('start_time', Date)
              )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('state')
    )
    op.create_table('genres',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=255), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('facebook_link', sa.String(length=255), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=255), nullable=True),
    sa.Column('image_link', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genre_artist',
    sa.Column('genres', sa.String(length=50), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['genres'], ['genres.name'], ),
    sa.PrimaryKeyConstraint('genres', 'artist_id')
    )
    op.create_table('genre_venue',
    sa.Column('genres', sa.String(length=50), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genres'], ['genres.name'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('genres', 'venue_id')
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
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
                       {'id': 14, 'state': 'IL', 'city': ''},
                       {'id': 15, 'state': 'IN', 'city': ''},
                       {'id': 16, 'state': 'IA', 'city': ''},
                       {'id': 17, 'state': 'KS', 'city': ''},
                       {'id': 18, 'state': 'KY', 'city': ''},
                       {'id': 19, 'state': 'LA', 'city': ''},
                       {'id': 20, 'state': 'ME', 'city': ''},
                       {'id': 21, 'state': 'MT', 'city': ''},
                       {'id': 22, 'state': 'NE', 'city': ''},
                       {'id': 23, 'state': 'NV', 'city': ''},
                       {'id': 24, 'state': 'NH', 'city': ''},
                       {'id': 25, 'state': 'NJ', 'city': ''},
                       {'id': 26, 'state': 'NM', 'city': ''},
                       {'id': 27, 'state': 'NY', 'city': 'New York'},
                       {'id': 28, 'state': 'NC', 'city': ''},
                       {'id': 29, 'state': 'ND', 'city': ''},
                       {'id': 30, 'state': 'OH', 'city': ''},
                       {'id': 31, 'state': 'OK', 'city': ''},
                       {'id': 32, 'state': 'OR', 'city': ''},
                       {'id': 33, 'state': 'MD', 'city': ''},
                       {'id': 34, 'state': 'MA', 'city': ''},
                       {'id': 35, 'state': 'MI', 'city': ''},
                       {'id': 36, 'state': 'MN', 'city': ''},
                       {'id': 37, 'state': 'MS', 'city': ''},
                       {'id': 38, 'state': 'MO', 'city': ''},
                       {'id': 39, 'state': 'PA', 'city': ''},
                       {'id': 40, 'state': 'RI', 'city': ''},
                       {'id': 41, 'state': 'SC', 'city': ''},
                       {'id': 42, 'state': 'SD', 'city': ''},
                       {'id': 43, 'state': 'TN', 'city': ''},
                       {'id': 44, 'state': 'TX', 'city': ''},
                       {'id': 45, 'state': 'UT', 'city': ''},
                       {'id': 46, 'state': 'VT', 'city': ''},
                       {'id': 47, 'state': 'VA', 'city': ''},
                       {'id': 48, 'state': 'WA', 'city': ''},
                       {'id': 49, 'state': 'WV', 'city': ''},
                       {'id': 50, 'state': 'WI', 'city': ''},
                       {'id': 51, 'state': 'WY', 'city': ''},
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
                       {'name': 'Swing'},
                       {'name': 'Other'},
                   ]
                   )

    op.bulk_insert(venue,
                   [
                       {'id': 1, 'area_id': 5, 'name': 'The Musical Hop', 'address': '1015 Folsom Street', 'phone': '123-123-1234', 'website': 'https://www.themusicalhop.com',  'seeking_description': 'We are on the lookout for a local artist to play every two weeks. Please call us.', 'seeking_talent': True,
                           'facebook_link': 'https://www.facebook.com/TheMusicalHop', 'image_link': 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'},
                       {'id': 2, 'area_id': 27, 'name': 'The Dueling Pianos Bar', 'address': '335 Delancey Street', 'phone': '914-003-1132', 'website': 'https://www.theduelingpianos.com', 'facebook_link': 'https://www.facebook.com/theduelingpianos',
                           'seeking_description': None, 'seeking_talent': False, 'image_link': 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'},
                       {'id': 3, 'area_id': 5, 'name': 'Park Square Live Music & Coffee', 'address': '34 Whiskey Moore Ave', 'phone': '415-000-1234', 'website': 'https://www.parksquarelivemusicandcoffee.com',
                           'facebook_link': 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
                           'seeking_description': None, 'seeking_talent': False, 'image_link': 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'}
                   ]
                   )

    op.bulk_insert(artist, [
        {'id': 4, 'name': 'Guns N Petals', 'area_id': 5, 'phone': '326-123-5000', 'website': 'https://www.gunsnpetalsband.com', 'facebook_link': 'https://www.facebook.com/GunsNPetals', 'seeking_venue': True, 'seeking_description':
            'Looking for shows to perform at in the San Francisco Bay Area!', 'image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'},
        {'id': 5, 'name': 'Matt Quevedo', 'area_id': 27, 'phone': '300-400-5000', 'facebook_link': 'https://www.facebook.com/mattquevedo923251523',
         'seeking_venue': False, 'seeking_description': None, 'image_link': 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'},
        {'id': 6, 'name': 'The Wild Sax Band', 'area_id': 5, 'facebook_link': None, 'phone': '432-325-5432',
         'seeking_venue': False, 'seeking_description': None,
         'image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'}
    ]
    )

    op.bulk_insert(genre_venue,
                   [
                       {'genres': 'Jazz', 'venue_id': 1},
                       {'genres': 'Reggae', 'venue_id': 1},
                       {'genres': 'Swing', 'venue_id': 1},
                       {'genres': 'Classical', 'venue_id': 1},
                       {'genres': 'Folk', 'venue_id': 1},
                       {'genres': 'Classical', 'venue_id': 2},
                       {'genres': 'R&B', 'venue_id': 2},
                       {'genres': 'Hip-Hop', 'venue_id': 2},
                       {'genres': 'Rock n Roll', 'venue_id': 3},
                       {'genres': 'Jazz', 'venue_id': 3},
                       {'genres': 'Classical', 'venue_id': 3},
                       {'genres': 'Folk', 'venue_id': 3},
                   ]
                   )

    op.bulk_insert(genre_artist,
                   [
                       {'genres': 'Rock n Roll', 'artist_id': 4},
                       {'genres': 'Jazz', 'artist_id': 5},
                       {'genres': 'Jazz', 'artist_id': 6},
                       {'genres': 'Classical', 'artist_id': 6},
                   ]
                   )
    op.bulk_insert(shows,
                   [
                       {'id': 1, 'venue_id': 1, 'artist_id': 4,
                           'start_time': '2019-05-21T21:30:00.000Z'},
                       {'id': 2, 'venue_id': 3, 'artist_id': 5,
                        'start_time': '2019-06-15T23:00:00.000Z'},
                       {'id': 3, 'venue_id': 3, 'artist_id': 6,
                        'start_time': '2035-04-01T20:00:00.000Z'},
                       {'id': 4, 'venue_id': 3, 'artist_id': 6,
                        'start_time': '2035-04-08T20:00:00.000Z'},
                       {'id': 5, 'venue_id': 3, 'artist_id': 6,
                        'start_time': '2035-04-15T20:00:00.000Z'}
                   ])





def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    op.drop_table('genre_venue')
    op.drop_table('genre_artist')
    op.drop_table('venue')
    op.drop_table('artist')
    op.drop_table('genres')
    op.drop_table('area')
    # ### end Alembic commands ###