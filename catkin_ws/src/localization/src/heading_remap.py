#!/usr/bin/env python

# heading is the angle between the sensor x-axis ang Earth North axis
# if start from sensor x-axis, then the rotation is positive if CCW
# range between -180 and 180 degrees

import rospy
import tf
from math import degrees

from sensor_msgs.msg import Imu

def cb_imu(msg):
	imu_remap = Imu()
	imu_remap = msg
	quat = [msg.orientation.x, \
		msg.orientation.y, \
		msg.orientation.z, \
		msg.orientation.w]
	euler = tf.transformations.euler_from_quaternion(quat)
	yaw = euler[2] * -1
	quat_remap = tf.transformations.quaternion_from_euler(euler[0], euler[1], yaw)
	imu_remap.orientation = quat_remap
	pub_imu.publish(imu_remap)
	'''heading_rad = euler[2]
	heading_deg = degrees(heading_rad)
	# Convert to branch [0, 360)
	if heading_deg < 0:
		heading_deg += 360	
	print "IMU heading: ", heading_deg '''
	print degrees(euler[0]), degrees(euler[1]), degrees(yaw)

if __name__ == "__main__":
	rospy.init_node('view_heading_node')
	pub_imu = rospy.Publisher('/imu/data_corrected', Imu, queue_size = 20)
	rospy.Subscriber('/imu/data', Imu, cb_imu, queue_size = 20)
	rospy.spin()
