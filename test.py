import wlkatapython
import serial
import time

coordinate_g = [[30 , 0 , 0 , 0 , 0 , 0], 
                [-30 , 0 , 0 , 0 , 0 , 0], 
                [0 , 30 , 0 , 0 , 0 , 0], 
                [0 , -30 , 0 , 0 , 0 , 0], 
                [0,  0,  30,  0,  0,  0], 
                [0 , 0 , -30 , 0 , 0 , 0], 
                [0,  0,  0,  30,  0,  0], 
                [0,  0,  0,  -30,  0,  0], 
                [0 , 0 , 0 , 0 , 30 , 0], 
                [0 , 0 , 0 , 0 , -30 , 0], 
                [0 , 0 , 0 , 0 , 0 , 30], 
                [0 , 0 , 0 , 0 , 0 , -30]]

serial1 = serial.Serial('COM7', 115200)  # Set the serial port and baud rate
mirobot1 = wlkatapython.Wlkata_UART()  # Create object mirobot1
print("Initializing Robot...")

# Initialize the robot
mirobot1.init(serial1, -1)  # Set robotic arm address
print("Robot Initialized.")

# Check the robot state
state = mirobot1.getState()
print(f"Initial Robot State: {state}")

if state == "Alarm":  # If the robotic arm is in the Alarm state, home robotic arm
    print("Entering Homing Process...")
    mirobot1.homing()
    
    # Wait for homing to complete
    time.sleep(2)  # Give the robot time to perform the homing process
    
    # Ensure that the robot is in 'Idle' state after homing
    state = mirobot1.getState()
    print(f"Robot State After Homing: {state}")
    
    # Wait until robot is idle after homing
    while state != "Idle":
        print("Waiting for robot to finish homing...")
        time.sleep(1)  # Wait a bit before checking again
        state = mirobot1.getState()  # Check status again

    print("Homing Complete, Robot is Idle.")

# Now move the robotic arm through the coordinates
for i in range(0, 12): 
    print(f"Moving to position {i + 1}...")
    
    # Wait for the robot to be idle before sending the next command
    while mirobot1.getState() != "Idle": 
        print(f"Robotic Arm Status: {mirobot1.getState()}")
        mirobot1.homing()
        time.sleep(1)  # Wait a bit before checking again

    # Send the move command
    print(f"Sending angle command for position {i + 1}: {coordinate_g[i]}")
    mirobot1.writeangle(0, coordinate_g[i][0], coordinate_g[i][1], coordinate_g[i][2], coordinate_g[i][3], coordinate_g[i][4], coordinate_g[i][5])

# Return robotic arm to initial position
print("Returning robot to initial position...")
mirobot1.zero()

# Close serial port
serial1.close()
print("Serial port closed.")
