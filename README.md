This repository contains five ROS 2 packages to help familiarize you with the Leo rovers. 
## [leo_teleop](leo_teleop)
This package is to teleoperate the real rover using the keyboard:
Control the Leo Rover with the keyboard:
  w = forward,
  s = backward,
  a = turn left,
  d = turn right,
  x = stop,
  q = quit

To run the package: 
 ```c
ros2 run leo_teleop leo_teleop_node
```

## [leo_communication](leo_communication)
This package is to send messages between 2 robots. 
Run each line on a different rover:
 ```c
ros2 run leo_communication receiver --ros-args -p robot_name:=rob_2
ros2 run leo_communication sender --ros-args -p robot_name:=rob_1 -p target_robot:=rob_2
```

## [leo_gazebo](leo_gazebo)
This package spawns a rover in the Gazebo environment and allows you to teleoperate it using the keyboard. 
```c
ros2 launch leo_gazebo leo_gazebo_teleop.launch.py start_teleop:=false
```

## [leo_aruco](leo_aruco)
This package is to detect an Aruco marker using the robot camera
```c
ros2 run leo_aruco aruco_detector_node
```

## [leo_common-ros2](https://github.com/LeoRover/leo_common-ros2)
This package is copied from the company website of the robots, which includes the URDF model of the robot

