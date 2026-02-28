cmake_minimum_required(VERSION 3.8)
project(pkg_cv_ros_tutorial_by_dhanuzch)

# Default to C++14 or newer for ROS 2 if any C++ code is added in the future
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)

# Install executable python scripts to the package's lib directory
install(PROGRAMS
  scripts/camera_read.py
  scripts/decode_qr.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install specific directories to the package's share directory
install(DIRECTORY
  launch/
  models/
  worlds/
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
