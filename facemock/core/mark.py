import numpy as np
import cv2

def mark_mouse(filename, rect):
    # rect = {'height': 44.0, 'width': 548.0, 'x': 313.0, 'y': 228.0}
    img=cv2.imread(filename)
    print("img origin size: {}".format(img.size))
    img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_CUBIC)
    pos = int(rect.get("x")), int(rect.get("y"))
    dia = int(rect.get("x") + rect.get("width")), int(rect.get("y") + rect.get("height"))
    cv2.rectangle(img, pos, dia,(20,0,250),1)
    #cv2.line(img,(200,0),(111,511),(255,255,2),5)
    cv2.imwrite(filename, img)

if __name__ == '__main__':
    rect = {'height': 44.0, 'width': 548.0, 'x': 313.0, 'y': 228.0}
    mark_mouse('./meta/click_at_1593168167.262957_.png', rect)
