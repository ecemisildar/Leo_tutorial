#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Receiver(Node):
    def __init__(self):
        super().__init__('receiver')

        self.declare_parameter('robot_name', 'rob_2')
        self.robot_name = self.get_parameter('robot_name').value

        self.sub = self.create_subscription(
            String,
            '/fleet_messages',
            self.callback,
            10
        )

        self.get_logger().info(f'{self.robot_name} listening...')

    def callback(self, msg):
        data = msg.data

        # format: sender:hello rob_X
        try:
            sender, text = data.split(':')
        except:
            return

        if self.robot_name in text:
            self.get_logger().info(f'RECEIVED from {sender}: {text}')


def main(args=None):
    rclpy.init(args=args)
    node = Receiver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()