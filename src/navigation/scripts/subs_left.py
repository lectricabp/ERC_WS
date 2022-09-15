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

def euler_from_quaternion(x, y, z, w):
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = 2.0 * (w * y - z * x)
    t2 = 1.0 if t2 > 1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = 2.0*( w* z + x * y)
    t4 = 1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return (roll_x, pitch_y, yaw_z)

def listener():
    rospy.init_node('cam_pos_left', anonymous = False)
    rospy.Subscriber("/camera/left/image_raw",Image, callback)
    

    rospy.spin()
    cv2.destroyAllWindows()
    

def callback(data):
    cv_image = bridge.imgmsg_to_cv2(data)
    pose_estimation(cv_image)
    
def pose_estimation(frame):

    pub = rospy.Publisher('/left/pos_webCam',Position, queue_size=100)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = AR_landmark()
    parameters = cv2.aruco.DetectorParameters_create()
    parameters.markerBorderBits = 2
    parameters.errorCorrectionRate = 0.2
    matrix_coefficients = np.load("/home/upcspjetson/Desktop/ERC_WS/src/navigation/scripts/calibration_matrix.npy")
    distortion_coefficients = np.load("/home/upcspjetson/Desktop/ERC_WS/src/navigation/scripts/distortion_coefficients.npy")

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)
  
        # If markers are detected
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.09, matrix_coefficients,
                                                                       distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners) 
            
            pose = pose_comp(rvec[0][0], tvec[0][0], ids[i])


            pos_cam = Position()
            pos_cam.x = pose.pose.position.x
            pos_cam.z = pose.pose.position.z
            pos_cam.id = ids[i][0] + 1
            
            roll_x, pitch_y, yaw_z = euler_from_quaternion(pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z, pose.pose.orientation.w)
            pos_cam.angle = yaw_z

            pub.publish(pos_cam)

            # Draw Axis
            cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  

    '''
    cv2.imshow("", frame)
    cv2.waitKey(1)
    '''
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
