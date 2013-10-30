""" Wibed command-api functionality. """

from flask import Blueprint, jsonify
from models.execution import Execution
from models.command import Command

bpCommandAPI = Blueprint("commandAPI", __name__, template_folder="../templates")

def commandExecutions(command):
    executions = Execution.query.filter(Execution.commandId==command.id)
    output = {"commandId": command.id, "command": command.command,
              "executions": []}

    for execution in executions:
        output["executions"].append(
            {"node": execution.node.id,
             "result":
                 {"exitCode": execution.exitCode,
                  "stdout": execution.stdout,
                  "stderr": execution.stderr
                 }
            }
        )
    return output

@bpCommandAPI.route("/commandOutput/<id>", methods=["GET"])
def commandOutput(id):
    command = Command.query.get(id)
    if command:
        output = commandExecutions(command)
        return jsonify(output)
    else:
        return jsonify({"error": "wrong ID"})
