#! /usr/bin/env python
""" Initializes the database schema. """

from server import app
from database import db
from models import *

db.create_all(app=app)
