#! /usr/bin/env python

import os

from flask import Flask, redirect, url_for, render_template, request, flash

def create_app(config_object="settings.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from database import db
    db.init_app(app)

    from filters.nl2br import nl2br
    app.jinja_env.filters['nl2br'] = nl2br

    from blueprints.experiment import bpExperiment
    app.register_blueprint(bpExperiment, url_prefix="/experiment")

    from blueprints.node import bpNode
    app.register_blueprint(bpNode, url_prefix="/node")

    from blueprints.command import bpCommand
    app.register_blueprint(bpCommand, url_prefix="/command")

    from blueprints.nodeapi import bpNodeAPI
    app.register_blueprint(bpNodeAPI, url_prefix="/api")

    from blueprints.commandapi import bpCommandAPI
    app.register_blueprint(bpCommandAPI, url_prefix="/api")

    from blueprints.experimentapi import bpExperimentAPI
    app.register_blueprint(bpExperimentAPI, url_prefix="/api")

    from blueprints.admin import bpAdmin
    app.register_blueprint(bpAdmin, url_prefix="/admin")

    from blueprints.firmware import bpFirmware
    app.register_blueprint(bpFirmware, url_prefix="/firmware")

    @app.before_first_request
    def initializeFolders():
        if not os.path.isdir(app.config["OVERLAY_DIR"]):
            os.makedirs(app.config["OVERLAY_DIR"])

        if not os.path.isdir(app.config["FIRMWARE_DIR"]):
            os.makedirs(app.config["FIRMWARE_DIR"])

    @app.route("/")
    def index():
            return redirect(url_for("login"))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
	     error = None
	     if request.method == 'POST':
		     if request.form['username'] != 'wibed' or \
				     request.form['password'] != 'wibed':
			 error = 'Invalid credentials'
		     else:
			 flash('You were successfully logged in')
			 return redirect(url_for("experiment.list"))
	     return render_template('login.html', error=error)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
