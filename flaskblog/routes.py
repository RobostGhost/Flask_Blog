import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm, 
                            RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
# render_template used to render an html file instead of inline html
# url_for for easy refrencing, vs specifing specific file location


# Can have multiple routes for one function
@app.route("/")
@app.route("/home")
def home():
    # if nothing in url, simply use first page, type pervents weird args from being read
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


