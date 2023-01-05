#!/usr/bin/env python3
from cmath import pi
import rospy
import tf.transformations as tft
from gazebo_msgs.srv import GetLinkState
from std_msgs.msg import Float32

def get_link_yaw(get_link_state_srv):
    # Call the service with the link name
    response = get_link_state_srv(link_name='ERC22_URDF::base_link')

    # Extract the orientation from the response
    orientation = response.link_state.pose.orientation

    quaternion = (orientation.x, orientation.y, orientation.z, orientation.w)

    # Convert the quaternion to Euler angles
    roll, pitch, yaw = tft.euler_from_quaternion(quaternion)

    if yaw < 0:
        yaw = 2*pi + yaw

    return yaw
 

def main():
    rospy.init_node('get_link_state_')

    # Wait for the service to be available
    rospy.wait_for_service('/gazebo/get_link_state')

    # Create a handle to the service
    get_link_state_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

    yaw_pub = rospy.Publisher('angle', Float32, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        yaw = get_link_yaw(get_link_state_srv)
        yaw_pub.publish(yaw)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

