from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user is None:
            flash('Failed to Login! Email is not registered.', 'danger')
            return redirect(url_for('login'))

        if bcrypt.check_password_hash(existing_user.password, form.password.data):
            login_user(existing_user, remember=form.remember.data)
            flash(f'Welcome back {existing_user.username}!', 'success')

            # if the next param exists in url, go to that page instead
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Failed to Login! Incorrect password.', 'danger')

        return redirect(url_for('login'))
            
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)
