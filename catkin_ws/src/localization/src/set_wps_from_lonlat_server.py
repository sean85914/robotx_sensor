#!/usr/bin/env python

import rospy
import utm
import tf
from math import cos, sin
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import PoseArray, Pose
from localization.srv import *

pose_array = PoseArray()
pose_array.header.frame_id = 'odom'
status = False
x_ = y_ = theta_= None

def handle_set_wps(req):
	global x_, y_, theta_
	global status
	global pose_array
	
	utm_x, utm_y, _, _ = utm.from_latlon(req.lat, req.lon)
	
	resp = set_wps_from_lonlatResponse()
	
	if status == True:
		c_ = cos(theta_)
		s_ = sin(theta_)
		resp.x =  utm_x * c_ + utm_y * s_ - x_ * c_ - y_ * s_
		resp.y = -utm_x * s_ + utm_y * c_ + x_ * s_ - y_ * c_
		rospy.loginfo("[%s] odom x: %s, y: %s" %(rospy.get_name(), resp.x, resp.y))
		p = Pose()
		p.position.x = resp.x
		p.position.y = resp.y
		p.orientation.w = 1
		pose_array.poses.append(p)
		return resp
		
def cb_tf(msg):
	global x_, y_, theta_
	global status

	if status == True:
		return
	x_ = msg.transforms[0].transform.translation.x
	y_ = msg.transforms[0].transform.translation.y
	quat_ = [msg.transforms[0].transform.rotation.x, \
		 msg.transforms[0].transform.rotation.y, \
		 msg.transforms[0].transform.rotation.z, \
		 msg.transforms[0].transform.rotation.w]
	euler_ = tf.transformations.euler_from_quaternion(quat_)
	theta_ = euler_[2]
	rospy.loginfo("[%s] x: %s, y: %s, theta: %s" %(rospy.get_name(), x_, y_, theta_))
	status = True
	rospy.loginfo("[%s] Ready to set waypoints" %(rospy.get_name()))
	
def pub_data(event):
	global pub_wps

	if len(pose_array.poses)!= 0:
		pose_array.header.stamp = rospy.Time.now()
		pub_wps.publish(pose_array)

def main():
	rospy.init_node('set_wps_from_lonlat_server_node')
	server = rospy.Service('set_wps_from_lonlat', set_wps_from_lonlat, handle_set_wps)
	sub_tf = rospy.Subscriber('/tf_static', TFMessage, cb_tf, queue_size = 1)
	global pub_wps
	pub_wps = rospy.Publisher('/waypoints_lonlat', PoseArray, queue_size = 20)
	rospy.Timer(rospy.Duration(1.0), pub_data)
	rospy.spin()


if __name__ == "__main__":
	main()
