""" Admin-related functionality. """

from flask import Blueprint
from flask import render_template

from models.node import Node
from models.command import Command

from restrictions import get_nodes

bpAdmin = Blueprint("admin", __name__, template_folder="../templates")

@bpAdmin.route("/")
def index():
    commands = Command.query.filter(Command.experimentId == None).all()

    return render_template("admin/index.html", commands=commands,\
			nodes=get_nodes("Node.available == True"))
