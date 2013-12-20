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
		#name = request.form["name"]
		name = secure_filename(resultFile.filename)
		expId = int((name.split("."))[0])
		logging.debug("The id of the experiments is: %s", expId)
		exp = Experiment.query.get(expId)
		if True :
			logging.debug(exp)
			logging.debug(exp.name)
			# Better  solution the experiment idi guess
			#expName = exp.name if exp else str(expId)
			expName  =  str(expId)
			logging.debug("The name of the experiments is: %s", expName)
			filePath = os.path.join(app.config["RESULTS_DIR"],name)
			logging.debug("Saving the file in : %s", filePath)
			resultFile.save(filePath)
			newDir = os.path.join(app.config["RESULTS_DIR"],expName)
			logging.debug("Extracting the file in : %s", newDir)
			try:
				os.mkdir(newDir)
				logging.debug("New dir created")
			except OSError as exc: 
				if exc.errno == errno.EEXIST and os.path.isdir(newDir):
					pass
			tar = tarfile.open(filePath)
			tar.extractall(newDir)
			tar.close()
			logging.debug("The file %s is saved", name)
			return jsonify({"exit":"success"})
		else :
			return jsonify({"exit":"fail"})
	except:
		return jsonify({"exit":"fail"})


