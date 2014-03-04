""" Experiment command-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                url_for

from database import db
from models.command import Command
from models.node import Node

bpCommand = Blueprint("web.command", __name__, template_folder="../templates")

@bpCommand.route("/show/<id>")
def show(id):
    command = Command.query.get_or_404(id)
    executions = command.executions.all();
    # Get all nodes except those associated with executions
    # of this command
    pendingNodes = command.nodes.except_(\
            command.nodes.join(\
            command.executions.subquery())).all()
    return render_template("command/show.html", command=command, \
            executions=executions, pendingNodes=pendingNodes)

@bpCommand.route("/add", methods = ["POST"])
def add():
    commandString = request.form["command"]
    experimentId = None
    nodes = []

    try:
        experimentId = request.form["experimentId"]
    except KeyError:
        pass

    try:
        nodes = Node.query.filter(Node.id.in_(request.form.getlist("nodeIds"))).all()
    except KeyError:
        pass

    try:
        command = Command(commandString, experimentId, nodes)
        db.session.add(command)
        db.session.commit()
        flash("Command '%s' added successfully" % commandString)
    except Exception as e:
        db.session.rollback()
        flash("Error adding command '%s': %s" % (commandString, str(e))) 
    if experimentId:
        return redirect(url_for("web.experiment.show", id=experimentId))
    else:
        return redirect(url_for("web.admin.index"))
