#!/usr/bin/env python3

from cmath import pi
from re import M
from tkinter.tix import X_REGION
import rospy
import numpy as np
from navigation.msg import Position
import math
from std_msgs.msg import Float32

angle_b = 0

def land_pos():
    landmarks = [[0, 0, 0],
      [1, 10, 0],
      [2, 10, 10],
      [3, 28.35, 0.04],
      [4, 21.83, 2.80],
      [5, 18.72, 17,19],
      [6, 26.95, 7.94],
      [7, 15.97, -7.57],
      [8, 17.87, 7.57],
      [9, 10 , -10],
      [10, 29.26, 14.52],
      [11, 18.41, 25.83],
      [12, 23.34, 14.11],
      [13, 8.18, 18.63],
      [14, 0, 0],
      [15, 2.27, 16.84]]
    return landmarks

def cam_pos():
    cams = [[1, 0.23, 0.283], #up right
            [2, -0.225, 0.295], #up left
            [3, 0.25, -0.325],  #down right
            [4, -0,25, -0.325]] #down left
    return cams

def listener():
    rospy.init_node('pos_comp', anonymous = False)
    
    rospy.Subscriber("angle", Float32, callback_angle)

    rospy.Subscriber("/left/pos_webCam",Position, callback_up_left)
    rospy.Subscriber("/right/pos_webCam",Position, callback_up_right)
    rospy.Subscriber("/left/pos_piCam",Position, callback_down_left)
    rospy.Subscriber("/right/pos_piCam",Position, callback_down_right)
    rospy.spin()

def callback_angle(data):
    global angle_b
    angle_b = data.data *(pi / 180)

def callback_up_left(data):
    global angle_b
    x_land, y_land = find_coords(data.id)
    x_cam, y_cam = find_cam(2)
    angle = abs(math.atan2(x_cam, y_cam))

    x_rel = data.x* math.cos(angle) - data.z * math.sin(angle) + x_cam
    y_rel = data.x* math.sin(angle) + data.z * math.cos(angle) + y_cam
    x_aux = x_land + x_rel
    y_aux = y_land + y_rel
    x_g = x_aux * math.cos(angle_b) - y_aux * math.sin(angle_b) 
    y_g = x_aux * math.sin (angle_b) + y_aux * math.cos (angle_b)
    pos = Position()
    pos.id = 2
    pos.z = x_g
    pos.x = y_g
    pos.angle = angle_b
    pub = rospy.Publisher('pos',Position, queue_size=100)
    pub.publish(pos)

def callback_up_right(data):
    global angle_b
    x_land, y_land = find_coords(data.id)
    x_cam, y_cam = find_cam(1)
    angle = math.atan2(x_cam, y_cam)
    x_rel = data.x* math.cos(angle) + data.z * math.sin(angle) + x_cam
    y_rel = -data.x* math.sin(angle) + data.z * math.cos(angle) + y_cam
    x_aux = x_land - x_rel
    y_aux = y_land -y_rel
    x_g = x_aux * math.cos(angle_b) - y_aux * math.sin(angle_b) 
    y_g = x_aux * math.sin (angle_b) + y_aux * math.cos (angle_b)
    pos = Position()
    pos.id = 1
    pos.z = x_g
    pos.x = y_g
    pos.angle = angle_b
    pub = rospy.Publisher('pos',Position, queue_size=100)
    pub.publish(pos)

    
def callback_down_left(data):
    x_land, y_land = find_coords(data.id)
    x_cam, y_cam = find_cam(4)
    angle = math.atan2(x_cam, y_cam)* 180/(pi)
    x_rel = data.x* math.cos(angle) + data.z * math.sin(angle) + x_cam
    y_rel = -data.x* math.sin(angle) + data.z * math.cos(angle) + y_cam
    x_g = x_land + x_rel
    y_g = y_land + y_rel
    pos = Position()
    pos.id = 4
    pos.x = x_g
    pos.z = y_g
    pub = rospy.Publisher('pos',Position, queue_size=100)
    pub.publish(pos)


def callback_down_right(data):
    x_land, y_land = find_coords(data.id)
    x_cam, y_cam = find_cam(3)
    angle = math.atan2(x_cam, y_cam)* 180/(pi)
    x_rel = data.x* math.cos(angle) + data.z * math.sin(angle) + x_cam
    y_rel = -data.x* math.sin(angle) + data.z * math.cos(angle) + y_cam
    x_g = x_land + x_rel
    y_g = y_land + y_rel
    pos = Position()
    pos.id = 3
    pos.x = x_g
    pos.z = y_g
    pub = rospy.Publisher('pos',Position, queue_size=100)
    pub.publish(pos)

    

def find_coords(id):
    landmarks = land_pos()
    return(landmarks[id][2], landmarks[id][1])

def find_cam(i):
    cams = cam_pos()
    return(cams[i - 1][2],cams[i - 1][1])

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

