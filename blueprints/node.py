""" Testbed node-related functionality. """

from flask import Blueprint
from flask import request, render_template, flash, redirect, \
                  url_for, session

from database import db
from models.node import Node
from models.execution import Execution

from restrictions import get_nodes

bpNode = Blueprint("node", __name__, template_folder="../templates")

@bpNode.route("/")
def index():
    return redirect(url_for(".list"))

@bpNode.route("/list")
def list():
    return render_template("node/list.html", nodes=get_nodes(None))

@bpNode.route("/add", methods = ["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("node/add.html")
    elif request.method == "POST":
        id = request.form["id"]
        node = Node(id)
        db.session.add(node)
        db.session.commit()
        flash("Node '%s' added successfully" % node.id)
        return redirect(url_for(".show", id=node.id))

@bpNode.route("/remove/<id>")
def remove(id):
    node = Node.query.get_or_404(id)
    Execution.query.filter_by(nodeId = id).delete()
    db.session.delete(node)
    db.session.commit()
    return redirect(url_for(".list"))

@bpNode.route("/show/<id>")
def show(id):
    node = Node.query.get_or_404(id)
    return render_template("node/show.html", node=node)

@bpNode.route("/hide/<id>")
def hide(id):
    node = Node.query.get_or_404(id)
    if node.show:
	    node.show = False
	    db.session.commit()
    return render_template("node/show.html", node=node)

@bpNode.route("/unhide/<id>")
def unhide(id):
    node = Node.query.get_or_404(id)
    if not node.show:
	    node.show = True
	    db.session.commit()
    return render_template("node/show.html", node=node)
