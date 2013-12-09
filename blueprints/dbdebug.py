""" Testbed node-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for

from database import db
from models.node import Node
from models.experiment import Experiment
from models.command import Command

bpDb = Blueprint("dbdebug", __name__, template_folder="../templates")

@bpDb.route("/")
def index():
    return redirect(url_for(".list"))

@bpDb.route("/list")
def list():
    nodes = Node.query.all()
    experiments = Experiment.query.all()
    commands = Command.query.all()

    return render_template("dbdebug/list.html", nodes=nodes, experiments=experiments, commands=commands)

