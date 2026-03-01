import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_name = 'pkg_cv_ros_tutorial_by_dhanuzch'
    pkg_share = get_package_share_directory(pkg_name)
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    models_path = os.path.join(pkg_share, 'models')
    set_gazebo_model_path_cmd = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    world_file = os.path.join(pkg_share, 'worlds', '1_world.world')

    gazebo_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f"-r {world_file}"}.items()
    )

    return LaunchDescription([
        set_gazebo_model_path_cmd,
        gazebo_launch_cmd,
    ])
