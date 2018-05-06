from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("auth.html")

@app.route('/register')
def register():
    return render_template("reg.html")

@app.route('/dash')
def dash():
    return render_template("dash.html")

# add any other routes here!!!!

if __name__ == "__main__":
    app.run(debug=True)
