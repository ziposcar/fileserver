@echo off
call env\Scripts\activate
set FLASK_APP=fileserver.py
set FLASK_ENV=development
call flask run