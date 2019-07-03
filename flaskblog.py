
from flask import Flask, render_template
# Flask used to create app
# render_template used to render an html file instead of inline html

app = Flask(__name__)

# Can have multiple routes for one function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


# Makes sure app runs in debug
if __name__ == '__main__':
    app.run(debug = True)