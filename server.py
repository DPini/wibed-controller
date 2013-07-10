#! /usr/bin/env python

from flask import Flask, redirect, url_for

from database import db

app = Flask(__name__)
app.config.from_object("settings.DevelopmentConfig")
db.init_app(app)

from blueprints.experiment import bpExperiment
app.register_blueprint(bpExperiment, url_prefix="/experiment")

from blueprints.node import bpNode
app.register_blueprint(bpNode, url_prefix="/node")

from blueprints.command import bpCommand
app.register_blueprint(bpCommand, url_prefix="/command")

from blueprints.nodeapi import bpNodeAPI
app.register_blueprint(bpNodeAPI, url_prefix="/api")

@app.route("/")
def index():
    return redirect(url_for("experiment.list"))

if __name__ == "__main__":
    app.run()
