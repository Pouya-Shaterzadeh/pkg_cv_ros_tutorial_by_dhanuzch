#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2
import numpy as np

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pyzbar.pyzbar import decode

class Camera1(Node):

  def __init__(self):
    super().__init__('decode_qr')
    self.bridge = CvBridge()
    self.image_sub = self.create_subscription(
        Image,
        '/camera/image_raw',
        self.callback,
        10
    )

  def callback(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      self.get_logger().error(str(e))
      return

    # Keep original image size instead of squishing it (avoids distortion)
    image = cv_image
    
    # Pre-process image to optimize for pyzbar (grayscale + threshold)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
    
    # Run pyzbar decode on the thresholded image
    decoded_objects = decode(thresh)

    for obj in decoded_objects:
        # Get polygon points
        points = obj.polygon
        # Note: If the polygon has more than 4 points, we can compute the convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = hull.reshape(-1, 2)
        
        # Draw the bounding polygon (green color like in sky_warriors_ws)
        for j in range(len(points)):
            cv2.line(image, tuple(points[j]), tuple(points[(j+1) % len(points)]), (0, 255, 0), 3)

        # Draw the text at the top-left corner
        x = obj.rect.left
        y = obj.rect.top
        
        # Format the barcode text
        try:
          qr_data = obj.data.decode('utf-8')
        except AttributeError:
          qr_data = str(obj.data)

        # Print to terminal
        print(qr_data)
        
        # Render the text above the bounding box
        cv2.putText(image, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Camera output", image)
    cv2.waitKey(5)

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
