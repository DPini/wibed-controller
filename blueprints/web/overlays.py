from flask import Blueprint
from flask.ext.autoindex import AutoIndexBlueprint

bpOverlays = Blueprint("web.overlays",__name__, template_folder="../../templates")
idx=AutoIndexBlueprint(bpOverlays, browse_root='/opt/wibed-controller/static/overlays/', add_url_rules=False)


@bpOverlays.route('/',defaults={'path': ''})
@bpOverlays.route('/<path:path>')
def autoindex(path="."):
	return idx.render_autoindex(path, template="autoindex.html")
