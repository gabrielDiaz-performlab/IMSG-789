import viz
import vizshape
import vizact
import math
import cv2
import numpy as np

# Enable full screen anti-aliasing FSAA to smooth edges
#viz.setMultiSample(4)
# Increase the field of view(fov) to 60 degrees from default 40 degress
#viz.fov(60)
# viz.go starts an empty world

viz.window.setPosition( 0, 0 ) 
#Set the application window's size 
#in coordinates. 
viz.window.setSize( 1024, 512 ) # Set the window size to match the exact resolution of image

viz.go()

viz.clearcolor(viz.SKYBLUE)

viz.MainView.getHeadLight().enable()

viz.MainView.setPosition([5.12,-2.56,-1]) # Set the camera center based on the image resolution, 
											# y is negative so that pixel cordinates match vizard coordinates

viz.phys.enable()

img = cv2.imread('LineImage.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

wallUpZ = vizshape.addPlane(
	size = [10.24,5.12],	# Set the image plane to match the exact resolution of image in metres
	axis = -vizshape.AXIS_Z,
	cullFace = False
)
wallUpZ.setPosition(5.12,-2.56,6.0)	# Set the imaple plane center based on the image resolution

pic = viz.addTexture('LineImage.jpg')
wallUpZ.texture(pic)

midX = 512 # Based on horizontal image size

def createPhysicalObjects():
	global midX
	minLineLength = 3
	maxLineGap = 0.5
	
	edge = cv2.Canny(gray,100,200)
	
	lines = cv2.HoughLinesP(edge,1,np.pi/180,100,minLineLength,maxLineGap)
	
	noOfLines = lines.size/4
	print noOfLines
	
	i = 0
	while(i < noOfLines):
		for x1,y1,x2,y2 in lines[i]:
			print x1,y1,x2,y2
			midX = (float(x1) + float(x2))/2
			midY = (float(y1) + float(y2))/2
			x = float(midX)/100
			y = -float(midY)/100
			angle = int(math.atan((y1-y2)/(x2-x1))*180/math.pi)
			#print angle
			box = vizshape.addBox(splitFaces=True)  
			box.setPosition(x,y,6.0)
			xDiff = math.fabs(x1-x2)
			yDiff = math.fabs(y1-y2)
			square = math.pow(xDiff,2) + math.pow(yDiff,2)
			boxSize = math.sqrt(square)/100
			box.setScale(boxSize,0.02,0.5)
			#box.enable(viz.SAMPLE_ALPHA_TO_COVERAGE)
			box.color(viz.SKYBLUE)
			box.collideBox()
			box.disable(viz.DYNAMICS)
			box.setEuler(0,0,angle)
		i+=2

def onKeyDown(key):
	if key == ' ':
		print 'Space Key Pressed'
		ball1 = viz.add('soccerball.ive') #Add an object.
		ball1.setPosition(1.0,-1,6.0)
		ballPhys1 = ball1.collideSphere(bounce=1.5)   # Define ball's physical properties
		ball1.applyForce([0.01,0,0],1)
		
	if key == 'c':
		print 'Calculating edges and creating physical objects'
		createPhysicalObjects()
		
viz.callback(viz.KEYDOWN_EVENT,onKeyDown)

view = viz.MainView

MOVE_SPEED = 5
TURN_SPEED = 60
def updateView():
	if viz.key.isDown('W'):
		view.move([0,0,MOVE_SPEED*viz.elapsed()],viz.BODY_ORI)
	elif viz.key.isDown('S'):
		view.move([0,0,-MOVE_SPEED*viz.elapsed()],viz.BODY_ORI)
	elif viz.key.isDown('D'):
		view.setEuler([TURN_SPEED*viz.elapsed(),0,0],viz.BODY_ORI,viz.REL_PARENT)
	elif viz.key.isDown('A'):
		view.setEuler([-TURN_SPEED*viz.elapsed(),0,0],viz.BODY_ORI,viz.REL_PARENT)

vizact.ontimer(0,updateView)

