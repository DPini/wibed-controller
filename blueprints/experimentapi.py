""" Wibed experiment-api functionality. """

from flask import Blueprint, jsonify
from models.experiment import Experiment
from blueprints.commandapi import commandExecutions

bpExperimentAPI = Blueprint("experimentAPI", __name__, template_folder="../templates")

@bpExperimentAPI.route("/experimentInfo/<id>", methods=["GET"])
def experimentInfo(id):
    experiment = Experiment.query.get(id)
    if experiment:
        output = {
            experiment.id: {
                "nodes": [node.id for node in experiment.nodes],
                "commands": [command.id for command in experiment.commands]
                }
            }
        return jsonify(output)

    else:
        return jsonify({"error": "wrong ID"})

@bpExperimentAPI.route("/experimentOutput/<id>", methods=["GET"])
def experimentOutput(id):
    experiment = Experiment.query.get(id)
    if experiment:
        output = {"experimentId": experiment.id, "experiment": experiment.name,
                  "commands": []}

        for command in experiment.commands:
            commandOutput = commandExecutions(command)
            output["commands"].append(commandOutput)
        return jsonify(output)
    else:
        return jsonify({"error": "wrong ID"})
