import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class DiffDrive(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')

        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)

        self.turning = False
        self.cooling_down = False
        self.min_distance = float('inf')
        self.turn_duration = 1.5
        self.cooldown_duration = 2.0  
        self.turn_timer = None
        self.cooldown_timer = None

    def listener_callback(self, msg):
        
        if self.turning or self.cooling_down:
            return

        scan_center = len(msg.ranges) // 2
        scan_window = msg.ranges[scan_center - 15: scan_center + 15]
        valid_ranges = [r for r in scan_window if 0.1 < r < float('inf')]

        if not valid_ranges:
            self.get_logger().info("No obstacles detected. Moving... :)")
            self.publish_cmd(0.2, 0.0)
            return

        self.min_distance = min(valid_ranges)
        self.get_logger().info(f"Closest obstacle: {self.min_distance:.2f} m")

        if self.min_distance < 3.0:
            self.get_logger().info("Obstacle detected. Starting to turn... :O")
            self.start_turn()
        else:
            self.publish_cmd(0.2, 0.0)
            self.get_logger().info("Path clear. Moving forward... :D")

    def start_turn(self):
        if self.turning:
            return
        self.turning = True
        self.publish_cmd(0.0, 2.0)
        self.turn_timer = self.create_timer(self.turn_duration, self.stop_turn)

    def stop_turn(self):
        if self.turn_timer:
            self.turn_timer.cancel()
            self.turn_timer = None

        self.turning = False
        self.get_logger().info("Finished turning... ;D")
        self.publish_cmd(0.2, 0.0)

        
        self.cooling_down = True
        self.cooldown_timer = self.create_timer(self.cooldown_duration, self.end_cooldown)

    def end_cooldown(self):
        if self.cooldown_timer:
            self.cooldown_timer.cancel()
            self.cooldown_timer = None

        self.cooling_down = False
        self.get_logger().info("Cooldown complete. Resuming normal scan :)")

    def publish_cmd(self, linear_x, angular_z):
        cmd = Twist()
        cmd.linear.x = linear_x
        cmd.angular.z = angular_z
        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    avoider = DiffDrive()
    rclpy.spin(avoider)
    avoider.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
