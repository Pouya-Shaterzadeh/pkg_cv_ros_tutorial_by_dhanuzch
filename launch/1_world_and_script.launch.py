import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'pkg_cv_ros_tutorial_by_dhanuzch'
    pkg_share = get_package_share_directory(pkg_name)
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # Models path
    models_path = os.path.join(pkg_share, 'models')
    set_gazebo_model_path_cmd = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=models_path
    )

    # World file
    world_file = os.path.join(pkg_share, 'worlds', '1_world.world')

    # Include gazebo_ros empty_world launch file
    gazebo_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    # Node for camera_read
    camera_read_node = Node(
        package=pkg_name,
        executable='camera_read.py',
        name='camera_read',
        output='screen'
    )

    return LaunchDescription([
        set_gazebo_model_path_cmd,
        gazebo_launch_cmd,
        camera_read_node
    ])
