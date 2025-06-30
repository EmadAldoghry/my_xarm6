import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder

def launch_setup(context, *args, **kwargs):
    # Initialize Arguments
    use_sim_time = LaunchConfiguration("use_sim_time")

    # Get the URDF path from our description package
    urdf_path = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_description"), "urdf", "xarm6.urdf"]
    )

    # Get the SRDF path from the moveit_config package
    srdf_path = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_moveit_config"), "config", "UF_ROBOT.srdf"]
    )

    # Get the controller config path
    controllers_path = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_moveit_config"), "config", "UF_ROBOT_controllers.yaml"]
    )
    
    # Get the ros2_controllers config path
    ros2_controllers_path = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_moveit_config"), "config", "ros2_controllers.yaml"]
    )
    
    # Get the rviz config path
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("my_xarm6_moveit_config"), "config", "moveit.rviz"]
    )

    # MoveIt Configuration
    moveit_config = (
        MoveItConfigsBuilder("xarm6", package_name="my_xarm6_moveit_config")
        .robot_description(file_path=urdf_path.perform(context)) # perform substitution to get string
        .robot_description_semantic(file_path=srdf_path.perform(context)) # perform substitution
        .trajectory_execution(
            file_path=controllers_path.perform(context), # perform substitution
            moveit_manage_controllers=True
        )
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    # Start the actual move_group node/action server
    run_move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict(), {"use_sim_time": use_sim_time}],
    )

    # RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            {"use_sim_time": use_sim_time},
        ],
    )

    # Static TF
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "link_base"],
    )

    # Publish TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description, {"use_sim_time": use_sim_time}],
    )

    # ros2_control using FakeSystem as hardware
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            ros2_controllers_path,
        ],
        output="screen",
    )

    # Load controllers
    load_controllers = []
    for controller in [
        "xarm6_traj_controller",
        "joint_state_broadcaster",
    ]:
        load_controllers.append(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[controller],
                output="screen",
            )
        )

    return [
        rviz_node,
        static_tf,
        robot_state_publisher,
        run_move_group_node,
        ros2_control_node,
    ] + load_controllers


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use sim time if true",
        )
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )