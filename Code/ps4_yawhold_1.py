"""
    Name: ps4_yawhold.py
    Author: William A Loring
    Created: 06/17/24
    Purpose: Raspblock remote control with the Y axis held in place
"""


from pyPS4Controller.controller import Controller
# Import Raspblock drive library
from Raspblock import Raspblock
from time import sleep
import threading

# Create an instance of the Raspblock class to control the robot
robot = Raspblock()


class MyController(Controller):
    """Define a custom controller class inheriting from the
       PS4 Controller class"""

    def __init__(self, **kwargs):
        # Initialize the Controller parent class
        super().__init__(**kwargs)

        self.Speed_axis_X = 0  # Initialize X-axis speed value
        self.Speed_axis_Y = 0  # Initialize Y-axis speed value
        self.running = True  # Flag to control the running state of the update thread

        # Create and start a daemon thread for continuous movement updates
        self.update_thread = threading.Thread(
            target=self.update_movement_continuously
        )
        # Set the thread as a daemon, when program exits, the thread stops
        self.update_thread.daemon = True
        # Start the thread
        self.update_thread.start()

    # Event handler for moving the left joystick up
    def on_L3_up(self, value):
        self.update_y_axis(value)

    # Event handler for moving the left joystick down
    def on_L3_down(self, value):
        self.update_y_axis(value)

    # Event handler for moving the left joystick left
    def on_L3_left(self, value):
        self.update_x_axis(value)

    # Event handler for moving the left joystick right
    def on_L3_right(self, value):
        self.update_x_axis(value)

    # Update the Y-axis speed based on joystick value
    def update_y_axis(self, value):
        # Normalize the joystick value (32767 to -32767) to a power level (-25 to 25)
        self.Speed_axis_Y = int(50 * ((-value + 32767) / 65534)) - 25

    # Update the X-axis speed based on joystick value
    def update_x_axis(self, value):
        # Normalize the joystick value (-32767 to 32767) to a power level (-25 to 25)
        self.Speed_axis_X = int(50 * ((value + 32767) / 65534)) - 25

    # Continuously update the movement of the robot
    def update_movement_continuously(self):
        while True:
            self.update_movement()
            sleep(0.1)  # Adjust the sleep time as needed for smooth control

    # Update the robot's movement based on the current speed values
    def update_movement(self):
        # Prevent minor joystick movements from causing unintended actions
        if -2 < self.Speed_axis_X < 2:
            self.Speed_axis_X = 0
        if -2 < self.Speed_axis_Y < 2:
            self.Speed_axis_Y = 0

        # Print for debugging purposes
        # print(f"Speed_axis_X: {self.Speed_axis_X}, Speed_axis_Y: {self.Speed_axis_Y}")

        # Control the robot with the calculated speed values
        robot.Speed_axis_Yawhold_control(self.Speed_axis_X, self.Speed_axis_Y)


# Create an instance of MyController, connecting to the correct interface
# for the joystick
controller = MyController(
    interface="/dev/input/js0",
    connecting_using_ds4drv=False
)

try:
    # Listen for events from the controller for 60 seconds
    controller.listen(timeout=60)
except KeyboardInterrupt:
    # Handle program interruption (e.g., Ctrl+C)
    print("Program interrupted by the user")
finally:
    print("Controller stopped and program exited cleanly")
