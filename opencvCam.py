from PIL import Image
import cv2
import viz
import viztask
import vizshape
import math

#viz.fov(74.73,1.77)
viz.fov(106.1,0.89)

#cam = viz.MainView()
#cam.setPosition([0,1.8,0])
#viz.MainView.setPosition([0,0,0])
#Quad to display the image on vizard
#focalLen = 7 #meter
#planeWidth = 2*focalLen*math.tan(111.316*3.14/(2*180))
#planeHeight = 2*focalLen*math.tan(74.34*3.14/(2*180))
viz.MainView.setPosition([0,1.06,0])

s = 1000
focalLen = 449 * 1.75 * 10**-6 * s
planeHeight = 720 * 1.75 * 10**-6 * s
planeWidth = 1280 * 1.75 * 10**-6 * s

tex = viz.addBlankTexture([1,1])

pl_left = vizshape.addPlane(
		size = [planeWidth,planeHeight],
		axis = -vizshape.AXIS_Z,
		cullFace = False)

pl_left.setEuler([0,0,90])

#pl_left.setParent(viz.MainView)
#pl_left.setPosition([0,0,focalLen],viz.ABS_PARENT)

pl_left.setPosition ([0,1.06,focalLen])
#tex = viz.addTexture('imcalib30_corr.jpg')
pl_left.texture(tex)


def PIL_TO_VIZARD(image,texture):
	
	"""Copy the PIL image to the Vizard texture"""
	im = image.transpose(Image.FLIP_TOP_BOTTOM)
	texture.setImageData(im.convert('RGB').tobytes(),im.size)

def opencvMain():
	#capture_r = cv2.VideoCapture(0)
	capture_l = cv2.VideoCapture(1)	
	
	capture_l.set(3,1280)
	capture_l.set(4,720)
	capture_l.set(5,30)
	#capture = cv2.VideoCapture(1)#conect to a camera
	
	while True:
		ret, frame = capture_l.read() #Image from camera in BGR format
		#dst = cv.CreateImage(cv.GetSize(src),cv.IPL_DEPTH_8U,3)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converting BGR to RGB
		
		#Converting opencv image to PIL image
		
		height, width, channels = frame.shape
		pil = Image.frombytes("RGB", [width,height], frame.tostring())
		
		#Aply image to texture
		PIL_TO_VIZARD(pil,tex)
		
		cv2.waitKey(10)
		yield viztask.waitTime(0)
		
	print "Image dimensions: ", frame.shape
		
viztask.schedule(opencvMain())

viz.go()