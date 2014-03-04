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

bpResults = Blueprint("web.results", __name__, template_folder="../templates")

@bpResults.route("/")
def index():
    return redirect(url_for(".list"))

@bpResults.route("/list")
def list():
    RESULTS_DIR = app.config["RESULTS_DIR"]
    dirs = [ f for f in os.listdir(RESULTS_DIR) ]
    return render_template("results/list.html", dirs=dirs)


@bpResults.route("/list/<exp>")
def list_exp(exp):
    # List the existing results
    expDir = os.path.join(app.config["RESULTS_DIR"], exp)
    files = [ f for f in os.listdir(expDir) ]
    logging.debug(files)
    files = filter(lambda x : os.path.isfile(expDir + "/" + x) ,files)
    files = map(lambda x: {"dir" :(x.split("."))[0], "file":x},files)
    logging.debug("The save files are: %s", files)
    return render_template("results/list_exp.html", files=files, expDir=exp)

@bpResults.route("/<expDir>/<filename>")
def saved_file(expDir, filename):
	# Donwload a specific result file if exists
	resPath = os.path.join(app.config['RESULTS_DIR'],expDir)
	filePath = os.path.join(resPath,filename)
	logging.debug(filePath)
	if os.path.isfile(filePath):
		return send_from_directory(resPath, filename)
	else:
		abort(404)

@bpResults.route("/list/<expDir>/<nodeDir>")
def list_res(expDir,nodeDir):
    # List the files of a specific experiment
    resultsDir = os.path.join(app.config["RESULTS_DIR"],expDir,nodeDir)
    files = [ f for f in os.listdir(resultsDir) ]
    return render_template("results/list_res.html", files=files, expDir=expDir, nodeDir=nodeDir)

@bpResults.route("/<expDir>/<nodeDir>/<filename>")
def saved_res(expDir, nodeDir, filename):
	# Donwload a specific result file if exists
	logging.debug("Hi")
	resPath = os.path.join(app.config['RESULTS_DIR'],expDir,nodeDir)
	filePath = os.path.join(resPath,filename)
	logging.debug(filePath)
	if os.path.isfile(filePath):
		return send_from_directory(resPath, filename)
	else:
		abort(404)
