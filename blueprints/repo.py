from flask import Blueprint
from flask.ext.autoindex import AutoIndexBlueprint

bpRepo = Blueprint("bpRepo",__name__)
AutoIndexBlueprint(bpRepo, browse_root='/home/wibed/wibed-openwrt/bin/')
