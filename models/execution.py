""" Experiment execution-related functionality. """

from database import db

class Execution(db.Model):
    """
    Represents the execution of a command by a node.
    """

    commandId = db.Column(db.Integer, db.ForeignKey("command.id"), 
            primary_key=True)
    nodeId = db.Column(db.Integer, db.ForeignKey("node.id"), 
            primary_key=True)
    exitCode = db.Column(db.Integer)
    stdout = db.Column(db.Text)
    stderr = db.Column(db.Text)

    command = db.relationship("Command", 
            backref=db.backref("executions", lazy="dynamic"))
    node = db.relationship("Node", 
            backref=db.backref("executions", lazy="dynamic"))

    def __init__(self, commandId, nodeId, exitCode, stdout, stderr):
        self.commandId = commandId
        self.nodeId = nodeId
        self.exitCode = exitCode
        self.stdout = stdout
        self.stderr = stderr
