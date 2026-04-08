# 8 Apr 2026, ROS2 channel_control node v.0.8 for a physical device channel_control
# This node works as a receiver ROS2 node corresponding to
# a physical device called channel_control
# This node reads data from ROS2 topic /ch_control_data
# and sends this data via UDP packets to the channel_control device over Ethernet
# Communication ROS2 -> channel_control is implemented in only one direction.
# If needed, add channel_control -> ROS2 communication here.

import socket
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray  # For raw bytes

CH_BLOCK_IP = '192.168.3.10' # ch_block IP address
CH_BLOCK_PORT = 1104         # ch_block Port for UDP connection

class ChBlocKNode(Node):
    def __init__(self):
        super().__init__('ch_block_node')
        self.subscription = self.create_subscription(
            UInt8MultiArray,   # message type
            '/ch_block_data_udp',  # topic name 
            self.callback,     # method, that will be called 
            # every time a message published in topic /ch_block_data_udp
            10   # queue size
        )
        self.get_logger().info(f"Subscriber is ready. Listening for UInt8MultiArray...")

        ### UDP connection to ch_block device
        # create a socket object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_logger().info(f"Socket for ch_block creation: OK")
        
    # callback is called every time a message is published in topic /ch_block_data_udp
    def callback(self, msg):   
        raw_bytes = bytes(msg.data) # convertion to bytes
        self.get_logger().info(
            f"Received {len(raw_bytes)} bytes: Hex: {raw_bytes.hex()}"
        )
        try:
            text = raw_bytes.decode('utf-8')
            self.get_logger().info(f"As text: '{text}'")
        except UnicodeDecodeError:
            pass # empty operator
        self.get_logger().info(f"UInt8MultiArray msg: {msg}") ## debug only

        def uint8multiarray_to_bytes(multiarray):
            return bytes(multiarray.data)

        # convert UInt8MultiArray to bytes object
        bytes_msg = uint8multiarray_to_bytes(msg) 
        self.get_logger().info(f"Bytes msg: {bytes_msg}") ## debug only

        # send the message to ch_block device
        self.sock.sendto(bytes_msg, (CH_BLOCK_IP, CH_BLOCK_PORT))
        self.get_logger().info(f"Sent UDP packet to {CH_BLOCK_IP}:{CH_BLOCK_PORT}")

def main():
    rclpy.init()         # init of ROS rclpy system
    node = ChBlocKNode() # create of ChBlocKNode object
    rclpy.spin(node)     # spin the ChBlocKNode node
    node.destroy_node()  # destroy the ChBlocKNode node
    rclpy.shutdown()     # shutdown the rclpy system

if __name__ == '__main__':
    main()
