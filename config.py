import secrets
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/fyyur'

# secret_key = secrets.token_hex(16)
# # example output, secret_key = 
SECRET_KEY = '000d88cd9d90036ebdd237eb6b0db000'
