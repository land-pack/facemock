import sys

sys.path.append("..")

from facemock import Facemock
app = Facemock()

app.load_case()



if __name__ == '__main__':
    app.run()
