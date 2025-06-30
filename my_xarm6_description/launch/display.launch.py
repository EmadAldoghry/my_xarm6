from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

     # Get the URDF file
    urdf_path = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_description"), "urdf", "xarm6.urdf"]
    )
    robot_description = {"robot_description": Command(["cat ", urdf_path])}

    # Get the RViz config file (MODIFIED LINE)
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_description"), "rviz", "display.rviz"]
    )
    
    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
    )

    # Joint State Publisher GUI
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    
    # RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    return LaunchDescription(
        [
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )