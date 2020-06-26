from flask import Flask
from flask import render_template, send_from_directory
from data import ib_invoice_data

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return render_template("template.html", kwargs=ib_invoice_data)

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('', path)


if __name__ == '__main__':
    app.run(debug=True)
