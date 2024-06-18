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

# Loop to read events from the input device
for event in dev.read_loop():
    # Check if the event type is an absolute axis event
    if event.type == ecodes.EV_ABS:
        # Categorize the event for easy handling
        event_categorized = categorize(event)

        # Check if the event code is for the Y-axis of the left joystick
        if event.code == ecodes.ABS_Y:
            # Normalize the joystick value (0 to 255) to a power level (-25 to 25)
            power = int(50 * (event.value / 255)) - 25
            
            print(power)
            
            # Calculate power levels for each wheel based on joystick position
            if power > 127:
                # Moving forward
                front_left = power
                front_right = power
                back_left = power
                back_right = power
            elif power < 127:
                # Moving backward
                front_left = -power
                front_right = -power
                back_left = -power
                back_right = -power
            else:
                # Stop the robot if joystick is in the neutral position
                front_left = 0
                front_right = 0
                back_left = 0
                back_right = 0

            # Control the robot with the calculated power levels
            robot.Speed_Wheel_control(
                front_left, front_right, back_left, back_right
            )

        # Check if the event code is for the X-axis of the left joystick
        elif event.code == ecodes.ABS_X:
            # Handle left/right movement if needed
            pass  # Implement turning logic if required
