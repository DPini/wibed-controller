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

bpErrorAPI = Blueprint("ErrorAPI", __name__, template_folder="../templates")

@bpErrorAPI.route("/error/<nodeId>", methods=["POST"])
def saveFile(nodeId):
	node = Node.query.get(nodeId)
	if not node:
		logging.debug("ERROR storing file, node not found")
		return jsonify({"exit":"fail"})
	else:
		try:
			logging.debug("/api/error/%s:  Attempt to POST a file",nodeId)
			resultFile = request.files["file"]
			name = secure_filename(resultFile.filename)
			# Create experiment dir if it does not exist
			newDir = os.path.join(app.config["ERROR_DIR"],nodeId)
			try:
				os.mkdir(newDir)
				logging.debug("New dir created")
			except OSError as exc: 
				if exc.errno == errno.EEXIST and os.path.isdir(newDir):
					pass
			# store in experiment dir the tar.gz received including nodes name
			filePath = os.path.join(app.config["ERROR_DIR"],nodeId+".tar.gz")
			logging.debug("Saving the results in : %s", filePath)
			resultFile.save(filePath)
			logging.debug("Extracting the fileis in the folder : %s", newDir)
			tar = tarfile.open(filePath)
			tar.extractall(newDir)
			tar.close()
			return jsonify({"exit":"success"})
		except:
			return jsonify({"exit":"fail"})

