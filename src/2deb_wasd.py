#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

rospy.init_node("deb")
pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)

def main():
    vel = Twist()
    while not rospy.is_shutdown():
	move = raw_input("Puuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuush")
        if "w" in move:
            vel.linear.x = 0.1
        if "a" in move:
            vel.angular.z = 1
        if "s" in move:
            vel.linear.x = -0.1
        if "d" in move:
            vel.angular.z = -1
	pub.publish(vel)

if __name__ == '__main__':
    main()
