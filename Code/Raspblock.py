# -*- coding:utf-8 -*
import RPi.GPIO as GPIO
import serial

# Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)


class Raspblock():
    def __init__(self):
        # Open a serial connection with the specified parameters
        self.ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.001)
        print("Robot started!")

    # Destructor method for cleaning up resources
    def __del__(self):
        # Close the serial connection
        self.ser.close()
        print("Robot stopped!")

# ----------------------- PID MODE CONTROL ------------------------------- #
    def PID_Mode_control(self, Mode, Speed_KP, Speed_KI, Location_KP, Location_KI, Location_KD, Yaw_holdKP, Yaw_holdKI, Yaw_holdKD):
        """PID_Mode_control method with parameters for various PID control settings"""
        Function = 1  # Set the function code for PID control to 1
        Length = 9  # Set the length of the command data to 9 bytes

        # Set the run mode if it is either 0 or 1 (valid modes)
        if (Mode == 0 or Mode == 1):
            Run_Mode = Mode

        # Assign PID parameters to local variables
        Velocity_KP = Speed_KP  # Proportional gain for velocity control
        Velocity_KI = Speed_KI  # Integral gain for velocity control
        Position_KP = Location_KP  # Proportional gain for position control
        Position_KI = Location_KI  # Integral gain for position control
        Position_KD = Location_KD  # Derivative gain for position control
        Yaw_hold_KP = Yaw_holdKP  # Proportional gain for yaw hold control
        Yaw_hold_KI = Yaw_holdKI  # Integral gain for yaw hold control
        Yaw_hold_KD = Yaw_holdKD  # Derivative gain for yaw hold control

        # Calculate the checksum for error detection
        # The checksum is the lower 8 bits of the sum of all the command bytes
        Checknum = (Function + Length + Run_Mode + Velocity_KP + Velocity_KI + Position_KP +
                    Position_KI + Position_KD + Yaw_holdKP + Yaw_holdKI + Yaw_holdKD) & 0xff

        # Create the command byte array
        # The command consists of a start sequence (0xFF, 0xFE), function code, length,
        # the PID parameters, and the checksum for verification
        PID_CMD = [0xFF, 0xFE, Function, Length, Run_Mode, Velocity_KP, Velocity_KI,
                   Position_KP, Position_KI, Position_KD, Yaw_holdKP, Yaw_holdKI, Yaw_holdKD, Checknum]

        # Write the command byte array to the serial port
        # This sends the PID control settings to the robot
        self.ser.write(bytes(PID_CMD))

# -------------------------- SERVO CONTROL ------------------------------- #
    def Servo_control(self, angle_1, angle_2):
        """Servo_control method to control two servos"""
        Function = 2  # Set the function code for servo control to 2
        Length = 4  # Set the length of the command data to 4 bytes

        # Ensure angle_1 is within the valid range (500 to 2500)
        if angle_1 < 500:
            angle_1 = 500
        elif angle_1 > 2500:
            angle_1 = 2500

        # Ensure angle_2 is within the valid range (500 to 1950)
        if angle_2 < 500:
            angle_2 = 500
        elif angle_2 > 1950:
            angle_2 = 1950

        # Extract the high and low bytes of angle_1
        ServoA_H = (angle_1 >> 8) & 0x00ff  # High byte of angle_1
        ServoA_L = angle_1 & 0x00ff  # Low byte of angle_1

        # Extract the high and low bytes of angle_2
        ServoB_H = (angle_2 >> 8) & 0x00ff  # High byte of angle_2
        ServoB_L = angle_2 & 0x00ff  # Low byte of angle_2

        # Calculate the checksum for error detection
        # The checksum is the lower 8 bits of the sum of all the command bytes
        Checknum = (Function + Length + ServoA_H +
                    ServoA_L + ServoB_H + ServoB_L) & 0xff

        # Create the command byte array
        # The command consists of a start sequence (0xFF, 0xFE), function code, length,
        # the high and low bytes of the servo angles, and the checksum for verification
        Servo_CMD = [0xFF, 0xFE, Function, Length, ServoA_H,
                     ServoA_L, ServoB_H, ServoB_L, Checknum]

        # Write the command byte array to the serial port
        # This sends the servo control settings to the robot
        self.ser.write(bytes(Servo_CMD))

