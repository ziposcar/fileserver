#!/bin/sh
. ./env/bin/activate
export FLASK_APP=fileserver.py
export FLASK_ENV=development
flask run
