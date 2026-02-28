# Goal Description

The objective is to migrate the `pkg_cv_ros_tutorial_by_dhanuzch` repository from ROS 1 to ROS 2 (Foxy and newer), following the official ROS 2 Migration Guide. This includes updating package manifests, the build system (`ament_cmake`), Python source code for nodes, and transitioning ROS 1 XML launch files to ROS 2 Python launch files.

This plan has been structured to effectively delegate tasks among a team of 3 developers, ensuring efficient collaboration with clear boundaries of responsibility.

## Proposed Changes

---

### Developer 1: Package Manifest and Build System
**Responsibility**: Ensure the package's foundation is fully ROS 2 compliant. Update dependencies and build configurations to use `ament_cmake`.

#### [MODIFY] package.xml
- Change `<package format="2">` to at least format 3 for ROS 2 compatibility.
- Replace `<buildtool_depend>catkin</buildtool_depend>` with `<buildtool_depend>ament_cmake</buildtool_depend>`.
- Replace `build_depend`, `build_export_depend`, and `exec_depend` occurrences of `rospy` with `rclpy`.
- Add `sensor_msgs` and `cv_bridge` as `<exec_depend>` since they are required at runtime by the scripts.
- Add `<export><build_type>ament_cmake</build_type></export>` to declare the ament build type.

#### [MODIFY] CMakeLists.txt
- Update `cmake_minimum_required` to `VERSION 3.8`.
- Replace `find_package(catkin REQUIRED COMPONENTS rospy std_msgs)` with `find_package(ament_cmake REQUIRED)`.
- Use `install(PROGRAMS ...)` to install the Python scripts from `scripts/` into `lib/${PROJECT_NAME}` so they can be executed via `ros2 run`.
- Use `install(DIRECTORY ...)` to install [launch/](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/launch/2_world.launch), `models/`, and `worlds/` to the `share/${PROJECT_NAME}` destination.
- Replace `catkin_package()` with `ament_package()`.

---

### Developer 2: Python Node Migration
**Responsibility**: Migrate the ROS 1 specific Python code (`rospy`) to the ROS 2 API (`rclpy`).

#### [MODIFY] scripts/camera_read.py
- Change `import rospy` to `import rclpy` and include `from rclpy.node import Node`.
- Make the [camera_1](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/scripts/camera_read.py#10-31) class inherit from `Node` and update its [__init__](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/scripts/camera_read.py#12-14) constructor (e.g., `super().__init__('camera_read')`).
- Replace `rospy.Subscriber` with `self.create_subscription(Image, "/camera_1/image_raw", self.callback, 10)`.
- Update logging: replace `rospy.logerr(e)` with `self.get_logger().error(str(e))` and `rospy.loginfo` with `self.get_logger().info`.
- Rewrite the [main()](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/scripts/decode_qr.py#53-62) function to initialize `rclpy`, instantiate the node class, and use `rclpy.spin(node)`.
- Ensure appropriate shutdown logic (`node.destroy_node()`, `rclpy.shutdown()`).

#### [MODIFY] scripts/decode_qr.py
- Apply identical `rospy` to `rclpy` conversions for the node class and [main](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/scripts/decode_qr.py#53-62) function as described above.
- Verify that `cv_bridge` interactions correctly process `sensor_msgs/msg/Image` under the ROS 2 environment.

---

### Developer 3: Launch Files and Testing
**Responsibility**: Recreate the environment execution flow using ROS 2 Python launch files and conduct final system integration and testing.

#### [NEW] launch/1_world_and_script.launch.py
- Create a ROS 2 Python launch file.
- Implement logic to append the package's local `models` directory to the `GAZEBO_MODEL_PATH` environment variable.
- Include the standard `gazebo.launch.py` from the `gazebo_ros` package, configuring it to load the custom world file [worlds/1_world.world](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/worlds/1_world.world).
- Add a `Node` execution action for the `camera_read` script from this package.

#### [NEW] launch/2_world_and_script.launch.py
- Create a similar ROS 2 Python launch file pointing to [worlds/2_world.world](file:///home/pouya/pkg_cv_ros_tutorial_by_dhanuzch/worlds/2_world.world).
- Execute the `decode_qr` node concurrently with the Gazebo simulation.

#### [DELETE] launch/1_world_and_script.launch & launch/2_world_and_script.launch
- Safely remove the legacy ROS 1 XML launch files.

#### [DELETE] launch/1_world.launch & launch/2_world.launch
- Remove or convert these to standalone ROS 2 launch files, depending on team preference.

---

## Verification Plan

### Automated/Compilation Tests (Developer 1)
- Run `colcon build --symlink-install` from the workspace root workspace.
- Ensure the package compiles cleanly without CMake or ament errors.
- Verify that `source install/setup.bash` makes the package visible to `ros2 pkg list`.

### System Integration & Manual Verification (Developers 2 & 3)
- **Developer 3** will initiate the simulation using `ros2 launch pkg_cv_ros_tutorial_by_dhanuzch 1_world_and_script.launch.py`.
- **Developer 3** will verify that Gazebo starts with the correct environment and world layout.
- **Developer 2** and **Developer 3** will confirm that the popup `cv2.imshow` window appears and correctly shows the drone camera's viewpoint.
- **All developers** will then test `2_world_and_script.launch.py` and verify that the QR code is successfully detected, bounded by the blue box, and decoded in the live video output.















# pkg_cv_ros_tutorial_by_dhanuzch
This is the repo consisting of the ROS package used in "Using OpenCV with Gazebo in ROS" tutorial series by dhanuzch.medium.com

## Link to the Medium article
**[Part 0](https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-0-getting-everything-set-up-b60d4b2e472e) | [Part 1](https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-1-display-real-time-video-feed-a98c078c708b) | [Part 2](https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-2-read-and-decode-a-qr-code-ed6ce5c298ca)** 

 - Part 0 — Getting everything set up
 - Part 1 — Display real-time video feed of 2D camera in gazebo
 - Part 2 — Read and decode a QR Code present in Gazebo with pyzbar library