# ----------------------- SPEED AXIS CONTROL ----------------------------- #
    def Speed_axis_control(self, Speed_axis_X, Speed_axis_Y, Speed_axis_Z):
        """Control the speed along three axes"""
        Function = 3  # Set the function code for speed control to 3
        Length = 8  # Set the length of the command data to 8 bytes
        Speed_axis_Mode = 0x01  # Set the speed control mode

        # Extract the high and low bytes of the absolute value of Speed_axis_X
        # High byte of Speed_axis_X
        Speed_axis_XH = (abs(Speed_axis_X) >> 8) & 0xff
        Speed_axis_XL = abs(Speed_axis_X) & 0xff  # Low byte of Speed_axis_X

        # Extract the high and low bytes of the absolute value of Speed_axis_Y
        # High byte of Speed_axis_Y
        Speed_axis_YH = (abs(Speed_axis_Y) >> 8) & 0xff
        # Low byte of Speed_axis_Y
        Speed_axis_YL = abs(Speed_axis_Y) & 0xff

        # Extract the high and low bytes of the absolute value of Speed_axis_Z
        # High byte of Speed_axis_Z
        Speed_axis_ZH = (abs(Speed_axis_Z) >> 8) & 0xff
        # Low byte of Speed_axis_Z
        Speed_axis_ZL = abs(Speed_axis_Z) & 0xff

        # Determine the direction of movement for each axis
        # 0 means positive movement, 1 means negative movement
        if Speed_axis_X < 0:
            axis_X_direction = 1
        else:
            axis_X_direction = 0

        if Speed_axis_Y < 0:
            axis_Y_direction = 1
        else:
            axis_Y_direction = 0

        if Speed_axis_Z < 0:
            axis_Z_direction = 0  # Corrected to 1 to match the comment
        else:
            axis_Z_direction = 1

        # Determine the direction bits for each axis
        # Shift left to place bit in correct position
        Speed_axis_X_direction = axis_X_direction << 2
        # Shift left to place bit in correct position
        Speed_axis_Y_direction = axis_Y_direction << 1
        Speed_axis_Z_direction = axis_Z_direction  # No shift needed

        # Combine the direction bits into a single byte
        Speed_axis_direction = Speed_axis_X_direction | Speed_axis_Y_direction | Speed_axis_Z_direction

        # Calculate the checksum for error detection
        # The checksum is the lower 8 bits of the sum of all the command bytes
        Checknum = (Function + Length + Speed_axis_Mode + Speed_axis_XH + Speed_axis_XL +
                    Speed_axis_YH + Speed_axis_YL + Speed_axis_ZH + Speed_axis_ZL + Speed_axis_direction) & 0xff

        # Create the command byte array
        # The command consists of a start sequence (0xFF, 0xFE), function code, length,
        # mode, the high and low bytes of the speed values for each axis, the direction byte, and the checksum
        Speed_Motion_CMD1 = [0xFF, 0xFE, Function, Length, Speed_axis_Mode, Speed_axis_XH, Speed_axis_XL,
                             Speed_axis_YH, Speed_axis_YL, Speed_axis_ZH, Speed_axis_ZL, Speed_axis_direction, Checknum]

        # Write the command byte array to the serial port
        # This sends the speed control settings to the robot
        self.ser.write(bytes(Speed_Motion_CMD1))

# --------------- SPEED AXIS YAWHOLD CONTROL ----------------------------- #
    def Speed_axis_Yawhold_control(self, Speed_axis_X, Speed_axis_Y):
        """Control the speed along X and Y axes while holding yaw"""
        Function = 3  # Set the function code for speed control to 3
        Length = 8  # Set the length of the command data to 8 bytes
        Speed_axis_Mode = 0x03  # Set the speed control mode with yaw hold

        # Extract the high and low bytes of the absolute value of Speed_axis_X
        # High byte of Speed_axis_X
        Speed_axis_XH = (abs(Speed_axis_X) >> 8) & 0xff
        Speed_axis_XL = abs(Speed_axis_X) & 0xff  # Low byte of Speed_axis_X

        # Extract the high and low bytes of the absolute value of Speed_axis_Y
        # High byte of Speed_axis_Y
        Speed_axis_YH = (abs(Speed_axis_Y) >> 8) & 0xff
        Speed_axis_YL = abs(Speed_axis_Y) & 0xff  # Low byte of Speed_axis_Y

        # Determine the direction of movement for each axis
        # 0 means positive movement, 1 means negative movement
        if Speed_axis_X < 0:
            axis_X_direction = 1
        else:
            axis_X_direction = 0

        if Speed_axis_Y < 0:
            axis_Y_direction = 1
        else:
            axis_Y_direction = 0

        # Determine the direction bits for each axis
        # Shift left to place bit in correct position
        Speed_axis_X_direction = axis_X_direction << 2
        # Shift left to place bit in correct position
        Speed_axis_Y_direction = axis_Y_direction << 1

        # Combine the direction bits into a single byte
        Speed_axis_direction = Speed_axis_X_direction | Speed_axis_Y_direction

        # Calculate the checksum for error detection
        # The checksum is the lower 8 bits of the sum of all the command bytes
        Checknum = (Function + Length + Speed_axis_Mode + Speed_axis_XH + Speed_axis_XL +
                    Speed_axis_YH + Speed_axis_YL + Speed_axis_direction) & 0xff

        # Create the command byte array
        # The command consists of a start sequence (0xFF, 0xFE), function code, length,
        # mode, the high and low bytes of the speed values for each axis, padding for Z axis, the direction byte, and the checksum
        Speed_Motion_CMD1 = [0xFF, 0xFE, Function, Length, Speed_axis_Mode, Speed_axis_XH,
                             Speed_axis_XL, Speed_axis_YH, Speed_axis_YL, 0, 0, Speed_axis_direction, Checknum]

        # Write the command byte array to the serial port
        # This sends the speed control settings to the robot
        self.ser.write(bytes(Speed_Motion_CMD1))

