from time import sleep
# Import Raspblock Drive library
from Raspblock import Raspblock
# Create robot object
robot = Raspblock()

sleep(1)

# buzzer on
robot.Buzzer_control(1)
print("Buzzer on!")

sleep(1)

# buzzer off
robot.Buzzer_control(0)
print("Buzzer off!")

# Delete object after use, otherwise, when the next program needs to
# use this object module, it will be occupied and will become unusable
del robot
