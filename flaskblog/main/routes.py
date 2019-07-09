from flask import Blueprint


main = Blueprint('main', __name__)


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
