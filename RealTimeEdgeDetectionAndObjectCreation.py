import viz
import vizshape
import vizact
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
viz.window.setSize( 1024, 512 )

viz.go()

viz.clearcolor(viz.SKYBLUE)

viz.MainView.getHeadLight().enable()

viz.MainView.setPosition([5.12,-2.56,-1])

viz.phys.enable()

img = cv2.imread('LineImage.jpg',0)
edge = cv2.Canny(img,100,200)

img = cv2.imread('BoxImage.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

ans = []
for y in range(0, edge.shape[0]):
    for x in range(0, edge.shape[1]):
        if edge[y, x] != 0:
            ans = ans + [[x, y]]
ans = np.array(ans)
size = ans.shape[0]-1

midX = (ans[0][0] + ans[size][0])/2
midY = (ans[0][1] + ans[size][1])/2
x = float(midX)/100
y = -float(midY)/100

box = vizshape.addBox(splitFaces=True)  
box.setPosition(x,y,6.0)
boxSize = (float(midX - ans[0][0])/100)*2
box.setScale(boxSize,0.02,0.5)
box.collideBox()
box.disable(viz.DYNAMICS)
box.enable(viz.SAMPLE_ALPHA_TO_COVERAGE)

wallUpZ = vizshape.addPlane(
	size = [10.24,5.12],
	axis = -vizshape.AXIS_Z,
	cullFace = False
)
wallUpZ.setPosition(5.12,-2.56,6.0)

pic = viz.addTexture('LineImage.jpg')
wallUpZ.texture(pic)

def onKeyDown(key):
	if key == ' ':
		print 'Space Key Pressed'
		ball1 = viz.add('soccerball.ive') #Add an object.
		ball1.setPosition(float(midX)/100,-1,6.0)
		ballPhys1 = ball1.collideSphere(bounce=1.5)   # Define ball's physical properties
		
viz.callback(viz.KEYDOWN_EVENT,onKeyDown)

