# Used to gain access to the entire Vizard library
import viz
import vizshape
import vizact

# Enable full screen anti-aliasing FSAA to smooth edges
viz.setMultiSample(4)
# Increase the field of view(fov) to 60 degrees from default 40 degress
viz.fov(74.73,1.77)
# viz.go starts an empty world
viz.go()

viz.clearcolor(viz.SKYBLUE) #Setting the background color

# Set room dimensions.
# Make it a rectangle, not a square, or it will be too easy to accidentally switch width/height

roomWidthOnXAxis = 10
roomLengthOnZAxis = 20
roomHeightOnYAxis = 15

############################################################
### Use viz.addChild to import a model (ground.osgb)

'''
ground = viz.addChild('ground.osgb')
ground.collidePlane() # Make ground collide with objects as if it were an infinite plane
'''

############################################################
# Add world axes

'''
axes = vizshape.addAxes()
axes.setPosition(0,0,2)
'''

############################################################
### Add a spot light with viz.addSpotLight

viz.MainView.getHeadLight().enable()

#Move the view point so that everything is within the screen view
viz.MainView.setPosition([0,1.06,0])


'''
#Adding Light
myLight = viz.addLight()
myLight.enable()
myLight.position(0,2,0.8)
myLight.spread(180)
myLight.intensity(2)
'''

############################################################
### Add Image Plane!

ImagePlane = vizshape.addPlane(
	size = [0.00224,0.00126],
	axis = -vizshape.AXIS_Z,
	cullFace = False
)
ImagePlane.setPosition(-0.00005882,1.06 - 0.00008596,0.000814)
ImagePlane.enable(viz.BLEND)
ImagePlane.alpha(0.5)


# Load texture 
pic = viz.addTexture('imcalib30_corr.jpg')
ImagePlane.texture(pic)

checkerBoard = vizshape.addPlane(
	color = viz.GRAY,
	size = [0.533,0.497],
	axis = vizshape.AXIS_Z,
	cullFace = False
)
checkerBoard.setPosition(0,1.06,0.4191)

# checkerBoard.collideMesh()

# Adding Keyboard interactions
MOVE_SPEED = 5
TURN_SPEED = 60

view = viz.MainView

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

# view.setAxisAngle(1,0,0,30,viz.ABSOLUTE)

'''
Turn on the physics engine
viz.phys.enable()
'''