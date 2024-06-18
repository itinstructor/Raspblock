from evdev import InputDevice, categorize, ecodes
from time import sleep
from sys import exit

# Import Raspblock drive library
from Raspblock import Raspblock
# Create an instance of the Raspblock class to control the robot
robot = Raspblock()

# Create an InputDevice instance to access the input event device
dev = InputDevice('/dev/input/event0')

# Print the details of the input device
print(dev)

# Initialize variables to store joystick speed values
speed_axis_x = 0
speed_axis_y = 0


while True:
    # Loop to read events from the input device
    try:
        # Read a single event
        event = dev.read_one()

        # Check if there is an event code
        if event is not None:
            # If the event code is a joystick
            if event.type == ecodes.EV_ABS:

                # Categorize the event for easy handling
                event_categorized = categorize(event)
                # print(event_categorized)

                # Check if the event code is for the X-axis of the left joystick
                if event.code == ecodes.ABS_X:
                    # Normalize the joystick value (0 to 255) to a power level (-25 to 25)
                    speed_axis_x = int(50 * (event.value / 255)) - 25

                # Check if the event code is for the Y-axis of the left joystick
                elif event.code == ecodes.ABS_Y:
                    # Normalize the joystick value (0 to 255) to a power level (-25 to 25)
                    speed_axis_y = int(50 * (event.value / 255)) - 25

                # Keep joystick creep from making the robot move
                if abs(speed_axis_x) <= 1:
                    speed_axis_x = 0
                if abs(speed_axis_y) <= 1:
                    speed_axis_y = 0

        print(speed_axis_x, speed_axis_y)

        # Control the robot with the calculated speed values
        robot.Speed_axis_Yawhold_control(speed_axis_x, speed_axis_y)

        # Debounce control
        sleep(.1)

    except KeyboardInterrupt:
        del robot
        exit()
