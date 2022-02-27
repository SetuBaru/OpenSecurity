from bin import pose_estimation as pose

vid_writing = pose.head_tracking(cam=0, _record=True, _filename='TestOutput', _format='avi', _dimensions=(640, 480))

print('Video Writing Complete')
