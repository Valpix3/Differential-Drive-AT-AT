# Differential-Drive-AT-AT
Differential drive robot inspired by the AT-AT from Star Wars, using ROS2 and Gazebo


XML for the URDF file that defines the structure (links and joints) of the AT-AT inspired Differential Drive robot. 
Xacro file to define physics like material, mass, friction, and sensors (camera and LIDAR)
Python program to control the movement of the robot and obstacle avoidance using LIDAR sensor input.

Required terminal commands:
source /opt/ros/humble/setup.bash
ros2 launch <foldername> AT-AT_w.launch.py
ros2 run <foldername> diff_drive
