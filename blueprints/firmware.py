""" Admin-related functionality. """

import os
from dateutil import parser
from hashlib import md5

from flask import Blueprint
from flask import render_template, flash, redirect, request, \
                  url_for, current_app as app
from werkzeug import secure_filename

from database import db
from models.firmware import Firmware, Upgrade
from models.node import Node

import logging

bpFirmware = Blueprint("firmware", __name__, template_folder="../templates")

@bpFirmware.route("/")
def index():
    return redirect(url_for(".list"))

@bpFirmware.route("/list")
def list():
    installedFirmwares = Firmware.query.filter(Firmware.nodes.any())\
            .order_by(Firmware.id.desc()).all()
    otherFirmwares = Firmware.query.filter(~Firmware.nodes.any())\
            .order_by(Firmware.id.desc()).all()

    return render_template("firmware/list.html", 
        installedFirmwares=installedFirmwares,
        otherFirmwares=otherFirmwares)

@bpFirmware.route("/add", methods=["GET", "POST"])
def add():
    try:
        try:
            version = request.form["version"]

            if not version:
                raise Exception("Invalid version")
        except KeyError:
            raise Exception("Version not specified")

        firmwareFile = None

        try:
            firmwareFile = request.files["firmware"]
            firmwareFileName = secure_filename(version)
            firmwareHash = md5(firmwareFile.read()).hexdigest()
            firmwareFile.seek(0)
            firmwareFile.save(os.path.join(app.config["FIRMWARE_DIR"], 
                firmwareFileName))
        except KeyError:
            raise Exception("Invalid firmware uploaded")
        
        hashUploaded = None

        try:
	     hashUploaded = request.form['hash'].strip()
	     logging.debug("File hash: %s", firmwareHash)
	     logging.debug("Uploaded hash: %s", hashUploaded)
	     if firmwareHash != hashUploaded :
	     	flash("File has wrong hash")
		return redirect(url_for(".list"))
	except KeyError:
            raise Exception("Error validating checksum")

        firmware = Firmware(version, firmwareHash)
        db.session.add(firmware)
        db.session.commit()
        flash("Firmware '%s' added successfully" % version)
        return redirect(url_for(".list"))
    except Exception as e:
        db.session.rollback()
        flash("Failed to add firmware: %s" % str(e))
        return redirect(url_for(".list"))

@bpFirmware.route("/install/<id>", methods=["GET", "POST"])
def install(id):
    firmware = Firmware.query.get_or_404(id)
    if request.method == "GET":
        availableNodes = Node.query.filter(Node.firmwareId != id,
            Node.available == True).all()
        return render_template("firmware/install.html", firmware=firmware,
                availableNodes=availableNodes)
    elif request.method == "POST":
        try:
            try:
                upgradeTime = parser.parse(request.form['upgradeTime'])

            except ValueError:
                raise ValueError("Unable to parse upgrade time")
            except KeyError:
                raise Exception("Can't find upgrade time")

            try:
                nodes = Node.query.filter(Node.id.in_(request.form.getlist("nodeIds"))).all()

                if not nodes:
                    raise ValueError("Unable to parse selected nodes")
            except KeyError:
                raise Exception("Can't setup an installation with no nodes")

            upgrade = Upgrade(firmware.id, upgradeTime, nodes)
            db.session.add(upgrade)
            db.session.commit()
            flash("Firmware upgrade initiated successfully")
            return redirect(url_for(".show", id=id))
        except Exception as e:
            db.session.rollback()
            flash("Failed to start firmware upgrade: %s" % str(e))
            return redirect(url_for(".install", id=id))

@bpFirmware.route("/show/<id>")
def show(id):
    firmware = Firmware.query.get_or_404(id)
    nodesUpgraded = Node.query.filter(Node.firmwareId == id).all()
    nodesUpgrading = Node.query.join(Upgrade).filter(Upgrade.firmwareId == id).all()
    upgradeOrders = [o for o in firmware.upgradeOrders]

    return render_template("firmware/show.html", firmware=firmware,\
            upgradeOrders=upgradeOrders, nodesUpgraded=nodesUpgraded,
            nodesUpgrading=nodesUpgrading)
