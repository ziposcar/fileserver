from flask import Flask
from flask_script import Manager

app = Flask(__name__, static_folder='E:\\specials\\moive\\baseball')
from app import views

if __name__ == "__main__":
    app.run()
