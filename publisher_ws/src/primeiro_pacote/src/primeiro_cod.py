#! /usr/bin/python3.8

import rospy
from rospy.timer import Rate
from std_msgs.msg import String

rospy.init_node('primeiro_no')

pub = rospy.Publisher('msg', String, queue_size=1)

rate = Rate(100)

count = 0

while not rospy.is_shutdown():
    dado = "new Hello, World"
    pub.publish(dado)
    count += 1
    rate.sleep()