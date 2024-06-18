from evdev import InputDevice, categorize, ecodes
from time import sleep

# Import Raspblock drive library
from Raspblock import Raspblock
# Create an instance of the Raspblock class to control the robot
robot = Raspblock()

# Create an InputDevice instance to access the input event device
dev = InputDevice('/dev/input/event0')

# Print the details of the input device
print(dev)

# Initialize variables to store joystick speed values
Speed_axis_X = 0
Speed_axis_Y = 0

# Loop to read events from the input device
for event in dev.read_loop():
    # Check if the event type is an absolute axis event
    if event.type == ecodes.EV_ABS:
        # Categorize the event for easy handling
        event_categorized = categorize(event)
        # print(event_categorized)

        # Check if the event code is for the Y-axis of the left joystick
        if event.code == ecodes.ABS_Y:
            # Normalize the joystick value (0 to 255) to a power level (-25 to 25)
            Speed_axis_Y = int(50 * (event.value / 255)) - 25

        # Check if the event code is for the X-axis of the left joystick
        elif event.code == ecodes.ABS_X:
            # Normalize the joystick value (0 to 255) to a power level (-25 to 25)
            Speed_axis_X = int(50 * (event.value / 255)) - 25

        print(Speed_axis_X, Speed_axis_Y)
        # Control the robot with the calculated speed values
        robot.Speed_axis_Yawhold_control(Speed_axis_X, Speed_axis_Y)

