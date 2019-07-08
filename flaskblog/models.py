from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin # adds the necessary attributes/functions for our user model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #is the primary key of the db model
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # will use hash for image
    password = db.Column(db.String(60), nullable=False) # hash of password
    # One to Many relationship from User to Post
    posts = db.relationship('Post', backref='author', lazy=True) # backref adds author attribute to Post

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # date time function is passed, not run
    content = db.Column(db.Text, nullable=False)
    # foreign key to user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
