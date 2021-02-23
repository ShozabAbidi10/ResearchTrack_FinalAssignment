#include "ros/ros.h"           // here we have included the header file 
#include "my_srv/Velocity.h"   //that generated automatically when we builtthe pakage. 

double randMToN(double M, double N){ 
   return M + (rand()/(RAND_MAX/(N-M))); 
}


// There are two pointer for the request part and response part.
bool myrandom (my_srv::Velocity::Request&req, my_srv::Velocity::Response&res){
  res.x= randMToN(req.min, req.max);
  res.z= randMToN(req.min, req.max);
  return true;
}



int main(int argc,char **argv)
{
  ros::init(argc,argv,"velocity_server");
  ros::NodeHandle n;
  ros::ServiceServer service= n.advertiseService("/velocity", myrandom);
  ros::spin();
  
  return 0;
}
