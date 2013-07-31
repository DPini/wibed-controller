""" Firmware-related functionality. """

from sqlalchemy.ext.hybrid import hybrid_property
from enum import Enum

from database import db, DatabaseEnum

class Firmware(db.Model):
    """
    Represents the firmware of a testbed node.
    """

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Text, unique=True)
    hash = db.Column(db.String(40))

    def __init__(self, version, hash=None):
        self.version = version
        self.hash = hash

upgradeHistory = db.Table('firmware_installation_history',
    db.Column('upgrade_id', db.Integer, db.ForeignKey('upgrade.id')),
    db.Column('node_id', db.Integer, db.ForeignKey('node.id'))
)

class Upgrade(db.Model):
    """
    Represents an upgrade order of a firmware.
    """

    id = db.Column(db.Integer, primary_key=True)
    firmwareId = db.Column(db.Integer, db.ForeignKey("firmware.id"))
    upgradeTime = db.Column(db.DateTime)

    firmware = db.relationship("Firmware", backref="upgradeOrders")

    nodes = db.relationship("Node", secondary=upgradeHistory, \
            backref=db.backref("upgrades", lazy="dynamic"), lazy="dynamic")

    def __init__(self, firmwareId, upgradeTime, nodes):
        self.firmwareId = firmwareId
        self.upgradeTime = upgradeTime

        for node in nodes:
            if node.firmwareId == firmwareId:
                raise ValueError("At least one of the selected nodes already \
                        has this firmware.")
            if not node.available:
                raise ValueError("At least one of the nodes is not available \
                        for upgrade.")
            node.activeUpgrade = self

        self.nodes.extend(nodes)
