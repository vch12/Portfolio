# 8 Apr 2026, station_control_node.py, ROS-2 "Humble"
# This node runs on the station. A camera is directly connected through 
# a USB cable to the station. This node reads images from a camera, 
# process them and sends/reads messages from a remote Raspberry Pi. 
# Station <-> Raspberry communication is a direct, router less Wi-Fi connection.
# Raspberry uses two output pins to control servos depending on incoming 
# messages (day or night) based on processing of images from the camera.
# Raspberry also has three input pins, set to work as "buttons". Some sensor 
# periphery is connected there through three optocouplers.


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String 
from cv_bridge import CvBridge
import numpy as np

class LightControlNode(Node):
    def __init__(self):
        super().__init__('light_control_node')
        
        # camera subscription
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        
        # publishing commands for Raspberry
        self.publisher_ = self.create_publisher(String, '/rasp/cmd', 10)

        # subscription for a feedback from Raspberry (received:status + 3 inputs)
        self.feedback_sub = self.create_subscription(
            String,
            '/rasp/feedback',
            self.feedback_callback,
            10)

        self.br = CvBridge()
        self.threshold = 50.0  # Brightness threshold for a "night"
        self.get_logger().info('Station Control Node started. Checking light level...')

    def image_callback(self, data):
        try:
            # Conversion of ROS Image to OpenCV format
            current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')
        
            # convert to grayscale and calculate mean brigthness
            gray_frame = np.mean(current_frame)
        
            msg = String()
            if gray_frame < self.threshold: 
                msg.data = "NIGHT_MODE: ON"   # if dark, turn on "night"
                self.get_logger().warn(f'Dark ({gray_frame:.1f}). Sending NIGHT command to Raspberry')
            else:
                msg.data = "DAY_MODE: ON"     # if not dark, stay in "day"
                self.get_logger().info(f'Not dark ({gray_frame:.1f}). Sending DAY command to Raspberry')
        
            self.publisher_.publish(msg) # publish current day/night status

        except Exception as e:
            self.get_logger().error(f'Could not process image: {e}')

    def feedback_callback(self, msg): # if received a feedback from Raspberry
        self.get_logger().info(f'Received feedback from Raspberry: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = LightControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        pass
    finally: 
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
