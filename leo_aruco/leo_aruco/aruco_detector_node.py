#!/usr/bin/env python3

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage


class LeoArucoDetector(Node):
    def __init__(self):
        super().__init__('leo_aruco_detector')

        self.declare_parameter('image_topic', '/camera/image_rect_color/compressed')
        self.declare_parameter('target_marker_id', 1)

        self.image_topic = self.get_parameter('image_topic').value
        self.target_marker_id = int(self.get_parameter('target_marker_id').value)

        self.aruco_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.last_detection_state = None
        self._printed_decode_ok = False

        self.subscription = self.create_subscription(
            CompressedImage,
            self.image_topic,
            self.image_callback,
            10,
        )

        self.get_logger().info(f'Subscribed to image topic: {self.image_topic}')
        self.get_logger().info(f'Looking for ArUco marker id={self.target_marker_id}')
        self.get_logger().info(f'OpenCV version: {cv2.__version__}')

    def image_callback(self, msg: CompressedImage) -> None:
        compressed = np.frombuffer(msg.data, dtype=np.uint8)
        gray = cv2.imdecode(compressed, cv2.IMREAD_GRAYSCALE)

        if gray is None:
            self.get_logger().error('decode failed')
            return

        if not self._printed_decode_ok:
            self.get_logger().info(f"decode ok: {gray.shape}")
            self._printed_decode_ok = True

        corners, ids, rejected = cv2.aruco.detectMarkers(
            gray,
            self.aruco_dictionary,
        )

        detected_target = False
        if ids is not None:
            for marker_id in ids.flatten():
                if int(marker_id) == self.target_marker_id:
                    detected_target = True
                    break

        if detected_target != self.last_detection_state:
            status = 'detected' if detected_target else 'not detected'
            self.get_logger().info(f'ArUco ID {self.target_marker_id}: {status}')
            self.last_detection_state = detected_target


def main(args=None):
    rclpy.init(args=args)
    node = LeoArucoDetector()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()