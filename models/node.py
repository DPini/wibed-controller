""" Testbed node-related functionality. """

from sqlalchemy.ext.hybrid import hybrid_property
from enum import Enum

from database import db, DatabaseEnum

class Node(db.Model):
    """
    Represents a testbed node.
    """

    Status = Enum("Status", {"INIT": 0, "IDLE": 1, "PREPARING": 2, "READY": 3, 
        "RUNNING": 4, "UPGRADING": 5, "ERROR": 6})

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Text)
    version = db.Column(db.Text)
    status = db.Column(DatabaseEnum(Status, *[e.name for e in Status]))
    lastContact = db.Column(db.DateTime)
    experimentId = db.Column(db.Integer, db.ForeignKey("experiment.id"))

    activeExperiment = db.relationship("Experiment")

    @hybrid_property
    def available(self):
        return (self.activeExperiment == None) & \
               (self.status == self.Status.IDLE)

    def __init__(self, id):
        self.id = id
