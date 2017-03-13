#!/usr/bin/env python

# publisher: the ultrasonic sensors 
# purpose: alert the control of UAV if it's too close to obstacle

import rospy
from std_msgs.msg import String
import subprocess

def ultrasonic_publisher() :
	pub = rospy.Publisher('ultra_pub', String, queue_size=10)
	rospy.init_node('ultrasonic_publisher', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		result = "Publish Alert:"
		result += subprocess.Popen(["python","/home/carol/catkin_ws/src/obstacle_avoidance/scripts/ultrasonic_sensor.py"], stdout=subprocess.PIPE).communicate()[0]
		rospy.loginfo(result)
		pub.publish(result)
		rate.sleep()

if __name__ == '__main__':
	try:
		ultrasonic_publisher()
	except rospy.ROSInterruptException:
		pass
