#
# @Copyright (C): 2010-2020, Shenzhen Yahboom Tech
# @Author: Liusen
# @Date: 2020-02-03 16:03:02
# @LastEditors: Liusen
# @LastEditTime: 2020-02-04 14:03:02

# 1.Handle key test
# First of all, we open the http://html5gamepad.com webpage, and connect your Handle to your computer.
# Because maybe your PC computer can not only connect a handle,
# so the default value of the index of the handle you connect is not 0,
# so we need to go to this page to view the handle we are currently using.
# The index can be used correctly.

# Import widgets compennt
import matplotlib.pyplot as plt
import ctypes
import inspect
import threading
import time
from Raspblock import Raspblock
import ipywidgets.widgets as widgets

# index indicates the serial number of the handle we use
controller = widgets.Controller(index=0)
display(controller)                       # Display slide bars and boxes

# 2.It is recommended to end the task before running the following program,
# and then restart the kernel to run the following program.
#   
#    It is recommended that we use the simulation mode, press the ANALOG button on the handle to enter the simulation mode. Red light will on.
#
# The slide bars 0-9 represent the analog value, take value method: controller.axes [0] .value = -1.0 ~ 1.0
# The boxes 0-11 Bool represent the value of the keys, take Value method: controller.buttons [0] .value = True / False

# +

# Thread function operation library


robot = Raspblock()
# index indicates the serial number of the handle we use
controller = widgets.Controller(index=0)
display(controller)  # Display slide bars and boxes of Handle


# Define the _async_raise function

def _async_raise(tid, exctype):
    """Raises an exception in the thread with id tid."""
    # Convert thread id to a C long type
    tid = ctypes.c_long(tid)
    # Ensure exctype is a class (exception type)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    # Call Python C API function to raise the exception in the thread
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    # If the result is 0, the thread id is invalid
    if res == 0:
        raise ValueError("invalid thread id")
    # If the result is not 1, revert the effect by calling it again with None
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)


def stop_thread(thread):
    """Define the stop_thread function to stop a given thread"""
    # Call _async_raise to raise a SystemExit exception in the thread
    _async_raise(thread.ident, SystemExit)


# Define the Remote_thread function
def Remote_thread():
    # Infinite loop to continuously check the controller buttons
    while True:
        # If the first button on the controller is pressed
        if controller.buttons[0].value == True:
            # Turn on the robot's buzzer
            robot.Buzzer_control(1)
        else:
            # Otherwise, turn off the robot's buzzer
            robot.Buzzer_control(0)
        # Wait for 10 milliseconds before checking again
        time.sleep(0.01)


# Define the stop_thread function to stop a given thread
def stop_thread(thread):
    # Raise a SystemExit exception in the thread to stop it
    _async_raise(thread.ident, SystemExit)


thread = threading.Thread(target=Remote_thread)
thread.setDaemon(True)
thread.start()

# # When we need to end the entire program process, we need to run this code

stop_thread(thread)
del robot
