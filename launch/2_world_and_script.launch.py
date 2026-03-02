import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'pkg_cv_ros_tutorial_by_dhanuzch'
    pkg_share = get_package_share_directory(pkg_name)
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    px4_models_path = os.path.expanduser('~/PX4-Autopilot/Tools/simulation/gz/models')
    models_path = os.path.join(pkg_share, 'models') + ':' + px4_models_path
    
    set_gazebo_model_path_cmd = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    # World file
    world_file = os.path.join(pkg_share, 'worlds', '2_world.world')

    # Include ros_gz_sim launch file
    gazebo_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f"-r {world_file}"}.items()
    )

    # Bridge: Gazebo topic /camera -> ROS 2 topic /camera/image_raw
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera@sensor_msgs/msg/Image[gz.msgs.Image'
        ],
        remappings=[
            ('/camera', '/camera/image_raw')
        ],
        output='screen'
    )

    # Node for camera_read (subscribes to /camera/image_raw)
    camera_read_node = Node(
        package=pkg_name,
        executable='decode_qr.py',
        name='camera_read',
        output='screen'
    )

    return LaunchDescription([
        set_gazebo_model_path_cmd,
        gazebo_launch_cmd,
        bridge_node,
        camera_read_node
    ])
