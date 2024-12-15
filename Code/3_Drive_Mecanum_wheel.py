# Import Raspblock drive library
import time
from Raspblock import Raspblock
robot = Raspblock()

# # Single wheel control
#
# @library function：Speed_Wheel_control(Speed_WheelA, Speed_WheelB, Speed_WheelC, Speed_WheelD)
# @range of speed：-25 ~ 25
#

# Control wheel individually
robot.Speed_Wheel_control(4, 0, 0, 0)

# All wheel forward with 2 speed
robot.Speed_Wheel_control(2, 2, 2, 2)

# %%
robot.Speed_Wheel_control(-2, -2, -2, -2)  # All wheel reserve with 2 speed

# %%
robot.Speed_Wheel_control(2, 2, -2, -2)  # Spin left

# %%
robot.Speed_Wheel_control(-1, -1, 1, 1)  # Spin right

# %%
robot.Speed_Wheel_control(2, -2, 2, -2)  # Left translation

# %%
robot.Speed_Wheel_control(-2, 2, -2, 2)  # Right translation

# %%
robot.Speed_Wheel_control(0, 0, 0, 0)  # All wheel stop

# %%
# Keep moving for a while
print("Start : %s" % time.ctime())
for i in range(1, 4000):
    robot.Speed_Wheel_control(2, 2, 2, 2)
print("End : %s" % time.ctime())

# %% [markdown]
# # Whole rocker mode control method
#
# @library function： Speed_axis_Yawhold_control( Speed_axis_X, Speed_axis_Y) （With Self-stabilizing）
# @library function： Speed_axis_control(Speed_axis_X, Speed_axis_Y, Speed_axis_Z)（Outwith Self-stabilizing）
# @
# @Range of speed：
# @X：-25 ~ 25
# @Y: -25 ~ 25
# @Z: 0 ~ 200

# %%
robot.Speed_axis_Yawhold_control(0, 4)  # Advance

# %%
robot.Speed_axis_Yawhold_control(0, -4)  # Back

# %%
robot.Speed_axis_Yawhold_control(-4, 0)  # Left translation

# %%
robot.Speed_axis_Yawhold_control(4, 0)  # Right translation

# %%
robot.Speed_axis_Yawhold_control(-4, 4)  # Upper left

# %%
robot.Speed_axis_Yawhold_control(4, 4)  # Upper right

# %%
robot.Speed_axis_Yawhold_control(-4, -4)  # Lower left

# %%
robot.Speed_axis_Yawhold_control(4, -4)  # Lower right

# %% [markdown]
# # Square translation
#

# %%

robot.Speed_Wheel_control(-8, -8, 8, 8)  # Spin right
time.sleep(1)
robot.Speed_Wheel_control(-8, -8, -8, -8)  # All wheel reserve with 2 speed
time.sleep(1)
robot.Speed_Wheel_control(8, 8, -8, -8)  # Spin left
time.sleep(1)
robot.Speed_Wheel_control(8, 8, 8, 8)  # All wheel forward with 2 speed
time.sleep(1)

# %% [markdown]
# # Surround mode

# %% [markdown]
# @Library function：Speed_Wheel_control(Speed_WheelA, Speed_WheelB, Speed_WheelC, Speed_WheelD)
# @&ensp;&ensp;&ensp;Front of car
# @&ensp;|D&ensp;&ensp;&ensp;&ensp;&ensp;A|
# @&ensp;|C&ensp;&ensp;&ensp;&ensp;&ensp;B|
# @Range of speed:-25 ~ 25
#
# AD slow speed, BC fast speed to achieve the effect of surround mode

# %%

robot.Speed_Wheel_control(-8, -15, 15, 8)  # Right surround mode
time.sleep(5)


robot.Speed_Wheel_control(8, 15, -15, -8)    # Left surround mode
time.sleep(5)


# %%
del robot    # The object needs to be released after use, otherwise, when the next program needs to use this object module, it will be occupied and will become unusable
