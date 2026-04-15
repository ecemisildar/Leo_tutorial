#!/usr/bin/env python3

import cv2

import rclpy
from cv_bridge import CvBridge, CvBridgeError
from rclpy.node import Node
from sensor_msgs.msg import Image


class LeoArucoDetector(Node):
    def __init__(self):
        super().__init__('leo_aruco_detector')

        self.declare_parameter('image_topic', '/camera/image_rect_color')
        self.declare_parameter('target_marker_id', 1)

        self.image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.target_marker_id = (
            self.get_parameter('target_marker_id').get_parameter_value().integer_value
        )

        self.bridge = CvBridge()
        self.aruco_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.detector_parameters = self.create_detector_parameters()

        self.subscription = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10,
        )

        self.get_logger().info(f'Subscribed to image topic: {self.image_topic}')
        self.get_logger().info(f'Looking for ArUco marker id={self.target_marker_id}')

    def image_callback(self, msg: Image) -> None:
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except CvBridgeError as exc:
            self.get_logger().error(f'Failed to convert image: {exc}')
            return

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _rejected = self.detect_markers(gray_frame)
        detected_target = False

        if ids is not None and len(ids) > 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            for marker_corners, marker_id in zip(corners, ids.flatten()):
                if int(marker_id) != int(self.target_marker_id):
                    continue

                detected_target = True
                points = marker_corners.reshape((4, 2)).astype(int)
                center_x = int(points[:, 0].mean())
                center_y = int(points[:, 1].mean())

                cv2.putText(
                    frame,
                    f'Target ID {marker_id}',
                    (center_x - 60, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        status_text = (
            f'ArUco ID {self.target_marker_id}: detected'
            if detected_target
            else f'ArUco ID {self.target_marker_id}: not detected'
        )
        status_color = (0, 255, 0) if detected_target else (0, 0, 255)

        cv2.putText(
            frame,
            status_text,
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            status_color,
            2,
            cv2.LINE_AA,
        )

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
