#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2

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

    (rows,cols,channels) = cv_image.shape
    
    image = cv_image

    resized_image = cv2.resize(image, (360, 640)) 

    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    thresh = 40
    img_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

    #cv2.imshow("B&W Image", gray)
    #cv2.imshow("B&W Image /w threshold", img_bw)

    qr_result = decode(img_bw)

    if qr_result:
        qr_data = qr_result[0].data
        print(qr_data)

        (x, y, w, h) = qr_result[0].rect

        cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 0, 255), 4)

        # Assuming qr_data is bytes in Python 3 from pyzbar, so decode. If it's str, this will throw, but usually it's bytes.
        try:
          text = "{}".format(qr_data.decode('utf-8'))
        except AttributeError:
          text = "{}".format(qr_data)
          
        cv2.putText(resized_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Camera output", resized_image)

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
