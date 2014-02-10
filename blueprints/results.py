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

bpResults = Blueprint("results", __name__, template_folder="../templates")

@bpResults.route("/")
def index():
    return redirect(url_for(".list"))

@bpResults.route("/list")
def list():
    # List the existing results
    RESULTS_DIR = app.config["RESULTS_DIR"]
    files = [ f for f in os.listdir(RESULTS_DIR) ]
    logging.debug(files)
    files = filter(lambda x : os.path.isfile(RESULTS_DIR + "/" + x) ,files)
    files = map(lambda x: {"dir" :(x.split("."))[0], "file":x},files)
    logging.debug("The save files are: %s", files)
    return render_template("results/list.html", files=files)

@bpResults.route("/<filename>")
def saved_file(filename):
	# Download the tarball with all the results if exists 
	resPath = os.path.join(app.config['RESULTS_DIR'],filename)
	if os.path.isfile(resPath):
		return send_from_directory(app.config['RESULTS_DIR'],filename)
	else:
		abort(404)

@bpResults.route("/<exp>/<filename>")
def saved_result(exp, filename):
	# Donwload a specific result file if exists
	resDir = os.path.join(app.config['RESULTS_DIR'],exp)
	resPath = os.path.join(resDir,filename)
	if os.path.isfile(resPath):
		return send_from_directory(resDir, filename)
	else:
		abort(404)

@bpResults.route("/list/<exp>")
def list_res(exp):
    # List the files of a specific experiment
    resultsDir = os.path.join(app.config["RESULTS_DIR"],exp)
    files = [ f for f in os.listdir(resultsDir) ]
    return render_template("results/list_res.html", files=files, exp=exp)
