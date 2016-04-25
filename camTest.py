import viz

video = viz.add('VideoCamera.dle')

cam_r = video.addWebcam()

cam_l= video.addWebcam()

quad = viz.addTexQuad(pos = (0,1.8,1), texture = cam_l)
quad.setEuler([0,0,-90])

#quad1 = viz.addTexQuad(pos = (-5,1.8,1), texture = cam_l)
#fr = cam.getData()
#fr = cam.getFrameRate()
#print(fr)
viz.go()

