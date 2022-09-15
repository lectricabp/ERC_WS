#!/usr/bin/env python3

import  rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=3820,
    capture_height=2464,
    display_width=960,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

cap = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0, flip_method= 2), cv2.CAP_GSTREAMER)
print(cap.isOpened())
bridge = CvBridge()

def talker():
    pub = rospy.Publisher('/piCam/left/image_raw', Image, queue_size = 1)
    rospy.init_node('image_piCam_left', anonymous = False)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            break

        msg = bridge.cv2_to_imgmsg(frame, "bgr8")
        pub.publish(msg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if rospy.is_shutdown():
            cap.release()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
