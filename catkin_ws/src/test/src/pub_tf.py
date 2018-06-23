#!/usr/bin/env python
import rospy
import tf
import numpy
from math import degrees
from sensor_msgs.msg import Imu

def cb_imu(msg):
	quat = [msg.orientation.x, msg.orientation.y,\
		msg.orientation.z, msg.orientation.w]
	angles = tf.transformations.euler_from_quaternion(quat)
	print degrees(angles[0]), degrees(angles[1]), degrees(angles[2])

if __name__ == '__main__':
	rospy.init_node("rpy_node", anonymous= False)
	rospy.Subscriber("/imu/data", Imu, cb_imu, queue_size = 50)
	rospy.spin()
