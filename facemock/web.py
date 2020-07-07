from flask import Flask, send_from_directory
from flask import render_template, request

import redis
r = redis.Redis(host='localhost', port=6379, db=0)


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

'''

@app.route("/result")
def result():
    return render_template("result.html")

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

    return render_template('index.html', **{
        'images': images})

@app.route('/handle_data', methods=['POST'])
def handle_data():
    # part_id = xxx.form['part_id']
    xpath = request.form['xpath']
    print("xpath -->", xpath)
    # p = r.pubsub()
    # p.psubscribe('#update_xpath', xpath)
    r.publish("#update_xpath", xpath)
    return "ok"





if __name__ == '__main__':
    app.run(debug=True, host='::')

# if __name__ == '__main__':
#     app.run(debug=True)
