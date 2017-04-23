import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'

# Connect to the database
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


SQLALCHEMY_DATABASE_URI = 'postgres://nwpzolgh:wZbR4Q7D1YpI0PI0velMGKyFkKxPEuHi@elmer.db.elephantsql.com:5432/nwpzolgh'
# SQLALCHEMY_DATABASE_URI = 'postgresql://fulfil:@localhost:5432/kickstarterapp'

