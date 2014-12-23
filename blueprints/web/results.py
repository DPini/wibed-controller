from flask import Blueprint
from flask.ext.autoindex import AutoIndexBlueprint

bpResults = Blueprint("web.results",__name__, template_folder="../../templates")
idx=AutoIndexBlueprint(bpResults, browse_root='/opt/wibed-controller/static/results/', add_url_rules=False)


@bpResults.route('/',defaults={'path': ''})
@bpResults.route('/<path:path>')
def autoindex(path="."):
	return idx.render_autoindex(path, template="autoindex.html")
