#!/usr/bin/env python3

import rospy
import tf.transformations as tft
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64

def orientation_callback(msg):
    # Print the message
    #print(msg)

    # Get the quaternion from the message
    quaternion = (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w)

    # Convert the quaternion to Euler angles
    roll, pitch, yaw = tft.euler_from_quaternion(quaternion)

    # Publish the yaw angle
    yaw_angle_publisher.publish(yaw)

def main():
    # Initialize the ROS node
    rospy.init_node('yaw_angle_node')

    # Create a publisher for the yaw angle
    global yaw_angle_publisher
    yaw_angle_publisher = rospy.Publisher('yaw_angle', Float64, queue_size=10)

    # Create a subscriber for the orientation topic
    orientation_subscriber = rospy.Subscriber('imu', Imu, orientation_callback)

    # Spin the ROS node
    rospy.spin()

if __name__ == '__main__':

    main()

