
from flask import Flask, render_template, url_for, flash, redirect
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