# ----------------------- SPEED WHEEL CONTROL ---------------------------- #
    def Speed_Wheel_control(self, Speed_WheelA, Speed_WheelB, Speed_WheelC, Speed_WheelD):
        """control the speed of four wheels"""
        Function = 3  # Set the function code for wheel speed control to 3
        Length = 8  # Set the length of the command data to 8 bytes
        Speed_Wheel_Mode = 0x02  # Set the wheel speed control mode

        # Get the absolute values of the speed for each wheel
        # and ensure they fit in one byte (0-255)
        Speed_Wheel_A = abs(Speed_WheelA) & 0xff  # Speed for wheel A
        Speed_Wheel_B = abs(Speed_WheelB) & 0xff  # Speed for wheel B
        Speed_Wheel_C = abs(Speed_WheelC) & 0xff  # Speed for wheel C
        Speed_Wheel_D = abs(Speed_WheelD) & 0xff  # Speed for wheel D

        # Reserved bytes for future use or padding
        Speed_Wheel_Reserved1 = 0x00
        Speed_Wheel_Reserved2 = 0x00

        # Determine the direction of rotation for each wheel
        # 0 means forward rotation, 1 means reverse rotation
        if Speed_WheelA < 0:
            Wheel_A_direction = 1
        else:
            Wheel_A_direction = 0

        if Speed_WheelB < 0:
            Wheel_B_direction = 1
        else:
            Wheel_B_direction = 0

        if Speed_WheelC < 0:
            Wheel_C_direction = 1
        else:
            Wheel_C_direction = 0

        if Speed_WheelD < 0:
            Wheel_D_direction = 1
        else:
            Wheel_D_direction = 0

        # Combine the direction bits into a single byte
        Speed_Wheel_A_direction = Wheel_A_direction << 0  # No shift needed
        Speed_Wheel_B_direction = Wheel_B_direction << 1  # Shift left by 1 bit
        Speed_Wheel_C_direction = Wheel_C_direction << 2  # Shift left by 2 bits
        Speed_Wheel_D_direction = Wheel_D_direction << 3  # Shift left by 3 bits

        Speed_wheel_direction = (
            Speed_Wheel_A_direction |
            Speed_Wheel_B_direction |
            Speed_Wheel_C_direction |
            Speed_Wheel_D_direction
        )

        # Calculate the checksum for error detection
        # The checksum is the lower 8 bits of the sum of all the command bytes
        Checknum = (
            Function + Length + Speed_Wheel_Mode + Speed_Wheel_A +
            Speed_Wheel_B + Speed_Wheel_C + Speed_Wheel_D + Speed_wheel_direction) & 0xff

        # Create the command byte array
        # The command consists of a start sequence (0xFF, 0xFE),
        # function code, length, mode, the speed values for each wheel,
        # reserved bytes, the direction byte, and the checksum
        Speed_Motion_CMD2 = [
            0xFF, 0xFE, Function, Length, Speed_Wheel_Mode, Speed_Wheel_A,
            Speed_Wheel_B, Speed_Wheel_C, Speed_Wheel_D, Speed_Wheel_Reserved1,
            Speed_Wheel_Reserved2, Speed_wheel_direction, Checknum]

        # Write the command byte array to the serial port
        # This sends the speed control settings to the robot
        self.ser.write(bytes(Speed_Motion_CMD2))

