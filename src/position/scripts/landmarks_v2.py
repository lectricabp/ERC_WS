#!/usr/bin/env python3

from cmath import pi
from re import M
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
      [5, 18.72, 17.19],
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
            [2, 0, 0.295]] #up left
    return cams

def listener():
    rospy.init_node('pos_comp', anonymous = False)

    rospy.Subscriber("angle", Float32, callback_angle)

    rospy.Subscriber("/left/pos_webCam",Position, callback_up_left)
    # rospy.Subscriber("/right/pos_webCam",Position, callback_up_right)
    rospy.spin()

def callback_angle(data):
    global angle_b
    angle_b = data.data #(pi / 180)


def callback_up_left(data):
    global angle_b
    x_land, y_land = find_coords(data.id)
    y_cam, x_cam = find_cam(2)
    #angle = abs(math.atan2(x_cam, y_cam))
    angle = pi/4
    # Robot axes frame
    y_r = y_cam + data.z*math.sin(angle) + data.x*math.cos(angle)
    x_r = x_cam - data.z*math.cos(angle) + data.x*math.sin(angle)

    #print(data.z, data.x)
    #print(y_cam, x_cam)
    pos_pub(2, y_r, x_r, y_land, x_land)


def callback_up_right(data):
    global angle_b
    x_land, y_land = find_coords(data.id)
    y_cam, x_cam = find_cam(1)
    #angle = math.atan2(x_cam, y_cam)
    angle = pi/4
    #Robot axes frame
    y_r = y_cam + data.z*math.sin(angle) - data.x*math.cos(angle)
    x_r = x_cam + data.z*math.cos(angle) + data.x*math.sin(angle)

    pos_pub(1, y_r, x_r, y_land, x_land)


def pos_pub(id, y_r, x_r, y_land, x_land):
    # Convert robot to global axes
    y_g = x_r*math.cos(angle_b) - y_r*math.sin(angle_b)
    x_g = x_r*math.sin(angle_b) + y_r*math.cos(angle_b)
    #print(y_r, x_r, y_land, x_land, y_g, x_g)
    # Find the global position
    X = x_land - y_g
    Y = y_land - x_g
    # Initialize the position variable
    pos = Position()
    pos.id = id
    pos.z = X
    pos.x = Y
    pos.angle = angle_b
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

