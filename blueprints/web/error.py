from flask import Blueprint, current_app as app
from flask.ext.autoindex import AutoIndexBlueprint

bpError = Blueprint("web.error",__name__, template_folder="../../templates")
idx=AutoIndexBlueprint(bpError, browse_root="/opt/wibed-controller/static/error/", add_url_rules=False)


@bpError.route('/',defaults={'path': ''})
@bpError.route('/<path:path>')
def autoindex(path="."):
	return idx.render_autoindex(path, template="autoindex.html")
