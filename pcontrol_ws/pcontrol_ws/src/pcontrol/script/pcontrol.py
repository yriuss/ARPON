#! /usr/bin/python3.8

import rospy
from rospy.timer import Rate
#from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt,pi,fmod
from pyautogui import position


class TurtleBot:

    def __init__(self):
        rospy.init_node('pcontrol')

        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=1)

        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(15)

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
    
    
    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=10):
        return constant * self.smallest_angle_diff(self.steering_angle(goal_pose), self.pose.theta)

    def to_positive_angle(self, angle):
        angle = fmod(angle, 2*pi)
        while( angle < 0 ):
            angle = angle + 2*pi
        return angle

    def smallest_angle_diff(self, target, source):
        a = self.to_positive_angle(target) - self.to_positive_angle(source)
        if(a > pi):
            a = a - 2*pi
        elif(a < -pi):
            a = a + 2*pi
        return a

    def move2goal(self):
        goal_pose = Pose()
        x,y = position()
        x = x/100 - 1.19
        y = (767 - y)/100 - 0.65
        
        
        goal_pose.x = round(x,4)
        goal_pose.y = round(y,4)
        print(goal_pose.x,goal_pose.y)
        distance_tolerance = 0.2

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance and goal_pose.x >= 0 and goal_pose.y >= 0 and goal_pose.x <= 10 and goal_pose.y <= 10:
            x,y = position()
            x = x/100 - 1.19
            y = (767 - y)/100 - 0.65
            print(atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x))
            if(x >= 0 and y >= 0 and x <= 10 and y <=10):
                goal_pose.x = round(x,4)
                goal_pose.y = round(y,4)
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            print(goal_pose)
            print(self.pose)
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)
            
            self.velocity_publisher.publish(vel_msg)

            self.rate.sleep()

        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        x = TurtleBot()
        while not rospy.is_shutdown():
            x.move2goal()
    except rospy.ROSInterruptException:
        pass