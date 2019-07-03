
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
# Flask used to create app
# render_template used to render an html file instead of inline html
# url_for for easy refrencing, vs specifing specific file location

app = Flask(__name__)

# used for protection (ex: cookie modification)
# token generated using secrets.token_hex()
app.config['SECRET_KEY'] = '7fec327b7e1da6f8b90966f78d7372d1'

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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


# Makes sure app runs in debug
if __name__ == '__main__':
    app.run(debug = True)