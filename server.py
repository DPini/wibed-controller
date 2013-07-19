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

if not os.path.isdir(app.config["OVERLAY_DIR"]):
    os.makedirs(app.config["OVERLAY_DIR"])

@app.route("/")
def index():
    return redirect(url_for("experiment.list"))

if __name__ == "__main__":
    app.run()
