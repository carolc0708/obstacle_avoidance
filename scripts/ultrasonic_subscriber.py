#!/usr/bin/env python

# subscriber: the control node of UAV
# purpose: receive the alert from ultrasonic sensors

import rospy
from std_msgs.msg import String

def callback(data):
	rospy.loginfo('Receive Alert: %s', data.data)

def ultrasonic_subscriber():
	rospy.init_node('ultra_sub', anonymous=True)
	rospy.Subscriber('ultra_pub', String, callback)

	rospy.spin()

if __name__ == '__main__':
	ultrasonic_subscriber()

