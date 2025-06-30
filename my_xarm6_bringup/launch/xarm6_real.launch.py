from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip",
            description="IP address of the robot",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "report_type",
            default_value="normal",
            description="Tcp report type",
        )
    )

    # Initialize Arguments
    robot_ip = LaunchConfiguration("robot_ip")
    report_type = LaunchConfiguration("report_type")
    
    # Your fake launch file, but with the robot_ip
    fake_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("my_xarm6_bringup"), "launch", "xarm6_fake.launch.py"]
            )
        ),
        # We don't need to pass robot_ip here because it's read from the URDF's ros2_control tag now.
        # This is a key part of the simplification!
    )

    return LaunchDescription(
        declared_arguments
        + [
            fake_launch,
        ]
    )