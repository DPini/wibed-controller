""" Testbed experiment-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for

from database import db
from models.experiment import Experiment
from models.node import Node

bpExperiment = Blueprint("experiment", __name__, \
        template_folder="../templates")

@bpExperiment.route("/")
def index():
    return redirect(url_for(".list"))

@bpExperiment.route("/list")
def list():
    runningExperiments = Experiment.query.filter(\
            Experiment.status != Experiment.Status.FINISHED).all()
    finishedExperiments = Experiment.query.filter(\
            Experiment.status == Experiment.Status.FINISHED).all()
    return render_template("experiment/list.html", \
            runningExperiments=runningExperiments, \
            finishedExperiments=finishedExperiments)

@bpExperiment.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        query = Node.query.filter(Node.available == True)
        print(query)
        nodes = query.all()
        return render_template("experiment/add.html", freeNodes=nodes)
    elif request.method == "POST":
        name = request.form["name"]
        overlay = request.form["overlay"]
        nodes = Node.query.filter(Node.id.in_(request.form.getlist("nodeIds"))).all()
        try:
            experiment = Experiment(name, overlay, nodes)
            db.session.add(experiment)
            db.session.commit()
            flash("Experiment '%s' added successfully" % name)
            return redirect(url_for(".show", id=experiment.id))
        except Exception as e:
            db.session.rollback()
            flash("Failed to add experiment: %s" % str(e))
            return redirect(url_for(".add"))

@bpExperiment.route("/remove/<id>")
def remove(id):
    experiment = Experiment.query.get_or_404(id)
    db.session.delete(experiment)
    db.session.commit()
    return redirect(url_for(".list"))

@bpExperiment.route("/start/<id>")
def start(id):
    experiment = Experiment.query.get_or_404(id)
    try:
        experiment.start()
    except Exception as e:
        flash("Failed to start experiment: %s" % str(e))
    return redirect(url_for(".show", id=id))

@bpExperiment.route("/finish/<id>")
def finish(id):
    experiment = Experiment.query.get_or_404(id)
    experiment.finish()
    return redirect(url_for(".show", id=id))

@bpExperiment.route("/show/<id>")
def show(id):
    experiment = Experiment.query.get_or_404(id)
    nodes = experiment.nodes.all()
    commands = experiment.commands.all()

    return render_template("experiment/show.html", experiment=experiment,\
            nodes=nodes, commands=commands, Experiment=Experiment)
