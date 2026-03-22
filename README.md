# pkg_cv_ros_tutorial_by_dhanuzch — ROS 2 Jazzy Jalisco Migration

This is a fork of [dhanuzch/pkg_cv_ros_tutorial_by_dhanuzch](https://github.com/dhanuzch/pkg_cv_ros_tutorial_by_dhanuzch), fully migrated from **ROS 1 (Noetic / Ubuntu 20.04)** to **ROS 2 Jazzy Jalisco (Ubuntu 24.04)**. All changes follow the [official ROS 2 migration guide](https://docs.ros.org/en/jazzy/How-To-Guides/Migrating-from-ROS1.html) and have been verified on a clean Ubuntu 24.04 install with Gazebo Harmonic.

> 📖 **Full step-by-step migration documentation:**  
> [https://pouya-shaterzadeh.github.io/docs/ur_reach_migration/](https://pouya-shaterzadeh.github.io/docs/ur_reach_migration/)

---

## About the original tutorial

This package is used in the *"Using OpenCV with Gazebo in ROS"* tutorial series by [dhanuzch](https://dhanuzch.medium.com):

**[Part 0](https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-0-getting-everything-set-up-b60d4b2e472e) | [Part 1](https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-1-display-real-time-video-feed-a98c078c708b) | [Part 2](https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-2-read-and-decode-a-qr-code-ed6ce5c298ca)**

- **Part 0** — Getting everything set up
- **Part 1** — Display real-time video feed of a 2D camera in Gazebo
- **Part 2** — Read and decode a QR code present in Gazebo with the pyzbar library

---

## What changed in this migration

### `package.xml`
- Bumped to **format 3** (required by ROS 2).
- Replaced `catkin` buildtool with `ament_cmake`.
- Replaced `rospy` with `rclpy`, `sensor_msgs`, `cv_bridge`.
- Added `ros_gz_sim` and `ros_gz_bridge` for Gazebo Harmonic integration.
- Added `<export><build_type>ament_cmake</build_type></export>`.

### `CMakeLists.txt`
- Updated minimum CMake version to **3.8**.
- Replaced `find_package(catkin …)` / `catkin_package()` with `find_package(ament_cmake …)` / `ament_package()`.
- Added `install(PROGRAMS …)` so scripts are accessible via `ros2 run`.
- Added `install(DIRECTORY …)` for `launch/`, `models/`, and `worlds/`.

### `scripts/camera_read.py`
- Ported from `rospy` to `rclpy`; node class inherits from `rclpy.node.Node`.
- Subscriber created with `self.create_subscription(Image, '/camera/image_raw', …, 10)`.
- Logging via `self.get_logger().error()` / `.info()`.
- `main()` uses `rclpy.init()`, `rclpy.spin()`, and graceful `destroy_node()` / `rclpy.shutdown()`.

### `scripts/decode_qr.py`
- Same `rospy` → `rclpy` port as `camera_read.py`.
- Frames are pre-processed with grayscale conversion + binary threshold for reliable pyzbar decoding under Gazebo Harmonic.
- Draws a **green bounding polygon** around each detected QR code and prints the decoded text to the terminal.

### `launch/` — ROS 1 XML → ROS 2 Python

| Old (ROS 1 XML) | New (ROS 2 Python) |
|---|---|
| `1_world.launch` | `1_world.launch.py` |
| `2_world.launch` | `2_world.launch.py` |
| `1_world_and_script.launch` | `1_world_and_script.launch.py` |
| `2_world_and_script.launch` | `2_world_and_script.launch.py` |

- All files use `ros_gz_sim` (`gz_sim.launch.py`) instead of the legacy `gazebo_ros`.
- The `_and_script` variants additionally launch a `ros_gz_bridge` node that bridges the Gazebo `/camera` image topic to the ROS 2 `/camera/image_raw` topic.
- `GZ_SIM_RESOURCE_PATH` is configured so Gazebo Harmonic can locate the custom drone model.

---

## How to build and run

### Prerequisites
- Ubuntu 24.04
- ROS 2 Jazzy Jalisco (`ros-jazzy-desktop`)
- `ros-jazzy-ros-gz` (Gazebo Harmonic bridge)
- `python3-cv-bridge`, `python3-pyzbar`

### Build
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/Pouya-Shaterzadeh/pkg_cv_ros_tutorial_by_dhanuzch.git
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### Part 1 — Live camera feed (Tutorial Part 1)
```bash
ros2 launch pkg_cv_ros_tutorial_by_dhanuzch 1_world_and_script.launch.py
```
An OpenCV window titled **"Camera output resized"** appears showing the drone's downward-facing camera view.

### Part 2 — QR code detection (Tutorial Part 2)
```bash
ros2 launch pkg_cv_ros_tutorial_by_dhanuzch 2_world_and_script.launch.py
```
The **"Camera output"** window shows a live feed. When a QR code enters the frame a **green bounding polygon** is drawn around it and the decoded text is printed to the terminal.

---

## Related links
- 🔗 Original repository: [dhanuzch/pkg_cv_ros_tutorial_by_dhanuzch](https://github.com/dhanuzch/pkg_cv_ros_tutorial_by_dhanuzch)
- 📖 Migration documentation: [https://pouya-shaterzadeh.github.io/docs/ur_reach_migration/](https://pouya-shaterzadeh.github.io/docs/ur_reach_migration/)
