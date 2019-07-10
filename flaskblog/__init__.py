#  Package structure, where app will initialize
from flask import Flask # creates the app
from flask_sqlalchemy import SQLAlchemy # create db
from flask_bcrypt import Bcrypt # for hashing
from flask_login import LoginManager # manages login sessions
from flask_mail import Mail # for sending mail
from flaskblog.config import Config


# setup the db
db = SQLAlchemy()
# setup for password hasher
bcrypt = Bcrypt()
# setup login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login' # refers to our login page route func
login_manager.login_message_category = 'info'

mail = Mail()

# Initialize the app wih a function instead
# Allowing multiple instances
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # initialize routes using Blueprints
    from flaskblog.main.routes import main
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app