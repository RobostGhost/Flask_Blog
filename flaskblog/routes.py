from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
# render_template used to render an html file instead of inline html
# url_for for easy refrencing, vs specifing specific file location

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_to_register = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user_to_register)
        db.session.commit()

        flash(f'Account Created! You can now login.', 'success')
        return redirect(url_for('login'))

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
