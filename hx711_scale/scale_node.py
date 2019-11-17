#!/usr/bin/env python3
import atexit

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32, Bool

import RPi.GPIO as GPIO
from hx711 import HX711


class ScaleNode(Node):
    NUM_SAMPLES = 5

    def __init__(self, dout=5, pd_sck=6):
        super().__init__('scale_node')

        self.declare_parameter('reference_unit', 386.619)
        self._reference_unit = self.get_parameter('reference_unit').value
        self.declare_parameter('update_interval_s', 0.1)
        self._update_interval_s = self.get_parameter('update_interval_s').value

        self._hx = HX711(dout, pd_sck)
        self._hx.set_reading_format("MSB", "MSB")
        self._hx.set_reference_unit(self._reference_unit)

        self._subs = []
        self._subs.append(
            self.create_subscription(Bool, 'scale/enable', self._enable_callback, 1)
        )
        self._value_pub = self.create_publisher(Float32, 'scale/value', 10)
        self._timer = self.create_timer(self._update_interval_s, self._timer_callback)
        self._timer.cancel()

    def _enable_callback(self, msg):
        enable = msg.data
        if enable:
            self._hx.reset()
            self._hx.tare()
            self.get_logger().info('Tare done. Ready to add weight.')
            self._timer.reset()
        else:
            self._hx.power_down()
            self.get_logger().info('Scale disabled.')
            self._timer.cancel()

    def _timer_callback(self):
        self._measure()

    def _measure(self):
        value = self._hx.get_weight(self.NUM_SAMPLES)
        self._value_pub.publish(Float32(data=value))
        self.get_logger().debug('New measurement {}'.format(value))


def main(args=None):
    atexit.register(GPIO.cleanup)
    rclpy.init(args=args)

    node = ScaleNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
