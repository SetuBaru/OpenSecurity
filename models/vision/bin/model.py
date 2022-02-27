import cv2
import user_management as manage

# reference webcam [0] (the default cam).
video_capture = cv2.VideoCapture(0)

# Load sample pictures and learn how to recognize them.
manage = manage.ManagementConsole()
