'''

April 2016 
Aneesh Rangnekar, Anna Starynska, Arun K., Mahshad M., Sanketh Moudgalya, Rakshit Kothari
Gabriel Diaz 
Carlson Center for Imaging Science
Rochester Institute of Technology

'''

import viz

viz.res.addPath('resources')
sys.path.append('utils')

import oculus
from configobj import ConfigObj
from configobj import flatten_errors
from validate import Validator
import vizconnect
import platform
import os.path
import vizact
import vizshape

class Configuration():
	
	def __init__(self, expCfgName = ""):
		"""
		Opens and interprets both the system config (as defined by the <platform>.cfg file) and the experiment config
		(as defined by the file in expCfgName). Both configurations MUST conform the specs given in sysCfgSpec.ini and
		expCfgSpec.ini respectively. It also initializes the system as specified in the sysCfg.
		"""		
		self.__createSysCfg()
		
		for pathName in self.sysCfg['set_path']:
			viz.res.addPath(pathName)
		
			
		self.vizconnect = vizconnect.go( 'vizConnect/' + self.sysCfg['vizconfigFileName'])
		self.__postVizConnectSetup()
		
	def __postVizConnectSetup(self):
		''' 
		This is where one can run any system-specific code that vizconnect can't handle
		'''
		dispDict = vizconnect.getRawDisplayDict()
		
		self.clientWindow = dispDict['exp_display']
		self.riftWindow = dispDict['rift_display']
		
		if( self.sysCfg['use_wiimote']):
			# Create wiimote holder
			self.wiimote = 0
			self.__connectWiiMote()

		if self.sysCfg['use_phasespace']:
			
			from mocapInterface import phasespaceInterface			
			self.mocap = phasespaceInterface(self.sysCfg);
			self.linkObjectsUsingMocap()
			
			self.use_phasespace = True
		else:
			self.use_phasespace = False
		
		if self.sysCfg['use_hmd'] and self.sysCfg['hmd']['type'] == 'DK2':
			#self.__setupOculusMon()
			self.hmd = oculus.Rift()
			self.setupExperimenterDisplay()
			self.placeEyeNodes()
			
		viz.setOption("viz.glfinish", 1)
		viz.setOption("viz.dwm_composition", 0)
		
	def __createSysCfg(self):
		"""
		Set up the system config section (sysCfg)
		"""
		# Get machine name
		#sysCfgName = platform.node()+".cfg"
		sysCfgName = "sysConfig"+".cfg"
		
		if not(os.path.isfile(sysCfgName)):
			sysCfgName = "defaultSys.cfg"
			
		
		print "Loading system config file: " + sysCfgName
		
		# Parse system config file
		sysCfg = ConfigObj(sysCfgName, configspec='sysCfgSpec.ini', raise_errors = True)
		
		validator = Validator()
		sysCfgOK = sysCfg.validate(validator)
		
		if sysCfgOK == True:
			print "System config file parsed correctly"
		else:
			print 'System config file validation failed!'
			res = sysCfg.validate(validator, preserve_errors=True)
			for entry in flatten_errors(sysCfg, res):
			# each entry is a tuple
				section_list, key, error = entry
				if key is not None:
					section_list.append(key)
				else:
					section_list.append('[missing section]')
				section_string = ', '.join(section_list)
				if error == False:
					error = 'Missing value or section.'
				print section_string, ' = ', error
			sys.exit(1)
		self.sysCfg = sysCfg
	
	def setupExperimenterDisplay(self):

		viz.window.setFullscreenMonitor(self.sysCfg['experimenterDisplay'])
		viz.window.setFullscreen(1)
			
	def __connectWiiMote(self):
		
		wii = viz.add('wiimote.dle')#Add wiimote extension
		
		# Replace old wiimote
		if( self.wiimote ):
			print 'Wiimote removed.'
			self.wiimote.remove()
			
		self.wiimote = wii.addWiimote()# Connect to first available wiimote
		
		vizact.onexit(self.wiimote.remove) # Make sure it is disconnected on quit
		
		self.wiimote.led = wii.LED_1 | wii.LED_4 #Turn on leds to show connection
	
		
				
	def linkObjectsUsingMocap(self):
			
			self.headTracker = vizconnect.getRawTracker('head_tracker')
			self.mocap.start_thread()
			
			trackerDict = vizconnect.getTrackerDict()
			
			if( 'rift_tracker' in trackerDict.keys() ):
				
				self.UpdateViewAct = vizact.onupdate(viz.PRIORITY_LINKS, self.updateHeadTracker)
				
			else:
				print '*** Experiment:linkObjectsUsingMocap: Rift not enabled as a tracker'
				return
			
	def updateHeadTracker(self):
		"""
		A specailized per-frame function
		That updates an empty viznode with:
		- position info from mocap
		- orientation from rift
		
		"""

		riftOriTracker = vizconnect.getTracker('rift_tracker').getNode3d()			
		
		ori_xyz = riftOriTracker.getEuler()
		self.headTracker.setEuler( ori_xyz  )
		
		headRigidTracker = self.mocap.get_rigidTracker('hmd')	
		self.headTracker.setPosition( headRigidTracker.get_position() )	
		
	def resetHeadOrientation(self):

		vizconnect.getTracker('rift_tracker').resetHeading()
	
	def placeEyeNodes(self):
		'''
		For convenience, this places nodes at the cyclopean eye, left eye, and right eye.
		When linkjing things to the eyes, link them to the cyclopean, left, or right eye nodes
		e.g. viz.link(config.cycEyeNode,vizshape.addSphere(radius=0.05))
		'''
		
		IOD = self.hmd.getIPD() 
		print("IOD")
		print(IOD)
		
		self.cycEyeNode = vizshape.addSphere(0.015, color = viz.GREEN)
		self.cycEyeNode.setParent(self.headTracker)
		self.cycEyeNode.disable(viz.RENDERING)
		
		self.leftEyeNode = vizshape.addSphere(0.005, color = viz.BLUE)
		self.leftEyeNode.disable(viz.RENDERING)
		self.leftEyeNode.setParent(self.headTracker)
		self.leftEyeNode.setPosition(-IOD/2, 0, 0.0,viz.ABS_PARENT)
		
		self.rightEyeNode = vizshape.addSphere(0.005, color = viz.RED)
		self.rightEyeNode.disable(viz.RENDERING)
		self.rightEyeNode.setParent(self.headTracker)
		self.rightEyeNode.setPosition(IOD/2, 0, 0.0,viz.ABS_PARENT)

		
