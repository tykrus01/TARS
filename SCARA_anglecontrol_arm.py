import math
import pygame

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the screen
pygame.display.set_caption("Two-Link Robot Simulation")

# Define the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Define the link lengths
l1 = 190.0
l2 = 130.0

# Define the initial angles of the two links
homepos1=-45.0
homepos2=-160.0

theta1 = homepos1*math.pi/180
theta2 = homepos2*math.pi/180

itheta1limitl = -1.0
itheta1limith = 160.0
itheta2limitl = -1.0
itheta2limith = 160.0

theta1limitl = math.pi*itheta1limitl/180
theta1limith = math.pi*itheta1limith/180
theta2limitl = math.pi*itheta2limitl/180
theta2limith = math.pi*itheta2limith/180


# Define the position of the base of the robot
x0 = screen_width / 2
y0 = screen_height / 2

# Define the position of the end-effector of the robot
x_end = x0 + l1 * math.cos(theta1) + l2 * math.cos(theta1 + theta2)
y_end = y0 + l1 * math.sin(theta1) + l2 * math.sin(theta1 + theta2)

# Define the speed of the robot
speed = 4.9234123490871293874

# Define the font for displaying the angles
font = pygame.font.SysFont(None, 25)

# Define the clock
clock = pygame.time.Clock()

# Define the main loop of the program
# Define the main loop of the program
while True:
    # Clear the screen
    screen.fill(white)

    # Draw the base of the robot
    pygame.draw.circle(screen, black, (int(x0), int(y0)), 10)

    # Draw the first link of the robot
    pygame.draw.line(screen, black, (int(x0), int(y0)), (int(x0 + l1 * math.cos(theta1)), int(y0 + l1 * math.sin(theta1))), 5)

    # Draw the second link of the robot
    pygame.draw.line(screen, black, (int(x0 + l1 * math.cos(theta1)), int(y0 + l1 * math.sin(theta1))), (int(x_end), int(y_end)), 5)

    # Draw the end-effector of the robot
    pygame.draw.circle(screen, blue, (int(x_end), int(y_end)), 10)

    # Display the angles of the two links
    theta1_text = font.render("Theta1: {:.2f}".format(math.degrees(theta1)), True, black)
    theta2_text = font.render("Theta2: {:.2f}".format(math.degrees(theta2)), True, black)
    screen.blit(theta1_text, (10, 10))
    screen.blit(theta2_text, (10, 40))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # Update the angles of the two links based on the pressed keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        theta1 -= math.radians(speed)
        theta2 -= math.radians(speed)
        if theta1 < -theta1limith:
            theta1 = -theta1limith
        if theta2 < -theta2limith:
            theta2 = -theta2limith
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        theta1 -= math.radians(speed)
        theta2 += math.radians(speed)
        if theta1 < -theta1limith:
            theta1 = -theta1limith
        if theta2 > theta2limitl:
            theta2 = theta2limitl
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        theta1 += math.radians(speed)
        theta2 -= math.radians(speed)
        if theta1 > theta1limitl:
            theta1 = theta1limitl
        if theta2 < -theta2limith:
            theta2 = -theta2limith
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        theta1 += math.radians(speed)
        theta2 += math.radians(speed)
        if theta1 > theta1limitl:
            theta1 = theta1limitl
        if theta2 > theta2limitl:
            theta2 = theta2limitl
    elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        if keys[pygame.K_LEFT]:
            theta1 -= math.radians(speed)
        else:
            theta1 += math.radians(speed)
        if theta1 < -theta1limith:
            theta1 = -theta1limith
        elif theta1 > theta1limitl:
            theta1 = theta1limitl
    elif keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        if keys[pygame.K_UP]:
            theta2 -= math.radians(speed)
        else:
            theta2 += math.radians(speed)
        if theta2 < -theta2limith:
            theta2 = -theta2limith
        elif theta2 > theta2limitl:
            theta2 = theta2limitl

    # Update the position of the end
    x_end = x0 + l1 * math.cos(theta1) + l2 * math.cos(theta1 + theta2)
    y_end = y0 + l1 * math.sin(theta1) + l2 * math.sin(theta1 + theta2)
    # Update the screen
    pygame.display.update()

    # Set the FPS
    clock.tick(60)

pygame.quit()

