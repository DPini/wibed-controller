""" Admin-related functionality. """

from flask import Blueprint
from flask import render_template, redirect, url_for

from models.node import Node
from models.command import Command

from database import db

from restrictions import get_nodes

bpAdmin = Blueprint("admin", __name__, template_folder="../templates")

@bpAdmin.route("/")
def index():
    commands = Command.query.filter(Command.experimentId == None).all()

    return render_template("admin/index.html", commands=commands,\
			nodes=get_nodes("Node.available == True"))


@bpAdmin.route("/delCom")
def delCom():
	for command in Command.query.filter(Command.experimentId == None).all() :
		if command.executions.count() == command.nodes.count():
			for execution in command.executions.all():
		    		db.session.delete(execution)
	    		db.session.delete(command)
    	db.session.commit()
    	return redirect(url_for(".index"))


