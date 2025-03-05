"""Used for editor/editor's preview"""

import base64
from flask import Blueprint, request, render_template

editor_routes = Blueprint('simple_page', __name__, template_folder='templates')

@editor_routes.route("/editor")
def editor():
    return render_template("editor/editor.html")

@editor_routes.route("/preview/<b64>")
@editor_routes.route("/preview/")
def preview(b64:str=""):
    """Return a preview to show in the editor"""
    is_real_preview = request.args.get("website", False, type=bool)
    content = base64.b64decode(b64).decode("utf-8")
    if is_real_preview:
        return render_template("editor/demo.html", written=content)

    return render_template("editor/preview.html", content=content)
