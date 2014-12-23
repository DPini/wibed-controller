from flask import Blueprint
from flask.ext.autoindex import AutoIndexBlueprint

bpRepo = Blueprint("web.repo",__name__,template_folder="../../templates")
idx=AutoIndexBlueprint(bpRepo, browse_root='/home/wibed/public/', add_url_rules=False)

@bpRepo.route('/',defaults={'path': ''})
@bpRepo.route('/<path:path>')
def autoindex(path="."):
        return idx.render_autoindex(path, template="autoindex.html")
