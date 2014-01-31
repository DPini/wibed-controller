""" Testbed node-related functionality. """

from sqlalchemy.ext.hybrid import hybrid_property
from enum import Enum
from datetime import datetime
from flask import current_app

from database import db, DatabaseEnum

class Node(db.Model):
    """
    Represents a testbed node.
    """

    Status = Enum("Status", {"INIT": 0, "IDLE": 1, "PREPARING": 2, "READY": 3, 
	    "DEPLOYING":4, "RUNNING": 5, "RESETTING": 6,  "UPGRADING": 7, "ERROR": 8})

    id = db.Column(db.String(64), primary_key=True)
    model = db.Column(db.Text)
    firmwareId = db.Column(db.Integer, db.ForeignKey("firmware.id"))
    status = db.Column(DatabaseEnum(Status, *[e.name for e in Status]))
    lastContact = db.Column(db.DateTime)
    experimentId = db.Column(db.Integer, db.ForeignKey("experiment.id"))
    upgradeId = db.Column(db.Integer, db.ForeignKey("upgrade.id"))
    show = db.Column(db.Boolean, default=False)

    activeExperiment = db.relationship("Experiment")
    activeUpgrade = db.relationship("Upgrade")
    installedFirmware = db.relationship("Firmware", backref=db.backref("nodes", lazy="dynamic"))

    @hybrid_property
    def available(self):
        return (self.activeExperiment == None) & \
               (self.status == self.Status.IDLE) & \
               (self.activeUpgrade == None)


    @property
    def lastSeen(self):
        if self.lastContact:
            return (datetime.now() - self.lastContact).seconds

    @property
    def reachable(self):
        if self.lastSeen != None:
            return self.lastSeen < current_app.config['REACHABLE_WINDOW']
        else:
            return False

    @property
    def lastSeenStr(self):
        if self.lastSeen:
            return str(self.lastSeen)
        else:
            return ""

    def __init__(self, id):
        self.id = id
