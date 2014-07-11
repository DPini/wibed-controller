""" Testbed node-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for, session, current_app as app
from database import db
from models.experiment import Experiment
from models.node import Node
import logging

import os
import json


EXP_NAME="WibedTopology"

bpTopology = Blueprint("web.topology", __name__, template_folder="../templates")

@bpTopology.route("/")
def index():
	JS = app.config["JS_DIR"]
	jsTopo = os.path.join(JS,"topo.js")
	if not os.path.isfile(jsTopo):
		getData()
    	return render_template("topology/index.html")

@bpTopology.route("/getresults")
def getresults():
	getData()
	return render_template("topology/index.html")

def getData():
	nodes_js = list()
	edges_js = list()
	# Find latest experiment
	experiment = Experiment.query.filter( Experiment.name == EXP_NAME).order_by(db.desc(Experiment.finishTime)).first()
	logging.debug("%s,%s",experiment.id,experiment.name)
	
	# Create list of nodes in vis.js format
	nodes = experiment.nodes.all()
	for node in nodes:
		node_js= {"id": nodes.index(node), "label":node.id}
		nodes_js.append(node_js)
	logging.debug(nodes_js)
	
	# Create list of edje in vis.js format reading from the result files
	## Recover name of results directory
	resultName = EXP_NAME+"_"+str(experiment.creationTime)
	resultName = resultName.replace(" ","_")
	resultName = resultName.replace(":","-")
	RESULTS_DIR = app.config["RESULTS_DIR"]
	TOPO_RESULTS = os.path.join(RESULTS_DIR,resultName)
	logging.debug(TOPO_RESULTS)
	
	for node in nodes:
		NODE_TOPO_RESULTS = os.path.join(TOPO_RESULTS,resultName+"_"+node.id,"topo.txt")
		logging.debug("NODE TOPO RESULTS 1 %s",NODE_TOPO_RESULTS)
		infile = open(NODE_TOPO_RESULTS)
		for line in infile:
			tmp = line.rstrip('\n')
			tmp = tmp.split(',')
			nodeTo = [n for n in nodes if n.id == tmp[0]][0]
			toId = nodes.index(nodeTo)
			edge_js = { "from": nodes.index(node), "to": toId, "value": tmp[1], "label": tmp[1]}
			edges_js.append(edge_js)
	
	# Write nodes and edjes in json format in javascript file static/js/topo.js
	JS = app.config["JS_DIR"]
	jsTopo = os.path.join(JS,"topo.js")
	f = open(jsTopo,"w")
	print>> f, "var nodes = ["
	for item in nodes_js:
		f.write("%s,\n" % json.dumps(item))
	print>> f, "];\n"
	print>> f, "var edges = ["
	for item in edges_js:
		f.write("%s,\n" % json.dumps(item))
	print>> f, "];"
	f.close()
