""" Testbed node-related functionality. """

import os

import logging

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for, abort, current_app as app
from flask import send_from_directory

from database import db
from models.node import Node
from models.execution import Execution

bpError = Blueprint("web.error", __name__, template_folder="../templates")

@bpError.route("/")
def index():
    return redirect(url_for(".list"))

@bpError.route("/list")
def list():
    # List the existing logs
    errorDir = app.config["ERROR_DIR"]
    files = [ f for f in os.listdir(errorDir) ]
    files = filter(lambda x : os.path.isfile(errorDir + "/" + x) ,files)
    files = map(lambda x: {"dir" :(x.split("."))[0], "file":x},files)
    logging.debug("The error files are: %s", files)
    return render_template("error/list.html", files=files)

@bpError.route("/<filename>")
def saved_file(filename):
	# Donwload a specific log file if exists
	filePath = os.path.join(app.config['ERROR_DIR'],filename)
	logging.debug(filePath)
	if os.path.isfile(filePath):
		return send_from_directory(app.config['ERROR_DIR'], filename)
	else:
		abort(404)

@bpError.route("/list/<nodeDir>")
def list_node(nodeDir):
    # List the log files of a specific node
    resultsDir = os.path.join(app.config["ERROR_DIR"],nodeDir)
    files = [ f for f in os.listdir(resultsDir) ]
    return render_template("error/list_logs.html", files=files, nodeDir=nodeDir)

@bpError.route("/<nodeDir>/<filename>")
def saved_log(nodeDir, filename):
	# Donwload a specific log file if exists
	logging.debug("Hi")
	resPath = os.path.join(app.config['ERROR_DIR'],nodeDir)
	filePath = os.path.join(resPath,filename)
	logging.debug(filePath)
	if os.path.isfile(filePath):
		return send_from_directory(resPath, filename)
	else:
		abort(404)
