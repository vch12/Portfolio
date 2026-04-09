# 8 Apr 2026, raspberry_node.py, ROS-2 "Humble"
# This node runs on the Raspberry. A camera is directly connected through 
# a USB cable to the station. Station node reads images from the camera, 
# process them and sends/reads messages from a remote Raspberry Pi. 
# Station <-> Raspberry communication is a direct, router less Wi-Fi connection.
# Raspberry uses two output pins to control servos depending on incoming 
# messages (day or night) based on processing of images from the camera.
# Raspberry also has three input pins, set to work as "buttons".
# Sensor periphery is connected to Raspberry through three optocouplers.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from gpiozero import DigitalOutputDevice, Button
import time

class RaspberryNode(Node):
    def __init__(self):
        super().__init__('raspberry_node')

        # Setting GPIO Outputs
        # pin_day and pin_night - are independent pins for different systems
        self.pin_day = DigitalOutputDevice(12)   # pin 32 on board
        self.pin_night = DigitalOutputDevice(16) # pin 36 on board

        # Setting GPIO Inputs (as buttons, optocouplers are connected)
        # pull_up=False, when optocoupler gives +3.3V to a GPIO pin 
        self.inputs = {
            1: Button(23, pull_up=False), # pin 16 on board
            2: Button(24, pull_up=False), # pin 28 on board
            3: Button(25, pull_up=False)  # pin 22 on board
        }

        # ROS publishing and subscription 
        self.publisher_ = self.create_publisher(String, '/rasp/feedback', 10)
        self.subscription = self.create_subscription(
            String,
            '/rasp/cmd',
            self.cmd_callback,
            10)

        # Associate input state changes with publishing messages (Interrupt-driven)
        self.inputs[1].when_pressed = lambda: self.send_input_status(1, 1)
        self.inputs[1].when_released = lambda: self.send_input_status(1, 0)
        
        self.inputs[2].when_pressed = lambda: self.send_input_status(2, 1)
        self.inputs[2].when_released = lambda: self.send_input_status(2, 0)
        
        self.inputs[3].when_pressed = lambda: self.send_input_status(3, 1)
        self.inputs[3].when_released = lambda: self.send_input_status(3, 0)

        # Wait until central station is fully booted
        self.get_logger().info('Waiting 30s for Station to boot...')
        time.sleep(30)
    
        # Send initial statuses of inputs (once after power ON)
        self.send_initial_states()
        self.get_logger().info('Raspberry Node is ready!')

    def cmd_callback(self, msg): # when received a message from /rasp/cmd
        cmd = msg.data.upper()
        response = String()

        if "NIGHT" in cmd:
            # У рэжыме "ноч": першы пін у 0, другі ў 1
            # Night mode: first output pin = 0, second output pin = 1
            self.pin_day.off()  # 0 
            self.pin_night.on() # 1  
            response.data = "received: night"
            self.get_logger().info('Raspberry Node received: night')
        elif "DAY" in cmd:
            # Day mode: first output pin = 1, second output pin = 0
            self.pin_day.on()    # 1 
            self.pin_night.off() # 0
            response.data = "received: day"
            self.get_logger().info('Raspberry Node received: day')
        
        if response.data:
            self.publisher_.publish(response) # publish response to /rasp/cmd
            self.get_logger().info(f'published to /rasp/cmd: {response.data}')

    def send_input_status(self, input_num, state): # func for sending inputs' states
        msg = String()
        msg.data = f"input_{input_num}: {state}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sensor change: {msg.data}')

    def send_initial_states(self): # func for initial sending of inputs' states
        for i, btn in self.inputs.items():
            state = 1 if btn.is_pressed else 0
            self.send_input_status(i, state)

def main(args=None):
    rclpy.init(args=args)
    node = RaspberryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()


