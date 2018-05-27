import os
import urlparse
from json import dumps

from flask import Blueprint, jsonify, redirect, request

from app.service.HTTPServer import translate_path
from config import current_config

main = Blueprint('main', __name__, static_folder=current_config['static_folder'])


@main.route('/<path:path>')
def index(path):
    path = translate_path(path)
    if os.path.isdir(path):
        parts = urlparse.urlsplit(request.path)
        if not parts.path.endswith('/'):
            new_parts = (parts[0], parts[1], parts[2] + '/',
                         parts[3], parts[4])
            new_url = urlparse.urlunsplit(new_parts)
            return redirect(new_url)
        for index in "index.html", "index.htm":
            index = os.path.join(path, index)
            if os.path.exists(index):
                path = index
                break
        else:
            return list_directory(path)
    return jsonify([path])
    # return jsonify([dir(request), request.url])
