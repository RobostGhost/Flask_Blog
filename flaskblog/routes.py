import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
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


def save_picture(form_picture):
    random_hex_for_pic_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_f_name = random_hex_for_pic_name + f_ext

    # app.root_path gives us the path to our app
    picture_path = os.path.join(app.root_path, 'static/profile_pics/', picture_f_name)
    form_picture.save(picture_path)

    return picture_f_name

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # profile pic update
        if form.picture.data:
            picture_f_name = save_picture(form.picture.data)
            current_user.image_file = picture_f_name

        # user info is updated
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() # remember to actually save the changes to the db
        flash('Account Updated!', 'success')
        return redirect(url_for('account')) # ensures a GET once return to page
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
