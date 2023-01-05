#!/usr/bin/env python3

import sys
import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import PoseStamped
import tf
from customDict import AR_landmark
from navigation.msg import Position
import math



bridge = CvBridge()

def listener():
    rospy.init_node('cam_pos_right', anonymous = False)
    rospy.Subscriber("ERC22_URDF/right_camera/image_raw",Image, callback)


    rospy.spin()
    cv2.destroyAllWindows()


def callback(data):
    cv_image = bridge.imgmsg_to_cv2(data)
    pose_estimation(cv_image)

def pose_estimation(frame):

    pub = rospy.Publisher('/right/pos_webCam',Position, queue_size=100)
    pub2 = rospy.Publisher('/right/ARTag_det', Image, queue_size = 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = AR_landmark()
    parameters = cv2.aruco.DetectorParameters_create()
    parameters.markerBorderBits = 2
    parameters.errorCorrectionRate = 0.2
    #matrix_coefficients = np.load("/home/lectric/Desktop/ERC22_WS/src/navigation/scripts/calibration_matrix.npy")

    matrix_coefficients = np.array([[1086, 0, 319.5],[0, 1091, 239.5],[0, 0, 1]], dtype=float)

    distortion_coefficients = np.load("/home/lectric/Desktop/ERC22_WS/src/navigation/scripts/distortion_coefficients.npy")

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)

        # If markers are detected
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.055, matrix_coefficients,
                                                                       distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners)

            pose = pose_comp(rvec[0][0], tvec[0][0], ids[i])

            pos_cam = Position()
            pos_cam.x = pose.pose.position.x
            pos_cam.z = pose.pose.position.z
            pos_cam.id = ids[i][0] + 1

            pub.publish(pos_cam)

            # Draw Axis
            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)

    msg = bridge.cv2_to_imgmsg(frame, "bgr8")
    pub2.publish(msg)
    return frame

def pose_comp(rvec, tvec, ids):

    # we need a homogeneous matrix but OpenCV only gives us a 3x3 rotation matrix
    rotation_matrix = np.array([[0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 1]],
                                dtype=float)
    rotation_matrix[:3, :3], _ = cv2.Rodrigues(rvec)

    # convert the matrix to a quaternion
    quaternion = tf.transformations.quaternion_from_matrix(rotation_matrix)

    # To visualize in rviz, you can, for example, publish a PoseStamped message:
    pose = PoseStamped()
    pose.header.frame_id = "camera_frame"
    pose.pose.position.x = tvec[0]
    pose.pose.position.y = tvec[1]
    pose.pose.position.z = tvec[2]

    pose.pose.orientation.x = quaternion[0]
    pose.pose.orientation.y = quaternion[1]
    pose.pose.orientation.z = quaternion[2]
    pose.pose.orientation.w = quaternion[3]
    return(pose)



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
