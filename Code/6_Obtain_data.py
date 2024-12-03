#
# @Copyright (C): 2010-2020, Shenzhen Yahboom Tech
# @Author: Liusen
# @Date: 2020-02-06 10:10:02
# @LastEditors: Liusen
# @LastEditTime: 2020-02-06 16:01:19

# Import Raspblock drive library
import serial
import time
import RPi.GPIO as GPIO
from Raspblock import Raspblock
robot = Raspblock()

# ##  Define serial port receiving and opening functions

# Open serial port with specified device and baud rate
ser = serial.Serial("/dev/ttyAMA0", 115200)
# Flush input buffer to clear any existing data
ser.flushInput()

# Define the Attitude_update function


def Attitude_update():
    # Get the number of bytes in the receive buffer
    count = ser.inWaiting()
    # If there are bytes available to read
    if count != 0:
        # Read the bytes from the serial buffer
        recv = list(ser.read(count))
        # Convert the byte list to a string using UTF-8 encoding
        recv = str(bytes(recv), encoding='UTF-8')
        # Check if the received string contains both '{' and '}#'
        if recv.find("{") != -1 and recv.find("}#") != -1:
            # Print the received string (for debugging purposes)
            print(recv)
            # Potential regex for parsing the data (commented out)
            # reg = re.compile('^{A(?P<Pitch>[^ ]*):(?P<Roll>[^ ]*):(?P<Yaw>[^ ]*):(?P<Voltage>[^ ]*)}#')

    # Clear the receive buffer to remove any remaining data
    ser.flushInput()


# -

# # Library API：BoardData_Get(index)
# index:
# Range of index is 0~9.
#
# 0 -- Start Reporting
#
# 1~4 -- Four encoder
#
# 5 -- voltage data
#
# 6 -- Pitch
#
# 7 -- Roll
#
# 8 -- Yaw
#
# 9 -- Stop Reporting
#
while True:
    robot.BoardData_Get(5)  # Get voltage data
    Attitude_update()
    time.sleep(0.5)

del robot  
