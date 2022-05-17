from hunter import create_app
from flask_script import Manager


app = create_app()
manager = Manager(app)


if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'any secret string'
    manager.run()
