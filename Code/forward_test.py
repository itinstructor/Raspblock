# Import Raspblock drive library
import time
from Raspblock import Raspblock
robot = Raspblock()

power = 4

# Keep moving for a while
print(f"Start : {time.ctime()}")
for i in range(1, 4000):
    robot.Speed_Wheel_control(power, power, power, power)

print(f"End : {time.ctime()}")
