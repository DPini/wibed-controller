#! /usr/bin/env python
""" Initializes the database schema. """

from server import db
from models import *

db.create_all()
