""" Wibed experiment-api functionality. """

from flask import Blueprint, jsonify
from models.experiment import Experiment
from blueprints.userapi.commandapi import commandExecutions
import logging

bpExperimentAPI = Blueprint("userAPI.experiment", __name__, template_folder="../templates")

@bpExperimentAPI.route("/experimentInfo/<name>", methods=["GET"])
def experimentInfo(name):
    experiment = Experiment.query.filter_by(name=name).first()
    if experiment:
    	nodes = experiment.nodes
	resultName = name+"_"+str(experiment.creationTime)
	resultName = resultName.replace(" ","_")
	resultName = resultName.replace(":","-")
        output = {
            	"id": experiment.id,
                "nodes": [node.id for node in experiment.nodes],
                "commands": [command.id for command in experiment.commands],
		"resultdir": resultName
                }
        return jsonify(output)

    else:
        return jsonify({"error": "wrong ID"})

@bpExperimentAPI.route("/experimentNodes/<name>", methods=["GET"])
def experimentNodes(name):
    experiment = Experiment.query.filter((Experiment.name==name) & (Experiment.status==Experiment.Status.RUNNING) ).first()
    if experiment:
    	nodes = experiment.nodes
        output = {
                "nodes": [node.id for node in experiment.nodes],
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
