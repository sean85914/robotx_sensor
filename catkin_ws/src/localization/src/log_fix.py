#!/usr/bin/env python

# Write the GPS reported longitude and latitude to a user-defined text file
# You can visualize the data if you convert the file from txt to xlxs (Excel file)
# and with the help of the website as below:
# https://mygeodata.cloud/converter/ or 
# http://www.gpsvisualizer.com/convert?output

import rospy
from sensor_msgs.msg import NavSatFix

def cb_fix(msg):
    print "Received data, logging..."
    f.write(str(msg.latitude))
    f.write(' ')
    f.write(str(msg.longitude))
    f.write('\n')

def shutdown():
    print "Node shutdown..."
    rospy.delete_param('~file_name')
    print "Deleted pararmeter"
    f.close()

if __name__ == '__main__':
    rospy.init_node('log_fix_node')
    rospy.Subscriber('/fix', NavSatFix, cb_fix, queue_size = 30)
    file_name = rospy.get_param('~file_name')
    f = open('/home/sean/robotx_sensor/catkin_ws/src/localization/log/' + file_name + '.txt', 'a+')
    f.write('latitude longitude\n')
    rospy.on_shutdown(shutdown)
    rospy.spin()

