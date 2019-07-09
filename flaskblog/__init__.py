#  Package structure, where app will initialize
import os
from flask import Flask # creates the app
from flask_sqlalchemy import SQLAlchemy # create db
from flask_bcrypt import Bcrypt # for hashing
from flask_login import LoginManager # manages login sessions
from flask_mail import Mail # for sending mail


app = Flask(__name__)


# used for protection (ex: cookie modification), token generated using secrets.token_hex()
app.config['SECRET_KEY'] = '7fec327b7e1da6f8b90966f78d7372d1'
# /// indicates relative path, where the sb will be stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# setup the db
db = SQLAlchemy(app)
# setup for password hasher
bcrypt = Bcrypt(app)
# setup login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login' # refers to our login page route func
login_manager.login_message_category = 'info'
# setup mail server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
# Using user set environmental vars to ensure info not in code
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
mail = Mail(app)


# initialize routes using Blueprints
from flaskblog.users.routes import main
from flaskblog.users.routes import users
from flaskblog.users.routes import posts

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)