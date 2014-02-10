import os

import errno
import tarfile


import logging

from flask import Blueprint, jsonify
from flask import request, render_template, flash, redirect, \
		  url_for, current_app as app
from werkzeug import secure_filename

from models.experiment import Experiment


bpResultsAPI = Blueprint("ResultsAPI", __name__, template_folder="../templates")

@bpResultsAPI.route("/results", methods=["POST"])
def saveFile():
	try:
		logging.debug("/api/results:  Attempt to POST a file")
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
			filePath = os.path.join(app.config["RESULTS_DIR"],expName+".tar.gz")
			logging.debug("Saving the results in : %s", filePath)
			resultFile.save(filePath)
			newDir = os.path.join(app.config["RESULTS_DIR"],expName)
			logging.debug("Extracting the fileis in the folder : %s", newDir)
			try:
				os.mkdir(newDir)
				logging.debug("New dir created")
			except OSError as exc: 
				if exc.errno == errno.EEXIST and os.path.isdir(newDir):
					pass
			tar = tarfile.open(filePath)
			tar.extractall(newDir)
			tar.close()
			return jsonify({"exit":"success"})
		# If the experiment does not exist
		else :
			logging.debug("ERROR storing file, no relevant experiment found")
			return jsonify({"exit":"fail"})
	except:
		return jsonify({"exit":"fail"})


