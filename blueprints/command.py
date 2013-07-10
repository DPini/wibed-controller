""" Experiment command-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                url_for

from database import db
from models.command import Command

bpCommand = Blueprint("command", __name__, template_folder="../templates")

@bpCommand.route("/show/<id>")
def show(id):
    command = Command.query.get_or_404(id)
    executions = command.executions.all();
    # Get all nodes except those associated with executions
    # of this command
    pendingNodes = command.experiment.nodes.except_(\
            command.experiment.nodes.join(\
            command.executions.subquery())).all()
    return render_template("command/show.html", command=command, \
            executions=executions, pendingNodes=pendingNodes)

@bpCommand.route("/add", methods = ["POST"])
def add():
    commandString = request.form["command"]
    experimentId = request.form["experimentId"]
    try:
        command = Command(experimentId, commandString)
        db.session.add(command)
        db.session.commit()
        flash("Command '%s' added successfully" % commandString)
    except Exception as e:
        db.session.rollback()
        flash("Error adding command '%s': %s" % (command, str(e))) 
    return redirect(url_for("experiment.show", id=experimentId))
