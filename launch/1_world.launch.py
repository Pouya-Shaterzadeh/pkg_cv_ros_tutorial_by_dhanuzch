import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_name = 'pkg_cv_ros_tutorial_by_dhanuzch'
    pkg_share = get_package_share_directory(pkg_name)
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    models_path = os.path.join(pkg_share, 'models')
    set_gazebo_model_path_cmd = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=models_path
    )

    world_file = os.path.join(pkg_share, 'worlds', '1_world.world')

    gazebo_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    return LaunchDescription([
        set_gazebo_model_path_cmd,
        gazebo_launch_cmd,
    ])
