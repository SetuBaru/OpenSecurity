from models import pose_estimation as pose

vid_writing = pose.head_tracking(cam=0, _record=True, _format='avi', _dimensions=(640, 480))

