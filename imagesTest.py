from api import ps_drone
import time
import opencv

def mostrarImgF():
		img = drone.VideoImage
		img = cv2.resize(img, (320,640))
		cv2.imshow('Foto tomada por el drone', img)
		drone.hover()
		cv2.waitKey(1)
		cv2.destroyAllWindows()
