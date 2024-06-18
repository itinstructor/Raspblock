import time
from evdev import InputDevice, categorize, ecodes
from time import sleep

from Raspblock import Raspblock  # Import Raspblock drive library

# Create an instance of the Raspblock class to control the robot
robot = Raspblock()

# Define the power level and run time for the robot to move forward
power = 50  # Adjust the power level as needed
run_time = 2  # Time in seconds the robot will move forward

# Create an InputDevice instance to access the input event device
# Replace '/dev/input/event0' with the correct event file for your gamepad
dev = InputDevice('/dev/input/event0')

# Print the details of the input device
print(dev)

print("Waiting for button press to move forward...")

# Loop to read events from the input device
for event in dev.read_loop():
    # Check if the event type is a key press event
    if event.type == ecodes.EV_KEY:
        event_categorized = categorize(event)
        # Check if the button is pressed down (value == 1)
        if event_categorized.keystate == 1:  # 1 means key is pressed down
            
            # You can customize the button code here; 304 is typically the 'A' button on many gamepads
            if event_categorized.scancode == 305: 
                print("Button pressed! Moving forward.")
                # Move the robot forward with specified power
                robot.Speed_Wheel_control(power, power, power, power)
                sleep(run_time)
                # Stop the robot after the run time
                robot.Speed_Wheel_control(0, 0, 0, 0)
                print("Movement complete.")
                input("Press Any key to exit . . .")
                break
