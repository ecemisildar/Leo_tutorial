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

        self.image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.target_marker_id = (
            self.get_parameter('target_marker_id').get_parameter_value().integer_value
        )

        self.aruco_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.detector_parameters = self.create_detector_parameters()
        self.last_detection_state = None

        self.subscription = self.create_subscription(
            CompressedImage,
            self.image_topic,
            self.image_callback,
            10,
        )

        self.get_logger().info(f'Subscribed to image topic: {self.image_topic}')
        self.get_logger().info(f'Looking for ArUco marker id={self.target_marker_id}')

    # def image_callback(self, msg: CompressedImage) -> None:
    #     compressed = np.frombuffer(msg.data, dtype=np.uint8)
    #     gray_frame = cv2.imdecode(compressed, cv2.IMREAD_GRAYSCALE)

    #     if gray_frame is None:
    #         self.get_logger().error('Failed to decode compressed image frame.')
    #         return

    #     corners, ids, _rejected = self.detect_markers(gray_frame)
    #     detected_target = False

    #     if ids is not None and len(ids) > 0:
    #         for _marker_corners, marker_id in zip(corners, ids.flatten()):
    #             if int(marker_id) != int(self.target_marker_id):
    #                 continue

    #             detected_target = True
    #             break

    #     if detected_target != self.last_detection_state:
    #         status = 'detected' if detected_target else 'not detected'
    #         self.get_logger().info(f'ArUco ID {self.target_marker_id}: {status}')
    #         self.last_detection_state = detected_target
            
    def image_callback(self, msg):
        compressed = np.frombuffer(msg.data, dtype=np.uint8)
        gray = cv2.imdecode(compressed, cv2.IMREAD_GRAYSCALE)

        if gray is None:
            self.get_logger().error("decode failed")
            return

        self.get_logger().info_once(f"decode ok: {gray.shape}")

    def detect_markers(self, frame):
        if hasattr(cv2.aruco, 'ArucoDetector'):
            detector = cv2.aruco.ArucoDetector(
                self.aruco_dictionary,
                self.detector_parameters,
            )
            return detector.detectMarkers(frame)

        return cv2.aruco.detectMarkers(
            frame,
            self.aruco_dictionary,
            parameters=self.detector_parameters,
        )

    def create_detector_parameters(self):
        if hasattr(cv2.aruco, 'DetectorParameters'):
            return cv2.aruco.DetectorParameters()

        return cv2.aruco.DetectorParameters_create()


def main(args=None):
    rclpy.init(args=args)
    node = LeoArucoDetector()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