################################################################################
################################################################################
## Here is where the magic happens

def printEyePositions():
	'''
	Print eye positions in global coordinates
	'''
	
	print 'Left eye: ' + str(config.leftEyeNode.getPosition(viz.ABS_GLOBAL))
	print 'Right eye: ' + str(config.rightEyeNode.getPosition(viz.ABS_GLOBAL))
	print 'Cyclopean eye: ' + str(config.cycEyeNode.getPosition(viz.ABS_GLOBAL))
	
	
config = Configuration()

vizact.onkeydown('o', config.resetHeadOrientation)



if( config.sysCfg['use_phasespace'] ):
	vizact.onkeydown('s', config.mocap.saveRigid,'hmd')
	vizact.onkeydown('r', config.mocap.resetRigid,'hmd')
	print 'Using Phasespace'
else:
	viz.MainView.setPosition([0,1.6,0])
	print 'Using Vizard world view'

viz.go

###############################################################################
################################################################################
################start playing around from here  ################################

def showDuckToBothEyes():
	##  Here is an example of how to place something in front of the left eye, and to make it visible to ONLY the left eye
	binocularRivalDuck = viz.addChild('duck.cfg')
	binocularRivalDuck.setScale([0.25]*3)
	binocularRivalDuck.setParent(config.leftEyeNode)
	binocularRivalDuck.setPosition([0,-.3,2],viz.ABS_PARENT)
	binocularRivalDuck.setEuler([180,0,0])
	## do not write renderToEye(viz.RIGHT_EYE) function if you want to render to both eyes. If both eyes have to show, 
	## keep it as it is 
	
