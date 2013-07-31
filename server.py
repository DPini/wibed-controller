#! /usr/bin/env python

import os

from flask import Flask, redirect, url_for

from database import db

app = Flask(__name__)
app.config.from_object("settings.DevelopmentConfig")
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
    return redirect(url_for("experiment.list"))

if __name__ == "__main__":
    app.run()