# ----------------------- POSITION DISP CONTROL -------------------------- #
    def Position_disp_control(self, Position_disp_X, Position_disp_Y, Position_disp_Z):
        """Control the position displacement along X, Y, and Z axes"""
        Function = 3  # Set the function code for position control to 3
        Length = 8  # Set the length of the command data to 8 bytes
        Position_disp_Mode = 0x04  # Set the mode for position displacement control

        # Extract the high and low bytes of the absolute value of Position_disp_X
        # High byte of Position_disp_X
        Position_disp_XH = (abs(Position_disp_X) >> 8) & 0x00ff
        # Low byte of Position_disp_X
        Position_disp_XL = abs(Position_disp_X) & 0x00ff

        # Extract the high and low bytes of the absolute value of Position_disp_Y
        # High byte of Position_disp_Y
        Position_disp_YH = (abs(Position_disp_Y) >> 8) & 0x00ff
        # Low byte of Position_disp_Y
        Position_disp_YL = abs(Position_disp_Y) & 0x00ff

        # Extract the high and low bytes of the absolute value of Position_disp_Z
        # High byte of Position_disp_Z
        Position_disp_ZH = (abs(Position_disp_Z) >> 8) & 0x00ff
        # Low byte of Position_disp_Z
        Position_disp_ZL = abs(Position_disp_Z) & 0x00ff

        # Determine the direction of movement for each axis
        # 0 means positive movement, 1 means negative movement
        if Position_disp_X < 0:
            Position_disp_X_direction = 0
        else:
            Position_disp_X_direction = 1

        if Position_disp_Y < 0:
            Position_disp_Y_direction = 0
        else:
            Position_disp_Y_direction = 1

        if Position_disp_Z < 0:
            Position_disp_Z_direction = 0
        else:
            Position_disp_Z_direction = 1

        # Set direction bits for each axis
        # 0 means positive movement, shifted by 0 bits for X axis
        Position_disp_X_direction = Position_disp_X_direction << 0
        # 0 means positive movement, shifted by 1 bit for Y axis
        Position_disp_Y_direction = Position_disp_Y_direction << 1
        # 0 means positive movement, shifted by 2 bits for Z axis
        Position_disp_Z_direction = Position_disp_Z_direction << 2

        # Combine the direction bits into a single byte
        Position_disp_direction = (
            Position_disp_X_direction |
            Position_disp_Y_direction
            |
            Position_disp_Z_direction)

        # Calculate the checksum for error detection
        # The checksum is the lower 8 bits of the sum of all the command bytes
        Checknum = (Function + Length + Position_disp_Mode + Position_disp_XH + Position_disp_XL +
                    Position_disp_YH + Position_disp_YL + Position_disp_ZH + Position_disp_ZL +
                    Position_disp_direction) & 0xff

        # Create the command byte array
        # The command consists of a start sequence (0xFF, 0xFE), function code, length,
        # mode, the high and low bytes of the position values for each axis, the direction byte, and the checksum
        Position_Motion_CMD = [
            0xFF, 0xFE, Function, Length, Position_disp_Mode, Position_disp_XH, Position_disp_XL,
            Position_disp_YH, Position_disp_YL, Position_disp_ZH, Position_disp_ZL, Position_disp_direction, Checknum]

        # Write the command byte array to the serial port
        # This sends the position control settings to the robot
        self.ser.write(bytes(Position_Motion_CMD))

# ----------------------------- BUZZER CONTROL --------------------------- #
    def Buzzer_control(self, switch_state):
        """Control the state of the buzzer"""
        Function = 4  # Set the function code for buzzer control to 4
        Length = 1  # Set the length of the command data to 1 byte

        # Check if the switch state is valid (0 for off, 1 for on)
        if switch_state == 0 or switch_state == 1:
            # Calculate the checksum for error detection
            # The checksum is the lower 8 bits of the sum of the function
            # code, length, and switch state
            Checknum = (Function + Length + switch_state) & 0xff

            # Create the command byte array
            # The command consists of a start sequence (0xFF, 0xFE), 
            # function code, length, switch state, and checksum
            Buzzer_CMD = [0xFF, 0xFE, Function, Length, switch_state, Checknum]

            # Write the command byte array to the serial port
            # This sends the buzzer control settings to the robot
            self.ser.write(bytes(Buzzer_CMD))

# ----------------------------- BOARD INFO ------------------------------- #
    def BoardData_Get(self, index):
        Function = 5  # Function code for the command
        Length = 1  # Length of the data to be read

        # Computes a checksum by summing Function, Length, and index,
        # then performing a bitwise AND with 0xff
        # to ensure the result is a single byte.
        Checknum = (Function + Length + index) & 0xff

        # Creates a list of bytes to send, beginning with 0xFF and 0xFE
        # as header bytes, followed by Function, Length, index,
        # and the checksum Checknum.
        BoardData_CMD = [0xFF, 0xFE, Function, Length,
                         index, Checknum]
        # Converts the command list to a bytes object
        # and writes it to the serial port.
        self.ser.write(bytes(BoardData_CMD))
