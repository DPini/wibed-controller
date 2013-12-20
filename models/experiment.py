""" Testbed experiment-related functionality. """

from datetime import datetime
from enum import Enum

from database import db, DatabaseEnum

experimentHistory = db.Table('experiment_history',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('node_id', db.Integer, db.ForeignKey('node.id'))
)

class Experiment(db.Model):
    """
    Represents a testbed experiment.
    """
    __table_args__ = {'sqlite_autoincrement': True}

    Status = Enum("Status", "PREPARING RUNNING FINISHED")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    status = db.Column(DatabaseEnum(Status, *[e.name for e in Status]))
    overlay = db.Column(db.String(50))
    creationTime = db.Column(db.DateTime)
    startTime = db.Column(db.DateTime)
    finishTime = db.Column(db.DateTime)

    nodes = db.relationship("Node", secondary=experimentHistory, \
            backref=db.backref("experiments", lazy="dynamic"), lazy="dynamic")

    def __init__(self, name, overlay, nodes):
        self.name = name
        self.overlay = overlay

        for node in nodes:
            if not node.available:
                raise Exception("Some of the selected nodes are already \
                        running an experiment")
            node.activeExperiment = self

        self.nodes.extend(nodes)
        self.status = Experiment.Status.PREPARING
        self.creationTime = datetime.now()

    def __repr__(self):
        return "<Experiment %s - %s>" % (self.name, self.status)

    def start(self):
        if self.status != Experiment.Status.PREPARING:
            raise Exception("Experiment was already started.")

        for node in self.nodes:
            if node.status != Node.Status.READY:
                raise Exception("Node '%s' not ready." % node.id)

        self.status = Experiment.Status.RUNNING
        self.startTime = datetime.now()
        db.session.commit()

    def finish(self):
        if self.status == Experiment.Status.FINISHED:
            return

        self.status = Experiment.Status.FINISHED
        for node in self.nodes:
            node.activeExperiment = None
        self.finishTime = datetime.now()
        db.session.commit()

from .node import Node
