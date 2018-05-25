import os
from json import dumps

from flask import Blueprint, jsonify, request

from config import current_config
from app.service.HTTPServer import translate_path

main = Blueprint('main', __name__, static_folder=current_config['static_folder'])


@main.route('/<path:path>')
def index(path):
    path = translate_path(path)

    return jsonify([path])
    # return jsonify([dir(request), request.url])
