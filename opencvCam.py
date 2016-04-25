from PIL import Image
import cv2
import viz
import viztask

#Quad to display the image on vizard
tex = viz.addBlankTexture([1,1])
quad = viz.addTexQuad(pos=(0,1.8,2),texture = tex)
quad.setEuler([0,0,90])
'''
pl = vizshape.addPlane(
		size = [planeHeight,planeWidth],
		axis = vizshape.AXIS_Z,
		cullFace = False
	)
'''
def PIL_TO_VIZARD(image,texture):
	
	"""Copy the PIL image to the Vizard texture"""
	im = image.transpose(Image.FLIP_TOP_BOTTOM)
	texture.setImageData(im.convert('RGB').tobytes(),im.size)

def opencvMain():
	capture_r = cv2.VideoCapture(0)
	capture_l = cv2.VideoCapture(1)	
	#capture = cv2.VideoCapture(1)#conect to a camera
	
	while True:
		ret, frame = capture.read() #Image from camera in BGR format
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