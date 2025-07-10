import wlkatapython
import serial
import time

"Robot arm returns to zero"
Serial1=serial.Serial ("COM7", 115200) # Set serial port and baud rate
Mirobot1=wlkatapython.Mirobot_UART() # Create a new mirobot1 object
Mirobot1.init (Serial1, -1) # Set the address of the robotic arm
Mirobot1.homing() # Robot arm zeroing
Serial1.close() # Close serial port