def showImageToOneEye():
	
	s = 1000
	focalLen = 0.00081566 * s
	planeWidth = 0.00126 * s
	planeHeight = 0.0022 * s
	camcenter_dX = (640-606.3966)*1.75*(10^-6) * s
	camcenter_dY = (360-310.6875)*1.75*(10^-6) * s

	br = vizshape.addPlane(
		size = [planeHeight,planeWidth],
		axis = vizshape.AXIS_Z,
		cullFace = False
	)
	
	pic = viz.addTexture('imcalib30_corr.jpg')
	br.texture(pic)
	
	br.setParent(config.rightEyeNode)
	br.setPosition([0,0,focalLen],viz.ABS_PARENT)
	
	br.setEuler([180,0,0])
	br.renderToEye(viz.RIGHT_EYE)


def showImageToBothEyes():
	
	video = viz.add('VideoCamera.dle')
	outP = video.getWebcamNames(available = False)
	print(outP)
	
	cam1 = video.addWebcam(id=0, size=(640,480))
	cam2 = video.addWebcam(id=1, size=(640,480))
	
	
	s = 3000
	focalLen = 0.00081566 * s
	planeWidth = 0.00126 * s
	planeHeight = 0.0022 * s
	camcenter_dX = (640-606.3966)*1.75*(10^-6) * s
	camcenter_dY = (360-310.6875)*1.75*(10^-6) * s

	pl_left = vizshape.addPlane(
		size = [planeHeight,planeWidth],
		axis = vizshape.AXIS_Z,
		cullFace = False
	)
	
	pl_right = vizshape.addPlane(
		size = [planeHeight,planeWidth],
		axis = vizshape.AXIS_Z,
		cullFace = False
	)
	
	pl_left.texture(cam1)
	
	pl_right.texture(cam2)
	
	pl_left.setParent(config.leftEyeNode)
	pl_left.setPosition([0,0,focalLen],viz.ABS_PARENT)	
	
	pl_right.setParent(config.rightEyeNode)
	pl_right.setPosition([0,0,focalLen],viz.ABS_PARENT)
	
	## Add code to update orientation with changes in head orientation
	headEuler_YPR = config.headTracker.getEuler()
	pl_left.setEuler([180+headEuler_YPR[0],0+headEuler_YPR[1],-90+headEuler_YPR[2]])
	pl_right.setEuler([180+headEuler_YPR[0],0+headEuler_YPR[1],-90+headEuler_YPR[2]])
	
	pl_left.renderToEye(viz.LEFT_EYE)
	pl_right.renderToEye(viz.RIGHT_EYE)
	

def showBoxOnEyes(tableIn):
	tableTracker = config.mocap.get_rigidTracker('table')#gets the table location and orientation from Phasespace
	loc_table = tableTracker.get_position() #this stores the location in a list for modifying
		 
	tableIn.setPosition(loc_table[0], loc_table[1]/2.0, loc_table[2])
	
	ori_table = tableTracker.get_euler()
	tableIn.setEuler(ori_table)
	
table = vizshape.addBox([0.460,0.66,0.60],splitFaces=False)

ball = viz.addChild('basketball.osgb')

balllink = viz.link(table,ball)
balllink.preTrans([0,0.5,0])
glow = viz.addChild('fire.osg')
glowlink = viz.link(ball,glow)

vizact.onupdate(viz.PRIORITY_LINKS,showBoxOnEyes,table)

piazza = viz.addChild('piazza.osgb')

#showImageToBothEyes()