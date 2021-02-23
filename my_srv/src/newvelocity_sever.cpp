#include "ros/ros.h"           // here we have included the header file 
#include "my_srv/Newvelocity.h"   //that generated automatically when we builtthe pakage. 
#include <math.h>


#define PI 3.1415926

// There are two pointer for the request part and response part.
bool harmonic (my_srv::Newvelocity::Request&req, my_srv::Newvelocity::Response &res){
  	res.vel = 0.1 + 2*sin(PI*req.pos/7 -2*PI/7);
  return true;
}


int main(int argc,char **argv)
{
  ros::init(argc,argv,"newvelocity_server");
  ros::NodeHandle n;
  ros::ServiceServer service= n.advertiseService("/newvelocity", harmonic);
  ros::spin();
  
  return 0;
}
