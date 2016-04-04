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

viz.MainView.getHeadLight().enable()

cam = viz.MainView
cam.setPosition([0,1.06,0])

##
s = 1
focalLen = 0.00081566 * s
planeWidth = 0.00126 * s
planeHeight = 0.0022 * s
camcenter_dX = (640-606.3966)*1.75*(10^-6) * s
camcenter_dY = (360-310.6875)*1.75*(10^-6) * s

ImagePlane = vizshape.addPlane(
	size = [planeWidth,planeHeight],
	axis = -vizshape.AXIS_Z,
	cullFace = False
)

ImagePlane.enable(viz.BLEND)
ImagePlane.alpha(0.5)

link = viz.link(cam,ImagePlane)
link.preTrans([0,0,focalLen])

# Load texture 

video = viz.add('VideoCamera.dle')
cam_r = video.addWebcam()

pic = viz.addTexture('imcalib30_corr.jpg')
ImagePlane.texture(cam_r)


checkerBoard = vizshape.addPlane(
	color = viz.GRAY,
	size = [0.533,0.497],
	axis = vizshape.AXIS_Z,
	cullFace = False
)
#checkerBoard.setPosition(0,1.06,0.4191)

'''
Turn on the physics engine
viz.phys.enable()
'''