# Research_Track FinalAssignment:

This assignment requires controlling a robot in visualization tools Gazebo and Rviz using planning algorithm move_base and follow wall.

### Content Structure

There are two packages **final_assignment** and **my_srv**. Each of these packages contain nodes which perform their assigned functionalities. Please find the breakdown of these functionalities below.

## final_assignment Package

In final_assignment package we have multiple components such as house.world file which is our simulation environment. For execution purposes of this simulation environment we use simuation_gmapping.launch file which present in the launch folder. Besides this we also have Sim.rviz file in config folder. Since we our using move_base technique for localization and mapping the simulation environment, therefore we also a have move_base.launch file in launch folder. 

To accommodate the 'follow_wall' functionality of the robot, we have a wall_follow_service_m.py file in the scripts folder which allow robot to move continuously along the wall. Beside this we have a main file named 'f_a_user_interface.py' (f_a_user_interface is stands for final_assignment user interface) which handles all the user interface related functionalities along with merging other nodes. The details of the functionalities performed in this node is explain below.

This node perform following functionalities:

1. In this node we have initialized two service clients one for 'f_a_target_server' in order to receive random target index and one for robot wall follower script which basically allows to robot to follow walls as mentioned above.  
2. There is one subscriber initialized to '/move_base/status' topic of type GoalStatusArray which we use to see weather the robot has reached its target or not. 
3. There are two publishers also initialized in this node one to publish the robot's new target values in the topic '/move_base/goal' and the second one to publish robot's velocities in the '/cmd_vel' topic. 
4. The user interface is designed to allow user to decide which state of the robot they want execute out of total four. 
     a) In the first state, the robot randomly choose the new target position values from a set of six predefined positions. Once the robot has reached to its target position the user has the option to keep it this state or change it to something else. In order to achieve this behaviour we first send request to f_a_target_server for random target index then by using this index value we set the new target position for robot. Once the new target position has been set we publish these values to '/move_base/status' topic.  
     b) In the second state, the robot ask the user to choose the new target position from the list of six predefined positions. Again, once the robot has reached to its target position the user will have the option change the state or keep it as it is. We achieve this behaviour of robot by first finalizing the robot's new target values using user's input and then publishing it on '/move_base/status' topic.   
     c) In the third state, the robot follow the simulated environment wall using the wall follower service client
     d) In the fourth state, the robot stops in its position. We do it by publishing the robot's velocity values as zero in '/cmd_vel' topic. 

## my_srv Package

1. This node implement a ROS f_a_target_server which request for the min and max values which in our case are as follows: 
```
min:= 1 ; max:= 6
```

2. In reply to this request, the server randomly generates a number within this range which we use for indexing in state 1. 

## Computation graph: 

![alt text](https://github.com/ShozabAbidi10/ResearchTrack_FinalAssignment/blob/main/rqt_graph.PNG)

## Instruction to run the code

1. Once you have successfully cloned or downloaded this respository then execute the following command. Make sure you are in the ros workspace in your terminal.
```
catkin_make
```

2. Launch the gmapping simulation in Gazebo and Rviz by executing the following command:
```
roslaunch final_assignment simulation_gmapping.launch
```

3. Open a new terminal tab and execute the move_base.launch file by using following command.
```
roslaunch final_assignment move_base.launch
```

4. Open another terminal tab and execute the wall follow service by using the following command:
```
rosrun final_assignment wall_follow_service_m.py
```

5. Open an other terminal tab and launch f_a_target_server by using the following command. 
```
rosrun my_srv f_a_target_server
```
6. Finally launch the main user interface file by using the following command. 
```
rosrun final_assignment f_a_user_interface.py
```

# Note: 
At any stage if there is an error regarding "No such file or directory found" or any command not executing properly. Do the following steps.

Step 1: Make sure that currently you are in my_ros_ws directory, execute the following command
```
cd devel 
```
Step 2: Run the setup.bash file by using this command.

```
source setup.bash 
```
Step 3: Go back to my_ros_ws directory and the run that command again. Hopefully it will run this time.
 
