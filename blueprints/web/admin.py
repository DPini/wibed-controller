""" Admin-related functionality. """

from flask import Blueprint
from flask import render_template, redirect, url_for

from models.node import Node
from models.command import Command

from database import db

from restrictions import get_nodes

bpAdmin = Blueprint("web.admin", __name__, template_folder="../templates")

@bpAdmin.route("/")
def index():
    commands = Command.query.filter(Command.experimentId == None).all()

    # Example how to use get_nodes
    #availNodes = get_nodes("Node.available == True")
    # Show available nodes and also those in error state so you can run
    # commands to them
    tempNodes = get_nodes(None)
    nodes = [node for node in tempNodes if (node.available == True or node.status.name == "ERROR")]
    return render_template("admin/index.html", commands=commands,\
			nodes=nodes)


@bpAdmin.route("/delCom")
def delCom():
	for command in Command.query.filter(Command.experimentId == None).all() :
		if command.executions.count() == command.nodes.count():
			for execution in command.executions.all():
		    		db.session.delete(execution)
	    		db.session.delete(command)
    	db.session.commit()
    	return redirect(url_for(".index"))
