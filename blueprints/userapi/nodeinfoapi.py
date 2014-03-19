""" Wibed command-api functionality. """
import logging

from flask import Blueprint, jsonify
from models.node import Node

bpNodeInfoAPI = Blueprint("userAPI.nodeinfo", __name__, template_folder="../templates")

def getInfo(node):
    logging.debug("The node model is: %s",node.model)
    output = {"status": str(node.status),
	      "model": node.model,
              "firmware": node.installedFirmware.version,
	      "description": node.description
	      }
    logging.debug(output)
    return output

@bpNodeInfoAPI.route("/nodeinfo/<id>", methods=["GET"])
def nodeInfo(id):
    node = Node.query.get(id)
    if node:
        output = getInfo(node)
        return jsonify(output)
    else:
        return jsonify({"error": "wrong ID"})
