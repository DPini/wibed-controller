""" Wibed node-api functionality. """

import logging

from datetime import datetime

from flask import Blueprint, request, jsonify, json

from database import db
from models.node import Node
from models.experiment import Experiment
from models.command import Command
from models.execution import Execution
from models.firmware import Firmware

bpNodeAPI = Blueprint("nodeAPI", __name__, template_folder="../templates")

@bpNodeAPI.route("/wibednode/<id>", methods=["POST"])
def wibednode(id):
    logging.debug('Node request from node with id %s', id)
    output = {}
    logging.debug('NODE REQUEST: %s', request.get_json(force=True))

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

        handleFirmwareUpgrade(node, input, output)

        handleCommands(node, input, output)

    except Exception as e:
        logging.debug('Exception joining node: %s', e)
        output["errors"] = [str(e)]
        db.session.rollback()

    logging.debug('SERVER REPLY: %s', output)
    return jsonify(**output)

def validateInput(input):
    if not input:
        raise Exception("No input data provided.")

    if not "status" in input:
        raise Exception("No status information provided.")

    # Convert INT representation of status to Enum.
    input["status"] = Node.Status(input["status"])

    if input["status"] == Node.Status.INIT:
        if not "model" in input:
            raise Exception("No model information provided.")

        if not "version" in input:
            raise Exception("No firmware version information provided.")

def updateNode(node, input):
    if "model" in input:
        node.model = input["model"]
    if "version" in input:
        firmwareVersion = input["version"]
        try:
            firmware = Firmware.query.filter(Firmware.version == firmwareVersion).one()
        except Exception:
            firmware = Firmware(firmwareVersion)
            db.session.add(firmware)

        node.installedFirmware = firmware

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
        elif node.status == Node.Status.READY and \
             activeExperiment.status == Experiment.Status.RUNNING:
            output["experiment"] = {}
            output["experiment"]["action"] = "RUN"
	elif node.status == Node.Status.DEPLOYING or node.status == Node.Status.RESETTING:
	    output["experiment"] = {}
    # If node is not in an active experiment but still thinks it is,
    # tell it to finish
    else:
        if node.status in [Node.Status.PREPARING, Node.Status.READY, Node.Status.DEPLOYING, Node.Status.RUNNING]:
            output["experiment"] = {}
            output["experiment"]["action"] = "FINISH"

def handleFirmwareUpgrade(node, input, output):
    # If node is not idle or init, nothing to do
    if node.status not in [Node.Status.INIT, Node.Status.IDLE]:
        return

    activeUpgrade = node.activeUpgrade

    # If node is involved in an active upgrade
    if activeUpgrade is not None:

        # If node finished firmware upgrade
        if node.installedFirmware.version == activeUpgrade.firmware.version:
            node.activeUpgrade = None
            db.session.commit()
        # Else if node still has to start the upgrade, send upgrade data
        else:
            output["upgrade"] = {}
            output["upgrade"]["version"] = activeUpgrade.firmware.version
            output["upgrade"]["utime"] = activeUpgrade.upgradeTime.timestamp()
            output["upgrade"]["hash"] = activeUpgrade.firmware.hash

def handleCommands(node, input, output):
    activeExperiment = node.activeExperiment
    logging.debug('Active experiment? %s', activeExperiment)

    commandAck = input.get("commandAck", 0)
    missingCommands = (
                db.session.query(Command)
                .join(Command.nodes)     # It's  necessary to join the "children" of
                                         #Command
                .filter(Command.id > commandAck)
                # here comes the magic:  
                # you can filter with Node even though it was not directly joined
                .filter(Node.id == node.id) 
        )

    commandsToSend = []

    for command in missingCommands:
        if command.experiment is not None: 
            # If command is associated with an old experiment, ignore.
            if not activeExperiment or \
                activeExperiment.id != command.experiment.id:
                continue
            # If it is associated with a experiment which is still not
            # running, ignore too.
            elif command.experiment.status != Experiment.Status.RUNNING:
                continue

        commandsToSend.append(command)

    if node.status in [Node.Status.IDLE, Node.Status.RUNNING]:
        if len(commandsToSend) > 0:
            output["commands"] = \
                    {c.id: c.command for c in commandsToSend}
        # Check and add results provided by node
        handleResults(node, input, output)

def handleResults(node, input, output):
    results = input.get("results", [])

    if results:
        for commandId, result in results.items():
            (exitCode, stdout, stderr) = result
            execution = Execution(commandId, node.id, exitCode, stdout, stderr)
            # Insert or Update if already exists
            db.session.merge(execution)
        db.session.commit()

    lastNodeExecution = node.executions.order_by(Execution.commandId.desc()).first()

    if lastNodeExecution:
        output["resultAck"] = lastNodeExecution.commandId
