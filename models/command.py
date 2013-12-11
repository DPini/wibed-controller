""" Experiment command-related functionality. """

from database import db

from models.experiment import Experiment

commandTargets = db.Table('commandTargets',
    db.Column('command_id', db.Integer, db.ForeignKey('command.id')),
    db.Column('node_id', db.Integer, db.ForeignKey('node.id'))
)

class Command(db.Model):
    """
    Represents a command in a testbed experiment.
    """
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    experimentId = db.Column(db.Integer, db.ForeignKey("experiment.id"))
    command = db.Column(db.Text)

    experiment = db.relationship("Experiment", \
        backref=db.backref("commands", lazy="dynamic"))

    nodes = db.relationship("Node", secondary=commandTargets, \
            backref=db.backref("commands", lazy="dynamic"), lazy="dynamic")

    def __init__(self, command, experimentId=None, nodes=[]):
        self.command = command

        if experimentId:
            if len(nodes) == 0:
                nodes = Experiment.query.get(experimentId).nodes.all()
        elif len(nodes) == 0:
            raise ValueError("Cannot add command with no target nodes")

        self.experimentId = experimentId
        self.nodes.extend(nodes)

