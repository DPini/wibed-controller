""" Experiment command-related functionality. """

from database import db

class Command(db.Model):
    """
    Represents a command in a testbed experiment.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    experimentId = db.Column(db.Integer, db.ForeignKey("experiment.id"))
    command = db.Column(db.Text)

    experiment = db.relationship("Experiment", \
        backref=db.backref("commands", lazy="dynamic"))

    def __init__(self, experimentId, command):
        self.experimentId = experimentId
        self.command = command

