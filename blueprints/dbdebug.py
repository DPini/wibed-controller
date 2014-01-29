""" Testbed node-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for, session

from database import db
from models.node import Node
from models.experiment import Experiment
from models.command import Command
from models.firmware import Upgrade, Firmware
from restrictions import admin_required

import logging

bpDb = Blueprint("dbdebug", __name__, template_folder="../templates")

@bpDb.before_request
def restrict():
	return admin_required()

#bpDb.before_request(restrictions.admin_required())

@bpDb.route("/")
def index():
    return redirect(url_for(".list"))

@bpDb.route("/list")
def list():
    nodes = Node.query.all()
    experiments = Experiment.query.all()
    commands = Command.query.all()
    upgrades = Upgrade.query.all()
    firmwares  = Firmware.query.all()

    return render_template("dbdebug/list.html", nodes=nodes, experiments=experiments, commands=commands, upgrades=upgrades, firmwares= firmwares)

