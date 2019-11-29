""" Import some useful modules """
import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Class used to define some env const """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretdianou'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
