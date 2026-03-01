#!/usr/bin/env python3

# Tutorial link: https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-1-display-real-time-video-feed-a98c078c708b
import rclpy
from rclpy.node import Node
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Camera1(Node):

  def __init__(self):
    super().__init__('camera_read')
    self.bridge = CvBridge()
    self.image_sub = self.create_subscription(
        Image,
        '/camera_1/image_raw',
        self.callback,
        10
    )

  def callback(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
    except CvBridgeError as e:
      self.get_logger().error(str(e))
      return
    
    image = cv_image

    resized_image = cv2.resize(image, (360, 640)) 

    #cv2.imshow("Camera output normal", image)
    cv2.imshow("Camera output resized", resized_image)

    cv2.waitKey(3)

def main(args=None):
    rclpy.init(args=args)
    camera_node = Camera1()
    
    try:
        rclpy.spin(camera_node)
    except KeyboardInterrupt:
        camera_node.get_logger().info("Shutting down")
    finally:
        camera_node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
