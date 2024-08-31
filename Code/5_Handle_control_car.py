# @Copyright (C): 2010-2020, Shenzhen Yahboom Tech
# @Author: Liusen
# @Date: 2020-02-04 15:03:02
# @LastEditors: Liusen
# @LastEditTime: 2020-02-04 15:03:02

# We need to use the simulation mode, press the ANALOG button on the handle to enter the simulation mode. Red light will on.
#
# The slide bars 0-9 represent the analog value, take value method: controller.axes [0] .value = -1.0 ~ 1.0

# +
from Raspblock import Raspblock
import ipywidgets.widgets as widgets
import time

# Thread function operation library
import threading
import inspect
import ctypes
import matplotlib.pyplot as plt


robot = Raspblock()
controller = widgets.Controller(index=0)  # index indicates the serial number
display(controller)  # Display slide bars and boxes of handle


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# Initialize global variables for servo control
global leftrightpulse
leftrightpulse = 1500  # Initial pulse width for left-right control
global updownpulse
updownpulse = 1500  # Initial pulse width for up-down control


def camUpFunction():
    # Function to move the camera up
    global updownpulse
    updownpulse += 10  # Increase the pulse width to move up
    if updownpulse > 2500:  # Limit the maximum pulse width
        updownpulse = 2500
    robot.Servo_control(leftrightpulse, updownpulse)  # Control the servo


def camDownFunction():
    # Function to move the camera down
    global updownpulse
    updownpulse -= 10  # Decrease the pulse width to move down
    if updownpulse < 500:  # Limit the minimum pulse width
        updownpulse = 500
    robot.Servo_control(leftrightpulse, updownpulse)  # Control the servo


def camLeftFunction():
    # Function to move the camera left
    global leftrightpulse
    leftrightpulse += 10  # Increase the pulse width to move left
    if leftrightpulse > 2500:  # Limit the maximum pulse width
        leftrightpulse = 2500
    robot.Servo_control(leftrightpulse, updownpulse)  # Control the servo


def camRightFunction():
    # Function to move the camera right
    global leftrightpulse
    leftrightpulse -= 10  # Decrease the pulse width to move right
    if leftrightpulse < 500:  # Limit the minimum pulse width
        leftrightpulse = 500
    robot.Servo_control(leftrightpulse, updownpulse)  # Control the servo


def camservoInitFunction():
    # Function to initialize the camera servo position
    global leftrightpulse, updownpulse
    leftrightpulse = 1500  # Reset left-right pulse width to initial value
    updownpulse = 1500  # Reset up-down pulse width to initial value
    robot.Servo_control(leftrightpulse, updownpulse)  # Control the servo


def Remote_thread():
    # Initialize speed variables for different axes
    Speed_axis_X = 0
    Speed_axis_Y = 0
    Speed_axis_Z = 0

    # Several counters (count1 to count7) are initialized to manage
    # repeated actions based on the controller inputs.
    count1 = count2 = count3 = count4 = count5 = count6 = count7 = 0

    # Infinite loop to continuously check the controller inputs
    while 1:
        # If the joystick (axes 0 and 1) is moved beyond a threshold,
        # the robot's speed is adjusted accordingly.
        # Check if joystick axes values meet threshold for movement
        if (abs(controller.axes[0].value) >= 0.1 or abs(controller.axes[1].value) >= 0.1):
            count4 += 1

            # Execute control logic only after counting 4 consecutive valid readings
            if count4 >= 4:
                # Calculate speed values from joystick axes
                Speed_axis_X = int(controller.axes[0].value * 15)
                # Invert Y-axis for correct movement direction
                Speed_axis_Y = -int(controller.axes[1].value * 15)

                # Control the robot with calculated speed values
                robot.Speed_axis_Yawhold_control(Speed_axis_X, Speed_axis_Y)
                count4 = 0  # Reset count after executing control logic

        time.sleep(0.01)

        # Button 0 controls the buzzer
        if controller.buttons[0].value == True:
            robot.Buzzer_control(1)
        else:
            robot.Buzzer_control(0)

        # Axis 2 controls camera up and down
        if controller.axes[2].value == 1:
            count1 += 1
            if count1 >= 3:
                camDownFunction()
                count1 = 0
        elif controller.axes[2].value == -1:
            count1 += 1
            if count1 >= 3:
                camUpFunction()
                count1 = 0
        else:
            count1 = 0

        # Axis 5 controls camera left and right
        if controller.axes[5].value == 1:
            count2 += 1
            if count2 >= 3:
                camRightFunction()
                count2 = 0
        elif controller.axes[5].value == -1:
            count2 += 1
            if count2 >= 3:
                camLeftFunction()
                count2 = 0
        else:
            count2 = 0

        # Button 11 resets the camera servos to initial position
        if controller.buttons[11].value == True:
            count3 += 1
            if count3 >= 3:
                camservoInitFunction()
                count3 = 0
        else:
            count3 = 0

        # Button 3 spins the car left, button 1 spins the car right
        if controller.buttons[3].value == True:
            count6 += 1
            if count6 >= 3:
                robot.Speed_axis_control(0, 0, -15)
                count6 = 0
        elif controller.buttons[1].value == True:
            count6 += 1
            if count6 >= 3:
                robot.Speed_axis_control(0, 0, 15)
                count6 = 0
        else:
            count6 = 0

        # Wait for 10 milliseconds before checking inputs again
        time.sleep(0.01)


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


thread = threading.Thread(target=Remote_thread)
thread.setDaemon(True)
thread.start()

stop_thread(thread)
del robot
