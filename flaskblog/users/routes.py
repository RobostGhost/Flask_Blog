from flask import Blueprint

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
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


@users.route("/login", methods=['GET', 'POST'])
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


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # TODO maybe add profile pic clean up
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
        # Pre-fill user information
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page=5, page=page)
    return render_template("user_posts.html", posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()       
        send_reset_email(user) 
        flash('Email has been sent for instructions on how to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('Token invalid or has expired!', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_new_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_new_password
        db.session.commit()

        flash(f'Password has been reset to the new password!', 'success')
        return redirect(url_for('login'))
    
    return render_template("reset_token.html", title='Reset Password', form=form)
