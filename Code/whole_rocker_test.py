# Import Raspblock drive library
import time
from Raspblock import Raspblock
robot = Raspblock()

power = 4
loop_time = 1000

# # Whole rocker mode control method
# @library function： Speed_axis_Yawhold_control( Speed_axis_X, Speed_axis_Y) （With Self-stabilizing）
# @library function： Speed_axis_control(Speed_axis_X, Speed_axis_Y, Speed_axis_Z)（Outwith Self-stabilizing）
# @
# @Range of speed：
# @X：-25 ~ 25
# @Y: -25 ~ 25
# @Z: 0 ~ 200

# Keep moving for a while
print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # Forward
    robot.Speed_axis_Yawhold_control(0, power)

print(f"End : {time.ctime()}")


# # Reverse
print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # Reverse
    robot.Speed_axis_Yawhold_control(0, -power)

print(f"End : {time.ctime()}")


print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # # Left translation
    robot.Speed_axis_Yawhold_control(-4, 0)

print(f"End : {time.ctime()}")


print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # # Right translation
    robot.Speed_axis_Yawhold_control(4, 0)

print(f"End : {time.ctime()}")


print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # # Upper left
    robot.Speed_axis_Yawhold_control(-4, 4)

print(f"End : {time.ctime()}")



print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # # Upper right
    robot.Speed_axis_Yawhold_control(4, 4)

print(f"End : {time.ctime()}")


print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # # Lower left
    robot.Speed_axis_Yawhold_control(-4, -4)

print(f"End : {time.ctime()}")


print(f"Start : {time.ctime()}")
for i in range(1, loop_time):
    # # Lower right
    robot.Speed_axis_Yawhold_control(4, -4)

print(f"End : {time.ctime()}")
