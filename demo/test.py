import sys

sys.path.append("..")

from facemock import Facemock
app = Facemock()

app.dash_server()
