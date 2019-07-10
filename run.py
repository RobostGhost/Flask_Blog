from flaskblog import create_app

app = create_app()

# Makes sure app runs in debug
if __name__ == '__main__':
    app.run(debug=True)
