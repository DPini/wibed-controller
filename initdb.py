#! /usr/bin/env python
""" Initializes the database schema. """

from server import create_app
from database import db
from models import *

app=create_app("settings.DevelopmentConfig")
db.create_all(app=app)
