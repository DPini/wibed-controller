from flask import Blueprint
from flask.ext.autoindex import AutoIndexBlueprint

bpDirRes = Blueprint("bpDirRes",__name__)
AutoIndexBlueprint(bpDirRes, browse_root='/opt/wibed-controller/static/results/')
