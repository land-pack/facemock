import numpy as np 
import cv2

def mark_mouse(filename, position):
	img=cv2.imread(filename)
	print("img origin size: {}".format(img.size))
	img = cv2.resize(img, (800, 800), interpolation=cv2.INTER_CUBIC)
	
	cv2.rectangle(img, pos, (pos[0] + 20, pos[1] + 30),(0,255,0),3)
	#cv2.line(img,(200,0),(111,511),(255,255,2),5)
	cv2.imwrite(filename, img)


if __name__ == '__main__':
	pos = (80, 20)
	mark_mouse('./sx.png', pos)
