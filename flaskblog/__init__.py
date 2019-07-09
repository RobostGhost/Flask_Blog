#  Package structure, where app will initialize
from flask import Flask # creates the app
from flask_sqlalchemy import SQLAlchemy # create db
from flask_bcrypt import Bcrypt # for hashing
from flask_login import LoginManager # manages login sessions
from flask_mail import Mail # for sending mail
from flaskblog.config import Config


app = Flask(__name__)
app.config.from_object(Config)


# setup the db
db = SQLAlchemy(app)
# setup for password hasher
bcrypt = Bcrypt(app)
# setup login manager
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' # refers to our login page route func
login_manager.login_message_category = 'info'

mail = Mail(app)


# initialize routes using Blueprints
from flaskblog.main.routes import main
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)