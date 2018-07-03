#!/usr/bin/env python

import rospy

from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped, Point, Vector3
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA

class VisualPath(object):
	def __init__(self):
		self.node_name = rospy.get_name()
		self.pub_path = rospy.Publisher("visual/fusion_path", Path, queue_size = 20)
		#self.pub_marker = rospy.Publisher("visual/path_marker", Marker, queue_size = 20)
		self.sub_odom = rospy.Subscriber("/odometry/filtered", Odometry, self.cb_odom, queue_size = 20)
		self.path = Path()
		#self.marker = Marker()
		#self.marker.type = Marker.POINTS
		#self.marker.action = Marker.ADD
		#self.marker.scale = Vector3(0.01, 0.01, 0.01)
		rospy.loginfo("[%s] Initialized ..." %(self.node_name))

	def cb_odom(self, msg):
		self.path.header = msg.header
		#self.marker.header = msg.header
		#point_ = Point()
		#point_ = msg.pose.pose.position
		#self.marker.points.append(point_)
		#self.marker.colors.append(ColorRGBA(0.5, 0.0, 1.0, 1.0))
		pose_ = PoseStamped()
		pose_.header = msg.header
		pose_.pose = msg.pose.pose
		self.path.poses.append(pose_)
		self.pub_path.publish(self.path)
		#self.pub_marker.publish(self.marker)

	
if __name__ == "__main__":
	rospy.init_node('visual_path_node', anonymous= False)
	visual = VisualPath()
	rospy.spin()	

