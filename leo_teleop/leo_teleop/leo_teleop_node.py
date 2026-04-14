#!/usr/bin/env python3

import sys
import termios
import tty

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class LeoTeleopNode(Node):
    def __init__(self):
        super().__init__('leo_teleop_node')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        self.linear_speed = 0.2
        self.angular_speed = 0.8

        self.get_logger().info('Leo teleop node started.')
        self.get_logger().info('Controls: w/s/a/d, x=stop, q=quit')

    def publish_cmd(self, linear_x=0.0, angular_z=0.0):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Published cmd_vel: linear.x={linear_x:.2f}, angular.z={angular_z:.2f}'
        )

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def run(self):
        print('\nControl the Leo Rover with keyboard:')
        print('  w = forward')
        print('  s = backward')
        print('  a = turn left')
        print('  d = turn right')
        print('  x = stop')
        print('  q = quit\n')

        while rclpy.ok():
            key = self.get_key()

            if key == 'w':
                self.publish_cmd(linear_x=self.linear_speed)
            elif key == 's':
                self.publish_cmd(linear_x=-self.linear_speed)
            elif key == 'a':
                self.publish_cmd(angular_z=self.angular_speed)
            elif key == 'd':
                self.publish_cmd(angular_z=-self.angular_speed)
            elif key == 'x':
                self.publish_cmd(0.0, 0.0)
            elif key == 'q':
                self.publish_cmd(0.0, 0.0)
                print('\nQuitting teleop node.')
                break


def main(args=None):
    rclpy.init(args=args)
    node = LeoTeleopNode()

    try:
        node.run()
    except KeyboardInterrupt:
        node.publish_cmd(0.0, 0.0)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()