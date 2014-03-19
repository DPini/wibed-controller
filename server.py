#! /usr/bin/env python

import os
import logging

from flask import Flask, redirect, url_for, render_template, request, flash, session, escape, abort
from forms import LoginForm
# Enable for degubbing purposes
# Needs flask_debugtoolbar installed
#from flask_debugtoolbar import DebugToolbarExtension

def create_app(config_object="settings.DevelopmentConfig"):
    #Create Flask app
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Enable for degubbing purposes
    # Needs flask_debugtoolbar installed
    #toolbar = DebugToolbarExtension(app)

    #Define log level
    logLevel= logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(filename='/var/log/wibed-server.log',level = logLevel)
    logging.info('Started')
    logging.debug('Debug mode enabled')


    #Import initalized db
    from database import db
    db.init_app(app)

    #Load filters
    from filters.nl2br import nl2br
    app.jinja_env.filters['nl2br'] = nl2br

    ## Load blueprints
    # Web

    from blueprints.web.experiment import bpExperiment
    app.register_blueprint(bpExperiment, url_prefix="/experiment")

    from blueprints.web.node import bpNode
    app.register_blueprint(bpNode, url_prefix="/node")
    
    from blueprints.web.command import bpCommand
    app.register_blueprint(bpCommand, url_prefix="/command")

    from blueprints.web.admin import bpAdmin
    app.register_blueprint(bpAdmin, url_prefix="/admin")

    from blueprints.web.firmware import bpFirmware
    app.register_blueprint(bpFirmware, url_prefix="/firmware")
    
    from blueprints.web.results import bpResults
    app.register_blueprint(bpResults, url_prefix="/results")
    
    from blueprints.web.error import bpError
    app.register_blueprint(bpError, url_prefix="/error")

    from blueprints.web.repo import bpRepo
    app.register_blueprint(bpRepo, url_prefix="/wibed")
    
    	#DB debug page
    if app.debug :
	    from blueprints.web.dbdebug import bpDb
	    app.register_blueprint(bpDb, url_prefix="/dbdebug")

    # Node API

    from blueprints.nodeapi.nodeapi import bpNodeAPI
    app.register_blueprint(bpNodeAPI, url_prefix="/api")

    from blueprints.nodeapi.errorapi import bpErrorAPI
    app.register_blueprint(bpErrorAPI, url_prefix="/api")

    from blueprints.nodeapi.resultsapi import bpResultsAPI
    app.register_blueprint(bpResultsAPI, url_prefix="/api")
    
    # User API
    
    from blueprints.userapi.nodeinfoapi import bpNodeInfoAPI
    app.register_blueprint(bpNodeInfoAPI, url_prefix="/api")

    from blueprints.userapi.commandapi import bpCommandAPI
    app.register_blueprint(bpCommandAPI, url_prefix="/api")

    from blueprints.userapi.experimentapi import bpExperimentAPI
    app.register_blueprint(bpExperimentAPI, url_prefix="/api")
    

    #Initiliaze App
    @app.before_first_request
    def initialize():
	    initializeFolders()
	    initializeUsers()

    def initializeFolders():
        if not os.path.isdir(app.config["OVERLAY_DIR"]):
            os.makedirs(app.config["OVERLAY_DIR"])

        if not os.path.isdir(app.config["FIRMWARE_DIR"]):
            os.makedirs(app.config["FIRMWARE_DIR"])

        if not os.path.isdir(app.config["RESULTS_DIR"]):
            os.makedirs(app.config["RESULTS_DIR"])
    
        if not os.path.isdir(app.config["ERROR_DIR"]):
            os.makedirs(app.config["ERROR_DIR"])

    def initializeUsers():
	    from database import db
	    from models.user import User
	    #Create db Users
	    admin = User("admin","wibed")
	    user = User("wibed","wibed")
	    db.session.add(admin)
	    db.session.add(user)
	    db.session.commit()
	    
    @app.before_request
    def authorize():
	    logging.debug("BLUEPRINT: %s",request.endpoint)
	    #Guarantee that only logged in users have access to the services
	    if 'user' not in session:
		    if not request.endpoint or (("nodeAPI" not in request.endpoint) and ("userAPI" not in request.endpoint) and request.endpoint not in ['login','static', 'bpRepo.autoindex', '__autoindex__.static', 'bpRepo.silkicon']) :
			    flash("Not logged in")
			    return redirect(url_for('login'))
		    
	    #Associate bluprints with user role
	    adminBp = ["index", "static", "login", "logout", "firmware","dbdebug","admin", "node", "command", "error"]
	    userBp = ["index", "static", "login", "logout", "experiment", "node", "results", "admin", "command", "error"]

	    if ('user' in session) and request.endpoint and "nodeAPI" not in request.endpoint:
		    logging.debug("BLUEPRINT: %s",request.endpoint)
		    if session['user'] == "admin" :
			    if not [bp for bp in adminBp if bp in request.endpoint]  :
				    abort(401)
		    else:
			    if not [bp for bp in userBp if bp in request.endpoint]  :
				    abort(401)

    #Default route
    @app.route("/")
    def index():
	    if 'user' in session:
		    logging.debug("DEFAULT ROUTE for User: %s", session['user'])
		    if session['user'] == "admin" :
			    return redirect(url_for('web.admin.index'))
		    else:
			    return redirect(url_for("web.experiment.list"))
            return redirect(url_for("login"))

    #Login page
    @app.route('/login', methods=['GET', 'POST'])
    def login():
	    form = LoginForm()
	    #error = None
	    if request.method == 'POST':
		    if form.validate() == False:
			    return render_template('login.html', form=form)
		    else:
			 msg = "Succesfully logged in as: "+form.name.data
			 flash(msg)
			 session['user'] = form.name.data
			 return redirect(url_for("index"))
	    elif request.method == 'GET':
		     return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
	    if 'user' not in session:
		    flash("Not logged in")
		    return redirect(url_for('login'))
	    logging.debug(escape(session['user']))
	    session.pop('user', None)
	    return redirect(url_for('index'))

    return app

#In case of an external WSGI container this is not called
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
