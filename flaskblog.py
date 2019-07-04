
from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
# Flask used to create app
# render_template used to render an html file instead of inline html
# url_for for easy refrencing, vs specifing specific file location
# SQLAlchemy for database


app = Flask(__name__)


# used for protection (ex: cookie modification)
# token generated using secrets.token_hex()
app.config['SECRET_KEY'] = '7fec327b7e1da6f8b90966f78d7372d1'
# /// indicates relative path, where the sb will be stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Getting the db
db = SQLAlchemy(app)

# db Models
class User(db.Model):
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # hash of password

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# python dictionary representing post data
posts = [
    {
        'author' :  'Mark Rob',
        'title' :  'First Blog Post',
        'content' :  'Hello World',
        'date_posted' :  'July 3, 2019',
    },
    {
        'author' :  'Apple Orange',
        'title' :  'I am happy',
        'content' :  'The title says it all',
        'date_posted' :  'July 2, 2019',
    }
]


# Can have multiple routes for one function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Accont created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # temp fake accepted data to test form
    fake_accepted_email = 'admin@blog.com'
    fake_accepted_password = 'password123'

    if form.validate_on_submit():
        if form.email.data == fake_accepted_email and form.password.data == fake_accepted_password:
            flash('You are logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Failed to Login! Please try again.', 'danger')
            return redirect(url_for('home'))
            
    return render_template('login.html', title='Login', form=form)


# Makes sure app runs in debug
if __name__ == '__main__':
    app.run(debug = True)