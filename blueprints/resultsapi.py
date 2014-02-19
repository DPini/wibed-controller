import os

import errno
import tarfile


import logging

from flask import Blueprint, jsonify
from flask import request, render_template, flash, redirect, \
		  url_for, current_app as app
from werkzeug import secure_filename

from models.experiment import Experiment
from models.node import Node

bpResultsAPI = Blueprint("ResultsAPI", __name__, template_folder="../templates")

@bpResultsAPI.route("/results/<nodeId>", methods=["POST"])
def saveFile(nodeId):
	node = Node.query.get(nodeId)
	if not node:
		logging.debug("ERROR storing file, node not found")
		return jsonify({"exit":"fail"})
	else:
		try:
			logging.debug("/api/results/%s:  Attempt to POST a file",nodeId)
			resultFile = request.files["file"]
			name = secure_filename(resultFile.filename)
			expId = int((name.split("."))[0])
			exp = Experiment.query.get(int(expId))
			# If the experiment exists
			if exp :
				logging.debug(exp)
				# Naming of folders and files
				expName = exp.name+"_"+str(exp.creationTime)
				expName=expName.replace(" ","_")
				expName=expName.replace(":","-")
				expName=(expName.split("."))[0]
				logging.debug("The name of the experiment file is: %s", expName)
				# Create experiment dir if it does not exist
				newDir = os.path.join(app.config["RESULTS_DIR"],expName)
				try:
					os.mkdir(newDir)
					logging.debug("New dir created")
				except OSError as exc: 
					if exc.errno == errno.EEXIST and os.path.isdir(newDir):
						pass
				# store in experiment dir the tar.gz received including nodes name
				filePath = os.path.join(newDir,expName+"_"+nodeId+".tar.gz")
				logging.debug("Saving the results in : %s", filePath)
				resultFile.save(filePath)
				# create node dir and extract results in there
				nodeDir = os.path.join(newDir,expName+"_"+nodeId)
				logging.debug("Extracting the fileis in the folder : %s", nodeDir)
				try:
					os.mkdir(nodeDir)
					logging.debug("Node created")
				except OSError as exc: 
					if exc.errno == errno.EEXIST and os.path.isdir(newDir):
						pass
				tar = tarfile.open(filePath)
				tar.extractall(nodeDir)
				tar.close()
				return jsonify({"exit":"success"})
			# If the experiment does not exist
			else :
				logging.debug("ERROR storing file, no relevant experiment found")
				return jsonify({"exit":"fail"})
		except:
			return jsonify({"exit":"fail"})


