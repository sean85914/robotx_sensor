#!/usr/bin/env python

import rospy

from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped, Point, Vector3
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA

class VisualPath(object):
	def __init__(self):
		self.node_name = rospy.get_name()
		self.pub_path = rospy.Publisher("visual/gps_odom", Path, queue_size = 20)
		self.sub_odom = rospy.Subscriber("/odometry/gps", Odometry, self.cb_odom, queue_size = 20)
		self.path = Path()
		rospy.loginfo("[%s] Initialized ..." %(self.node_name))

	def cb_odom(self, msg):
		self.path.header = msg.header
		pose_ = PoseStamped()
		pose_.header = msg.header
		pose_.pose = msg.pose.pose
		self.path.poses.append(pose_)
		self.pub_path.publish(self.path)

	
if __name__ == "__main__":
	rospy.init_node('visual_gps_node', anonymous= False)
	visual = VisualPath()
	rospy.spin()	

