import sys

sys.path.append("..")

from facemock import Facemock
app = Facemock()


psswd = 'testKLOOK123!'


# app.load_case(max_workers=2)
# app.exec_case(max_workers=5)

app.update_step('test step')

if __name__ == '__main__':
    # app.run()
    app.update_step('test step')
