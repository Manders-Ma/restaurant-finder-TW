from flask import Flask
from hunter.route import index, park


def create_app():
    app = Flask(__name__, template_folder='template')
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/park', 'park', park, methods=['GET', 'POST'])
    return app
