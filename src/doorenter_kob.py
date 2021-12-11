#!/usr/bin/env python
# -*- coding: utf-8 -*-

# if door is open, go. if its close, 

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class EnterRoomServer():  
    def __init__(self):
        rospy.loginfo("Ready")
        self.twist_pub = rospy.Publisher('/vmegarocer/diff_drive_controller/cmd_vel', Twist,queue_size=1)
        self .front_laser_dist = 999.9
        rospy.Pubscriber('/scan', LaserScan, self.laserCB) #

    def laserCB(self, recieve_msg):
        self.laser_dist = recive_msg.ranges[359]

    def execute(self, srv_req):
        vel =Twist()                       
        vel.lineat.x = 10
	taeget_dist = 5       # ?
        safe_dist =1.0
        target_time = target_dist / vel.linear.x # time
        start_time = rospy.get_time()

        while not rospy.is_shutdown(): 

	    
            if  self.laser_dist > safe_dist:   # when safe dist
                print("now time:", rospy.get_time - start_time)
                selt.twist_pub.publish(vel)
            elif self.laser_dist <= safe_dist: # when door is close
                print("dude..can't enter room, open the door.")
                rospy.sleep(3.0)
            else:                              # when nothing in front
                vel.linear.x = 0
                self.twist_pub.publish(vel)
                end_time = rospy.get_time() - start_time 
                break

        if end_time >= target_time:
            print("Enter success")
            print("distance:", srv_req.dist, "velocity:" , srv_req.vel)

if __name__=="__main__":
    rospy.init_node("enter_room")
    ers = EnterRoomServer()                 
    rospy.spin()
