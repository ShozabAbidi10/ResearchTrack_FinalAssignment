#include "ros/ros.h"                 // initializing the header file of ROS
#include "my_srv/F_a_new_target.h"   // initializing the header file of service package my_srv/F_a_new_target.h 
#include <math.h>


/**
 * Author: Shozab Abidi
 * This file is intializing the random index number service which will be send the
 * random index number to client node upon request.
 */

double randMToN(double M, double N){ 
   return M + (rand()/(RAND_MAX/(N-M))); 
}

/**
 * Callback function "target" for recieving min-max vales and 
 * sending back random index number. For recieving the request there
 * are two pointer for the request and response parts.
 *
 */
bool target (my_srv::F_a_new_target::Request&req, my_srv::F_a_new_target::Response&res){
   
  res.index = randMToN(req.min, req.max);
  return true;
}

/**
 * Main function for initializing the service server and advertising the
 * "/target" service.
 */

int main(int argc,char **argv)
{
  ros::init(argc,argv,"f_a_target_server");
  ros::NodeHandle n;
  ros::ServiceServer service= n.advertiseService("/target", target);
  ros::spin();
  return 0;
}
