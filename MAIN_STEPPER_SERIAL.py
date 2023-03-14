import pygame
import serial
import sys
import time
from TARSlib import *

# Define the serial port and baud rate
ser = serial.Serial('COM3', 2000000)
fps = 180
time.sleep(3)

# Initialize Pygame
pygame.init()
pygame.joystick.init()

#defining the simulation clock
# clock = pygame.time.Clock()

# Check how many joysticks are connected
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks found.")
    pygame.quit()
    sys.exit()

# Find the Xbox 360 controller
xbox_360_controller = None
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    if joystick.get_name() == 'Xbox 360 Controller':
        xbox_360_controller = joystick
        break

if xbox_360_controller is None:
    print("Xbox 360 controller not found.")
    pygame.quit()
    sys.exit()

# Define the range of the joystick input
JOYSTICK_RANGE = 32767
ite=0
sumdt=0
# Loop until the user quits
while True:
    # Handle events
    tickabs = time.time_ns()
    tick = time.time_ns()
    ser.flushInput()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the current joystick input
    x_axis = xbox_360_controller.get_axis(0)
    # Map the joystick input to the angle range [-180, 180]
    if -0.1 < x_axis < 0.1:
        target_angle = 91
    else:
        target_angle = int(x_axis * 90 + 91)

        # Send the target angle through the serial connection
    target_angle_bytes = bytes(str(target_angle) + '\n', 'utf-8')
    ser.write(target_angle_bytes)

    # Send the target angle through the serial connection
    target_angle_bytes = bytes(str(target_angle) + '\n', 'utf-8')
    # tito()
    ser.write(target_angle_bytes)
    # tito()
    # Print the target angle

    # clock.tick(fps)
    ite = ite + 1
    tock = time.time_ns()
    dt = tock-tick
    sumdt = sumdt + dt
    # print(dt)
    # try:
    #     time.sleep(0.0007-dt)
    # except:
    #     print("crap")
    tockabs = time.perf_counter()
    print(dt)

