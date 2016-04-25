from PIL import Image
import cv2
import viz
import viztask

viz.MainView.getHeadLight().enable()
m = 1280
n = 720
d = 449
s = 1.75*10**-6
scale = 1000
#Move the view point so that everything is within the screen view
viz.MainView.setPosition([0,0,-d*s*scale])

#Quad to display the image on vizard

iod = 0.064/2
tex_l = viz.addBlankTexture([m*s*scale,n*s*scale])
quad_l = viz.addTexQuad(pos=(-iod,0,d*s*scale),texture = tex_l)
#quad_l.enable(viz.BLEND)
#quad_l.alpha(0.8)
quad_l.setEuler([0,0,90])

tex_r = viz.addBlankTexture([m*s*scale,n*s*scale])
quad_r = viz.addTexQuad(pos=(iod,0,d*s*scale),texture = tex_r)
#quad_r.enable(viz.BLEND)
#quad_r.alpha(0.8)
quad_r.setEuler([0,0,90])
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
	
	while True:
		ret_r, frame_r = capture_r.read()
		ret_l, frame_l = capture_l.read()
		#dst = cv.CreateImage(cv.GetSize(src),cv.IPL_DEPTH_8U,3)
		frame_r = cv2.cvtColor(frame_r, cv2.COLOR_BGR2RGB)
		frame_l = cv2.cvtColor(frame_l, cv2.COLOR_BGR2RGB)		
		#Converting opencv image to PIL image
		
		height_r, width_r, channels_r = frame_r.shape
		height_l, width_l, channels_l = frame_l.shape
		pil_r = Image.frombytes("RGB", [width_r,height_r], frame_r.tostring())
		pil_l = Image.frombytes("RGB", [width_l,height_l], frame_l.tostring())
	
		PIL_TO_VIZARD(pil_r,tex_r)
		PIL_TO_VIZARD(pil_l,tex_l)
		
		cv2.waitKey(10)
		yield viztask.waitTime(0)
		
viztask.schedule(opencvMain())

viz.go()