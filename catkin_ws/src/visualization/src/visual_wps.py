#!/usr/bin/env python

import rospy
from std_msgs.msg import ColorRGBA
from geometry_msgs.msg import Point, PoseArray, Vector3
from visualization_msgs.msg import Marker

marker = Marker()
marker.header.frame_id = 'odom'
marker.type = Marker.POINTS
marker.action = Marker.ADD
marker.scale = Vector3(0.1, 0.1, 0.1)

status_odom = False
status_lonlat = False

def cb_odom(msg):
	global marker
	global status_odom
	for i in range(0, len(msg.poses)):
		p = Point()
		p.x = msg.poses[i].position.x
		p.y = msg.poses[i].position.y
		marker.points.append(p)
		# Red points for odom
		c = ColorRGBA(1.0, 0.0, 0.0, 1.0)
		marker.colors.append(c)
	status_odom = True
	pub_data()

	
def cb_lonlat(msg):
	global marker
	global status_lonlat
	for i in range(0, len(msg.poses)):
		p = Point()
		p.x = msg.poses[i].position.x
		p.y = msg.poses[i].position.y
		marker.points.append(p)
		# Blue points for lonlat
		c = ColorRGBA(0.0, 0.0, 1.0, 1.0)
		marker.colors.append(c)
	status_lonlat = True
	pub_data()

def pub_data():
	global status_odom, status_lonlat
	global pub_marker
	if status_odom == True or status_lonlat == True:
		pub_marker.publish(marker)
		status_odom = status_lonlat = False

if __name__ == "__main__":
	rospy.init_node('visual_waypoints_node')
	global pub_marker
	pub_marker = rospy.Publisher('waypoints', Marker, queue_size = 20)
	rospy.Subscriber('/waypoints_odom', PoseArray, cb_odom, queue_size = 50)
	rospy.Subscriber('/waypoints_lonlat', PoseArray, cb_lonlat, queue_size = 50)
	rospy.spin()
