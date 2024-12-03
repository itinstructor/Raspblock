# Import necessary modules
import time
from Raspblock import Raspblock  # Import Raspblock drive library

# Create an instance of the Raspblock class to control the robot
robot = Raspblock()

# Set the power level for the wheels
power = 4

# Print the start time of the movement
print(f"Start : {time.ctime()}")

# Loop to control the robot's wheel speed
for i in range(1, 4000):
    # Set the speed of all four wheels to the specified power level
    robot.Speed_Wheel_control(power, power, power, power)

# Print the end time of the movement
print(f"End : {time.ctime()}")
