from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/a")
def index():
    return render_template("index.html")

@app.route("/svg")
def svg():
    return render_template("svg.html")


if __name__ == '__main__':
    app.run(debug=True)
