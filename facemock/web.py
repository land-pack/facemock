from flask import Flask, send_from_directory
#
#
# app = Flask(__name__)
#
# @app.route("/")
# def index():
#     return "Test Dashborad"
#
#
# @app.route('/assets/<path:filename>')
# def send_file(filename):
#       return send_from_directory('/Users/frank/code/selenium-dev/facemock2/demo/assets', filename)
#!/bin/python

import os
from flask import Flask, Response, request, abort, render_template_string, send_from_directory
from PIL import Image
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3

app = Flask(__name__)
p = os.getcwd() + '/assets'

WIDTH = 1000
HEIGHT = 800

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facemock Test Dash</title>
    <meta charset="utf-8" />
    <style>
body {
    margin: 0;
    background-color: #333;
}
.image {
    display: block;
    margin: 2em auto;
    background-color: #444;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}
img {
    display: block;
}
    </style>
<script src="{{ url_for('static', filename='dialog.js')}}" charset="utf-8"></script>
<script src="{{ url_for('static', filename='boostrap.js')}}" charset="utf-8"></script>
<script src="{{ url_for('static', filename='jquery.js')}}" charset="utf-8"></script>
    <script src="{{ url_for('static', filename='unveil.js')}}" charset="utf-8"></script>
    <script>
$(document).ready(function() {
    $('img').unveil(1000);
});
    </script>
</head>
<body>
    <h1> Test Case One </h1>
    <br>
    {% for image in images %}
        <h2> Test Case One </h2>
        <br>
        <a class="image" href="{{ image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
            <img src="{{image.src}}" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" width="{{ image.width }}" height="{{ image.height }}" />
        </a>
    {% endfor %}
</body>
'''

@app.route('/Users/frank/code/selenium-dev/facemock2/demo/assets/<path:filename>')
def image(filename):
    # print("filename 2->", filename.split("assets")[1])
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory(p, filename)

    try:
        filename2 = p + filename
        im = Image.open(filename2)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory(p, filename)

@app.route('/')
def index():
    images = []
    for root, dirs, files in os.walk(p):
        print("do ..", root, dirs, files)
        for filename in [os.path.join(root, name) for name in files]:
        # for filename in
            if not filename.endswith('.png'):
                continue

            # filename = filename.split('/assets')[1]
            print("filename -->,", filename)
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })

    return render_template_string(TEMPLATE, **{
        'images': images
    })

if __name__ == '__main__':
    app.run(debug=True, host='::')

# if __name__ == '__main__':
#     app.run(debug=True)
