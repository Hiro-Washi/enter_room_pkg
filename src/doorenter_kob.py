#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class EnterRoomServer():
    def __init__(self):
        self.twist_pub = rospy.Publisher('/vmegarover/diff_drive_controller/cmd_vel', Twist, queue_size=10)
        rospy.loginfo("Ready")
        rospy.Subscriber('/scan', LaserScan, self.laserCB) 
        self.front_laser_dist = 999.9

    def laserCB(self, receive_msg):
        self.front_laser_dist = receive_msg.ranges[359]

    def execute(self):
        print "Im OK."
        vel = Twist()
        vel.linear.x = 0.2
        target_dist = 3.0
        safe_dist = 1.0
        target_time = target_dist / vel.linear.x
        start_time = time.time()
        

        while not rospy.is_shutdown():
            if self.front_laser_dist >= safe_dist and (time.time() - start_time) < target_time:
                print ": now time ---", time.time() - start_time
                self.twist_pub.publish(vel)
                rospy.sleep(0.05)
            elif self.front_laser_dist <= safe_dist:
                 print "Oops! can't enter room, open the door."
                 rospy.sleep(1.0)
            else:
                vel.linear.x = 0.0
                self.twist_pub.publish(vel)
                end_time = time.time() - start_time
                break

        if end_time >= target_time and  self.front_laser_dist > safe_dist:               
            print "Im going to enter room."
            rospy.sleep(2.0)
            vel.linear.x = 0.5
            self.twist_pub.publish(vel)
            start_time = time.time()
            while not rospy.is_shutdown():
                if start_time - time.time >= float(5.0):
                    vel.linear.x = 0.0
                    self.twist_pub.publish(vel)
                    print "Im done."
                    break

if __name__=="__main__":
    rospy.init_node("door_enter")
    ers = EnterRoomServer()
    ers.execute()
    rospy.spin()

'''      linear_speed = 0.5
         target_dist = 5
        target_time = target_dist/linear_speed

         
         if back_time - rospy.get_time() >= 1:
             vel.linear.x = 0
             rospy.sleep(1.0)

'''
