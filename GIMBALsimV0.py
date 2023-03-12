import pygame
from pygame.locals import *
import math
import configparser
from numpy import dot, array, linalg, matmul

# Define vector coordinates
vec = [0, -1, 0]

# Define screen size
screen_width = 600
screen_height = 600

dtheta = 0.125

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("3D Vector Plotter")

def sind(thetad):
    theta = math.sin(thetad*math.pi/180.0)
    return theta

def cosd(thetad):
    theta = math.cos(thetad*math.pi/180.0)
    return theta

# Define rotation function
def rotate(vector, angle, axis):
    rad = math.radians(angle)
    sin = math.sin(rad)
    cos = math.cos(rad)
    x, y, z = vector
    if axis == "x":
        new_x = x
        new_y = y * cos - z * sin
        new_z = y * sin + z * cos
    elif axis == "y":
        new_x = x * cos + z * sin
        new_y = y
        new_z = -x * sin + z * cos
    elif axis == "z":
        new_x = x * cos - y * sin
        new_y = x * sin + y * cos
        new_z = z
    return [new_x, new_y, new_z]

def rotate3d(vector, anglev):
    alpha = anglev[0]
    beta = anglev[1]
    gamma = anglev[2]
    rgamma = array([[cosd(gamma),-sind(gamma),0],[sind(gamma),cosd(gamma),0],[0,0,1]])
    rbeta = array([[cosd(beta),0,sind(beta)],[0,1,0],[-sind(beta),0,cosd(beta)]])
    ralpha = array([[1,0,0],[0,cosd(alpha),-sind(alpha)],[0,sind(alpha),cosd(alpha)]])
    rmat = matmul(rgamma,matmul(rbeta,ralpha))
    rotvec = matmul(rmat,array(vector))
    return rotvec

# Define main loop
running = True
angle_x = 0
angle_y = 0
anglevec_x = 0
anglevec_y = 0
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        angle_x -= dtheta
    elif keys[pygame.K_DOWN]:
        angle_x += dtheta
    elif keys[pygame.K_LEFT]:
        angle_y += dtheta
    elif keys[pygame.K_RIGHT]:
        angle_y -= dtheta
    elif keys[pygame.K_w]:
        anglevec_x -= dtheta
    elif keys[pygame.K_s]:
        anglevec_x += dtheta
    elif keys[pygame.K_a]:
        anglevec_y -= dtheta
    elif keys[pygame.K_d]:
        anglevec_y += dtheta

    anglevec = [anglevec_x,anglevec_y,0]

    vec1 = vec
    vec1 = rotate3d(vec1, anglevec)
    vec1 = rotate3d(vec1, anglevec)
    # Clear screen
    screen.fill((255, 255, 255))
    # Define vectors for drawing lines, this is for camera rotation
    origin = [screen_width / 2, screen_height / 2]
    vec_start = origin

    rotated_vec = rotate(vec1, angle_y, "y")
    rotated_vec= rotate(rotated_vec, angle_x, "x")
    vec_end = [vec_start[i] + rotated_vec[i] * 50 for i in range(2)]

    pygame.draw.line(screen, (255, 0, 0), vec_start, vec_end,3)

    # Draw axes
    axes = [(50, 0, 0), (0, 50, 0), (0, 0, 50)]
    for axis in axes:
        rotated_axis = rotate(axis, angle_y, "y")
        rotated_axis = rotate(rotated_axis, angle_x, "x")
        axis_end = [vec_start[i] + rotated_axis[i] * 50 for i in range(2)]
        pygame.draw.line(screen, (0, 0, 0), vec_start, axis_end, 1)

    # Update display
    pygame.display.update()
    vec = vec1
    anglevec_x = 0
    anglevec_y = 0

    clock.tick(120)

# Quit Pygame
pygame.quit()
