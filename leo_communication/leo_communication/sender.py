#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Sender(Node):
    def __init__(self):
        super().__init__('sender')

        self.declare_parameter('robot_name', 'rob_1')
        self.declare_parameter('target_robot', 'rob_2')

        self.robot_name = self.get_parameter('robot_name').value
        self.target_robot = self.get_parameter('target_robot').value

        self.pub = self.create_publisher(String, '/fleet_messages', 10)

        self.timer = self.create_timer(2.0, self.send_message)

        self.get_logger().info(f'{self.robot_name} sending to {self.target_robot}')

    def send_message(self):
        msg = String()
        msg.data = f'{self.robot_name}:hello {self.target_robot}'
        self.pub.publish(msg)

        self.get_logger().info(f'SENT: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = Sender()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()