from flask import Flask, render_template, request


def init_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_pyfile('config.py')
    
    with app.app_context():
        import routes

        return app