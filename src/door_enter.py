#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------
# Desc: If the door opens, proceed. If it is near, stay there. Useless code.
# Author: Hiroto Washio
# Date: Jan 2021
#--------
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
        vel = Twist()
        vel.linear.x = 0.3
        target_dist = 3.0
        safe_dist = 1.0
        target_time = target_dist / vel.linear.x
        end_time = 0
        count = 0
        while not rospy.is_shutdown():
            start_time = time.time() 
            if self.front_laser_dist >= safe_dist and count == 0:
                print ": now time ---", time.time() - start_time
                self.twist_pub.publish(vel)
                rospy.sleep(0.2)
            elif self.front_laser_dist <= safe_dist:
                print "Oops! can't enter room, open the door."
                rospy.sleep(0.2)  
                waited_time = time.time()
                if self.front_laser_dist >= safe_dist and (time.time()-waited_time) <= 4.0:
                    self.twist_pub.publish(vel)
                    print "Im going to enter room."
                    rospy.sleep(0.1)
                else:
                    count += 1
                    end_time = time.time()
                    pass
            if end_time >= target_time and  self.front_laser_dist > safe_dist:
                print "Im going to enter room."
                rospy.sleep(2.0)
                self.twist_pub.publish(vel)
                last_time = time.time()
                while not rospy.is_shutdown():
                    if last_time - time.time() >= float(5.0):
                        vel.linear.x = 0.0
                        self.twist_pub.publish(vel)
                        print "Im done."
                        break

if __name__=="__main__":
    rospy.init_node("door_enter")
    ers = EnterRoomServer()
    ers.execute()
    rospy.spin()
