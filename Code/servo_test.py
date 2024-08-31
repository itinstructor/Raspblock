from time import sleep
# Import Raspblock drive library
from Raspblock import Raspblock
robot = Raspblock()

# Single servo control
# Servo_control_single(index, angle)

# index： S1~S4
# angle：500-2500 -> 0 - 180
# 1500 is straight ahead for camera tower rotation
# robot.Servo_control_single(1, 1500)


# Vertical servo: 500-1950
# 1500 is straight ahead
#robot.Servo_control_single(2, 1500)

# Double servo control
# Servo_control(angle_A, angle_B)

# Horizontal servo: 500-2500
# Vertical servo: 500-1950

# If it exceeds this range, the servo will be damaged
# Horizontal servo 500, vertical servo 1300
robot.Servo_control(500, 1300)
sleep(2)

robot.Servo_control(1500, 1500)

del robot
