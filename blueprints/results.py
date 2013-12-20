""" Testbed node-related functionality. """

import os

import logging

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for, current_app as app
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
    RESULTS_DIR = app.config["RESULTS_DIR"]
    files = [ f for f in os.listdir(RESULTS_DIR) ]
    logging.debug(files)
    files = filter(lambda x : os.path.isfile(RESULTS_DIR + "/" + x) ,files)
    files = map(lambda x: {"dir" :(x.split("."))[0], "file":x},files)
    logging.debug("The save files are: %s", files)
    return render_template("results/list.html", files=files)

@bpResults.route("/<filename>")
def saved_file(filename):
	return send_from_directory(app.config['RESULTS_DIR'],
			filename)

@bpResults.route("/<exp>/<filename>")
def saved_result(exp, filename):
	return send_from_directory(app.config['RESULTS_DIR'],exp+"/"+filename)

@bpResults.route("/list/<exp>")
def list_res(exp):
    RESULTS_DIR = app.config["RESULTS_DIR"]
    files = [ f for f in os.listdir(RESULTS_DIR+"/"+exp) ]
    return render_template("results/list_res.html", files=files, exp=exp)
