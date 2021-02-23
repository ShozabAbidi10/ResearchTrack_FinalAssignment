#! /usr/bin/env python

###
### Author: Shozab Abidi
### Description: This file is handling all the user interface related
### along with merging different components of the project.
### 

# import ros stuff
import rospy                               
from std_srvs.srv import *                           ### Importing all std_srvs.srv dependecies
import time                                          ### Importing time dependecies         
from time import sleep                               ### Importing sleep from time
from geometry_msgs.msg import Twist                  ### Importing Twist msg from geometry_msgs.msgs
from move_base_msgs.msg import MoveBaseActionGoal    ### Importing MoveBaseActionGoal from move_base_msgs.msg
from actionlib_msgs.msg import GoalStatusArray       ### Importing GoalStatusArray from actionlib_msgs.msg
from my_srv.srv import F_a_new_target                ### Importing F_a_new_target service from my_srv.srv

target_list_ = [[-4,-3],[-4,2],[-4,7],[5,-7],[5,-3],[5,1]]   ### Initializing the list containing all the possible robot's target positions
target_reached_status = 0                                       


###
###  Callback function for checking the Robot's target achived status
###
def clbk_move_base_status(status):
    global target_reached_status                  
    if(len(status.status_list) > 0):               ### Checking if move_base/status status_list is not empty, which it is before 
                                                   ### recieving the target position for the first time after running the file.

    	if(status.status_list[0].status == 3):     ### In move_base/status topic list the status turns to 3 when robot reached the target.
					           ### Using this as flag to see when robot has reach the target position 
							
            target_reached_status = 1              ## When robot has reached the target position. We change the status to 1 which refers to
						   ## the when robot is reaching the target.

def main():
    rospy.init_node('f_a_user_interface')

    global  srv_random_index_, robot_move_base_status_, publish_new_target_, target_reached_status, srv_client_wall_follower_, publish_robot_vel_

    ### Initializing random index service client to get random index number.
    srv_random_index_ = rospy.ServiceProxy('/target', F_a_new_target)

    ### Initializing subscriber to the 'move_base/status' topic get the robot status.
    robot_move_base_status_ = rospy.Subscriber('/move_base/status', GoalStatusArray, clbk_move_base_status, queue_size=1)    

    ### Initializing publisher to publish new target postion in move_base/goal topic
    publish_new_target_ = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=1)

    ### Initializing service client to access the '/wall_follower_switch' script which allow robot to follow walls.
    srv_client_wall_follower_ = rospy.ServiceProxy('/wall_follower_switch', SetBool) 

    ### Initializing publisher to publish robot velocity in /cmd_vel topic
    publish_robot_vel_ = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)

    print("Hello!!!")

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        print("This is my final assignment simulation. Please choose robot state from 1 to 4")
        choosen_State = float(raw_input('I choose: '))
	if (choosen_State == 1):
                
                ### 1. Call service for randomly find new target position among given 6 points.
                ### 2. System will publish new target position on topic move_base/goal.
                ### 3. While reaching the target, system will provide status. 
                ### 4. Once target is achived, the system will notify the user that target is achived and if it should continue or user wants to change state.
                   
		resp = srv_client_wall_follower_(False)         ### Closing the 'following_wall' script for cases in which that running prior to this state. 
                resp = srv_random_index_(1,6)                   ### Requesting random index service for random index number  
                random_index_ = resp.index                      ### Recieving random index number.

                print("The new target position is (" + str(target_list_[random_index_-1][0]) + ", " + str(target_list_[random_index_-1][1]) + ")")

                ### 
		### Publishing the robot's new target goal on the "move_base/goal" topic.
                ### 'frame_id' and 'orientation.w' fields has been initialized as per the given instruction.
                ### x and y value has been set using recived random_index
		###                
			
		move_base = MoveBaseActionGoal()                               
		move_base.goal.target_pose.header.frame_id = "map"
		move_base.goal.target_pose.pose.orientation.w = 1
		move_base.goal.target_pose.pose.position.x = target_list_[random_index_-1][0]
		move_base.goal.target_pose.pose.position.y = target_list_[random_index_-1][1]
		publish_new_target_.publish(move_base)                                                

                print('Robot is reaching the new target')
		sleep(15)         
                target_reached_status = 0                        
                while(target_reached_status == 0):             ### Checking if robot has reached its target position or not.
                     sleep(1)
                print('Target is reached.')
         
        elif (choosen_State == 2):

        	# 1. System will ask user for new target position.
                # 2. System will check if this new target position matches with the given six positions. 
                # 3. If user's new target position matches then the system will publish new target position on topic move_base/goal.

                resp = srv_client_wall_follower_(False)      ### Closing the 'following_wall' script for cases in which that running prior to this state. 
              
		print("Please choose any one of the followng new target position for robot.")
		print("1.(-4,-3) 2.(-4,2) 3.(-4,7) 4.(5,-7) 5.(5,-3) 6.(5,1)")
                user_input = int(raw_input("Type the number of your desired new target position: "))
                print("The new target position is ("+ str(target_list_[user_input-1][0]) + ", " + str(target_list_[user_input-1][1]) + ")")

                ### 
		### Publishing the robot's new target goal on the "move_base/goal" topic.
                ### 'frame_id' and 'orientation.w' fields has been initialized as per the given instruction.
                ### x and y value has been set using user's input
		###  

		move_base = MoveBaseActionGoal()
		move_base.goal.target_pose.header.frame_id = "map"
		move_base.goal.target_pose.pose.orientation.w = 1
		move_base.goal.target_pose.pose.position.x = target_list_[user_input-1][0]
		move_base.goal.target_pose.pose.position.y = target_list_[user_input-1][1]
		publish_new_target_.publish(move_base)

                print('Robot is reaching the new target')
		sleep(15)
                target_reached_status = 0;
                while(target_reached_status == 0):       ### Checking if robot has reached its target position or not.
                     sleep(1)
                print('Target is reached.')

        elif (choosen_State == 3):

                # 1. Run follow wall script
                resp = srv_client_wall_follower_(True)       ### Running the robot's 'follow wall' script. 
                print('Robot is following the wall')

        elif (choosen_State == 4):

                # 1. Stop the Robot on the last reached target.

                resp = srv_client_wall_follower_(False)     ### Closing the 'following_wall' script for cases in which that running prior to this state.
                
		### 
		### Publishing the robot's velocity to be zero on the "/cmd_vel" topic.
		###  

                twist_msg = Twist()
        	twist_msg.linear.x = 0
        	twist_msg.angular.z = 0
        	publish_robot_vel_.publish(twist_msg)
                print('robot is stopped.')

        rate.sleep()


if __name__ == '__main__':
    main()
