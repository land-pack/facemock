import sys

sys.path.append("..")

from facemock import Facemock
app = Facemock()

app.load_case(max_workers=2)
app.exec_case(max_workers=5)


if __name__ == '__main__':
    app.run()
