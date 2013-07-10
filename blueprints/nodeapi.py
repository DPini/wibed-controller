""" Wibed node-api functionality. """

from datetime import datetime

from flask import Blueprint, request, jsonify, json

from database import db
from models.node import Node
from models.experiment import Experiment
from models.command import Command
from models.execution import Execution

bpNodeAPI = Blueprint("nodeAPI", __name__, template_folder="../templates")

@bpNodeAPI.route("/wibednode/<id>", methods=["POST"])
def wibednode(id):
    output = {}

    try:
        input = json.loads(request.data)
        validateInput(input)

        # Attempt to get existing node from id
        node = Node.query.get(id)

        # If it doesn't exist, create a new one
        if not node:
            node = Node(id)
            db.session.add(node)

        # Update node fields based on input
        updateNode(node, input)

        handleExperimentData(node, input, output)

        handleFirmwareUpdate(node, input, output)
    except Exception as e:
        
        output["errors"] = [str(e)]
        db.session.rollback()

    return jsonify(**output)

def validateInput(input):
    if not input:
        raise Exception("No input data provided.")

    if not "model" in input:
        raise Exception("No model information provided.")

    if not "version" in input:
        raise Exception("No firmware version information provided.")

    if not "status" in input:
        raise Exception("No status information provided.")

    # Convert INT representation of status to Enum.
    input["status"] = Node.Status(input["status"])

def updateNode(node, input):
    node.model = input["model"]
    node.version = input["version"]
    node.lastContact = datetime.now()
    node.status = input["status"]
    db.session.commit()

def handleExperimentData(node, input, output):
    activeExperiment = node.activeExperiment
    # If node is participating in an active experiment
    if activeExperiment:
        # If node is idle, it first has to prepare the 
        # experiment -> install overlay
        if node.status == Node.Status.IDLE:
            output["experiment"] = {}
            output["experiment"]["id"] = activeExperiment.id
            output["experiment"]["action"] = "PREPARE"
            output["experiment"]["overlay"] = activeExperiment.overlay
        # Else, if node is ready or running and experiment has
        # started, send missing commands (if any)
        elif node.status in [Node.Status.READY, Node.Status.RUNNING] and \
             activeExperiment.status == Experiment.Status.RUNNING:
            commandAck = input.get("commandAck", 0)
            output["experiment"] = {}
            output["experiment"]["action"] = "RUN"

            missingCommands = activeExperiment.commands.\
                              filter(Command.id > commandAck).all()

            output["experiment"]["commands"] = \
                    [(c.id, c.command) for c in missingCommands]

            # Check and add results provided by node
            handleExperimentResults(node, activeExperiment, input, output)
    # If node is not in an active experiment but still thinks it is,
    # tell it to finish
    else:
        if node.status not in [Node.Status.IDLE, Node.Status.UPGRADING]:
            output["experiment"] = {}
            output["experiment"]["action"] = "FINISH"

def handleFirmwareUpdate(node, input, output):
    # TODO: Implement this
    pass

def handleExperimentResults(node, experiment, input, output):
    results = input.get("results", [])

    for result in results:
        (commandId, exitCode, stdout, stderr) = result
        execution = Execution(commandId, node.id, exitCode, stdout, stderr)
        # Insert or Update if already exists
        db.session.merge(execution)
    db.session.commit()

    lastNodeExecution = node.executions.order_by(Execution.commandId.desc()).first()

    if lastNodeExecution:
        output["resultAck"] = lastNodeExecution.commandId
