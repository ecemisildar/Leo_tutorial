from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')
    robot_name = LaunchConfiguration('robot_name')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    start_teleop = LaunchConfiguration('start_teleop')

    model_file = PathJoinSubstitution(
        [FindPackageShare('leo_description'), 'urdf', 'leo_sim.urdf.xacro']
    )

    robot_description = Command(['xacro', ' ', model_file])

    state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': use_sim_time,
            }
        ],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py']
            )
        ),
        launch_arguments={'gz_args': ['-r ', world]}.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-name',
            robot_name,
            '-topic',
            'robot_description',
            '-x',
            x,
            '-y',
            y,
            '-z',
            z,
            '-Y',
            yaw,
        ],
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],
    )

    teleop = ExecuteProcess(
        condition=IfCondition(start_teleop),
        cmd=[
            'script',
            '-qec',
            'ros2 run leo_teleop leo_teleop_node',
            '/dev/null',
        ],
        output='screen',
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument('use_sim_time', default_value='true'),
            DeclareLaunchArgument('world', default_value='empty.sdf'),
            DeclareLaunchArgument('robot_name', default_value='leo_rover'),
            DeclareLaunchArgument('x', default_value='0.0'),
            DeclareLaunchArgument('y', default_value='0.0'),
            DeclareLaunchArgument('z', default_value='0.2'),
            DeclareLaunchArgument('yaw', default_value='0.0'),
            DeclareLaunchArgument('start_teleop', default_value='true'),
            gazebo,
            state_publisher,
            spawn_robot,
            bridge,
            teleop,
        ]
    )
