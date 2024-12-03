# Import Raspblock drive library
from time import sleep
from Raspblock import Raspblock
robot = Raspblock()

run_time = 1
power = 4
# # Single wheel control
# @library function：Speed_Wheel_control(Speed_WheelA, Speed_WheelB, Speed_WheelC, Speed_WheelD)
# @range of speed：-25 ~ 25

# Control wheel individually
# robot.Speed_Wheel_control(4, 0, 0, 0)
# sleep(run_time)
# input("Press Any key . . .")

# All wheel forward with 2 speed
robot.Speed_Wheel_control(power, power, power, power)
sleep(run_time)
input("Press Any key . . .")

# All wheel reserve with 2 speed
robot.Speed_Wheel_control(-power, -power, -power, -power)
sleep(run_time)
input("Press Any key . . .")

# Spin left
robot.Speed_Wheel_control(power, power, -power, -power)
sleep(run_time)
input("Press Any key . . .")

# Spin right
robot.Speed_Wheel_control(-power, -power, power, power)
sleep(run_time)
input("Press Any key . . .")

# Left translation
robot.Speed_Wheel_control(power, -power, power, -power)
sleep(run_time)
input("Press Any key . . .")

# Right translation
robot.Speed_Wheel_control(-power, power, -power, power)
sleep(run_time)
input("Press Any key . . .")

# Stop
robot.Speed_Wheel_control(0, 0, 0, 0)
sleep(run_time)
input("Press Any key . . .")

# Keep moving for a while
# print("Start : %s" % time.ctime())
# for i in range(1, 4000):
#     robot.Speed_Wheel_control(2, 2, 2, 2)
# print("End : %s" % time.ctime())

# # # Whole rocker mode control method
# # @library function： Speed_axis_Yawhold_control( Speed_axis_X, Speed_axis_Y) （With Self-stabilizing）
# # @library function： Speed_axis_control(Speed_axis_X, Speed_axis_Y, Speed_axis_Z)（Outwith Self-stabilizing）
# # @
# # @Range of speed：
# # @X：-25 ~ 25
# # @Y: -25 ~ 25
# # @Z: 0 ~ 200

# # Forward
# robot.Speed_axis_Yawhold_control(0, 4)

# # Reverse
# robot.Speed_axis_Yawhold_control(0, -4)

# # Left translation
# robot.Speed_axis_Yawhold_control(-4, 0)

# # Right translation
# robot.Speed_axis_Yawhold_control(4, 0)

# # Upper left
# robot.Speed_axis_Yawhold_control(-4, 4)

# # Upper right
# robot.Speed_axis_Yawhold_control(4, 4)

# # Lower left
# robot.Speed_axis_Yawhold_control(-4, -4)

# # Lower right
# robot.Speed_axis_Yawhold_control(4, -4)

# Square translation
# Spin right
robot.Speed_Wheel_control(-8, -8, 8, 8)

# All wheel reserve with 2 speed
robot.Speed_Wheel_control(-8, -8, -8, -8)

# Spin left
robot.Speed_Wheel_control(8, 8, -8, -8)

# All wheel forward with 2 speed
robot.Speed_Wheel_control(8, 8, 8, 8)


# Surround mode
# @Library function：Speed_Wheel_control(Speed_WheelA, Speed_WheelB, Speed_WheelC, Speed_WheelD)
# Front of car
# @Range of speed:-25 ~ 25
# AD slow speed, BC fast speed to achieve the effect of surround mode

# Right surround mode
robot.Speed_Wheel_control(-8, -15, 15, 8)
sleep(1)

# Left surround mode
robot.Speed_Wheel_control(8, 15, -15, -8)
sleep(1)

del robot    
