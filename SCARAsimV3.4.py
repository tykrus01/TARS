import math
import pygame
import sys
import configparser
from ast import literal_eval
from numpy import dot, array, linalg


config = configparser.ConfigParser()
config.read('init.ini')

g='geometry'
d='display'
c='control'
s='simulation'

# Initialize Pygame
pygame.init()

#define framerate and timestep (note timestep is currently unused as calculations are done per frame for convenience)
fps = config.getint(s,'fps')
dt = 1/fps

#defining the simulation clock
clock = pygame.time.Clock()

###Begin controller initialization

#controller init
pygame.joystick.init()

#defining controller mode to be off/keyboard mode on at init
is_controller_mode = config.getboolean(c,'is_controller_default')

# Check how many joysticks are connected
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks found.")

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

# Define the range of the joystick input
JOYSTICK_RANGE = 32767

# Define deadzone lower limit as a percentage

bdeadzone = config.getfloat('control','bdeadzone')

###end controller initialization

# Set the screen dimensions
screen_width = config.getint(d,'w')
screen_height = config.getint(d,'h')

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the screen
pygame.display.set_caption("Two-Link Robot Simulation")

# Define the colors
black = literal_eval(config.get('color', 'black'))
white = literal_eval(config.get('color', 'white'))
red = literal_eval(config.get('color', 'red'))
green = literal_eval(config.get('color', 'green'))
blue = literal_eval(config.get('color', 'blue'))

# Define the link lengths
simscale = config.getint('simulation','simscale')
l1 = config.getfloat(g, 'l1')*simscale
l2 = config.getfloat(g, 'l2')*simscale

# Define Angle Limits l:low h:high
#theta1 is an absolute angle,theta2 is relative to theta1
#klimit is the relative angle difference limit, eg klimit = 20 ensures that link2 is always at least 20 degrees away from being colinear

klimit = config.getint('geometry','klimit')

theta1limitl = config.getint(g, 'btheta1limitl')
theta1limith = config.getint(g, 'btheta1limith')
theta2limitl = config.getint(g, 'btheta2limitl')
theta2limith = config.getint(g, 'btheta2limith')

thetalimitv = [theta1limitl,theta1limith,theta2limitl,theta2limith]

#Define Homeposition, this position was solved to be directly vertical at (0,2ft)
homepos1=float(config.get(g, 'hpostheta1'))
homepos2=float(config.get(g, 'hpostheta2'))

#initialization of theta1 and theta2
theta1 = homepos1
theta2 = homepos2

#velocity limit in cartesian direction FIX
vlimit=config.getint(s,'vlimit')

def jacobianR2P(x, y, l2, theta1, theta2):
    matrix = array([[-y, -l2*sind(theta1+theta2)], [x, l2*cosd(theta1+theta2)]], dtype=float)
    return matrix

def inv_jacobian(J):
    invJ = linalg.inv(J)
    return invJ

def invjacprod(x, y, l2, theta1, theta2, limitv):
    J = jacobianR2P(x, y, l2, theta1, theta2)
    invJ = inv_jacobian(J)
    wlimit = dot(invJ, limitv)
    return wlimit

def sind(thetad):
    theta = math.sin(thetad*math.pi/180.0)
    return theta

def cosd(thetad):
    theta = math.cos(thetad*math.pi/180.0)
    return theta

def toggle_controller_mode():
    global is_controller_mode
    is_controller_mode = not is_controller_mode

def limitborders():
    x1 = x0 + l1 * cosd(theta1limitl) + l2 * cosd(theta1limitl + theta2limitl)
    y1 = y0 + l1 * sind(theta1limitl) + l2 * sind(theta1limitl + theta2limitl)

    for i in range(theta1limitl,theta1limith):

        x2 = x0 + l1 * cosd(i) + l2 * cosd(i + theta2limitl)
        y2 = y0 + l1 * sind(i) + l2 * sind(i + theta2limitl)
        pygame.draw.line(screen, red, (x1,y1), (x2,y2), 1)
        x1=x2
        y1=y2

    for i in range(theta2limitl,theta2limith):

        x2 = x0 + l1 * cosd(theta1limith) + l2 * cosd(theta1limith + i)
        y2 = y0 + l1 * sind(theta1limith) + l2 * sind(theta1limith + i)
        pygame.draw.line(screen, red, (x1,y1), (x2,y2), 1)
        x1=x2
        y1=y2

    for i in range(theta1limith,theta1limitl,-1):

        x2 = x0 + l1 * cosd(i) + l2 * cosd(i + theta2limith)
        y2 = y0 + l1 * sind(i) + l2 * sind(i + theta2limith)
        pygame.draw.line(screen, red, (x1,y1), (x2,y2), 1)
        x1=x2
        y1=y2


    for i in range(theta2limith,theta2limitl,-1):

        x2 = x0 + l1 * cosd(theta1limitl) + l2 * cosd(theta1limitl + i)
        y2 = y0 + l1 * sind(theta1limitl) + l2 * sind(theta1limitl + i)
        pygame.draw.line(screen, red, (x1,y1), (x2,y2), 1)
        x1=x2
        y1=y2

nfactor = 0.1
tfactor = 1-nfactor

def translation(theta1, theta2, vlimitv):

    w = invjacprod(x_end - x0, y_end - y0, l2, theta1, theta2, vlimitv)
    w1 = float(w[0])
    w2 = float(w[1])
    theta1_new = theta1 + w1
    theta2_new = theta2 + w2
    if theta1limitl <= theta1_new <= theta1limith and theta2limitl <= theta2_new <= theta2limith:
        theta1 = theta1_new
        theta2 = theta2_new
    elif theta1limitl+1 <= theta1 <= theta1limith-1:
        vlimitx = -(l1*cosd(theta1)+l2*cosd(theta1+theta2))
        vlimity = -(l1*sind(theta1)+l2*sind(theta1+theta2))
        vlimitvpre = array([vlimitx, vlimity], dtype=float)/math.sqrt(vlimitx*vlimitx+vlimity*vlimity)

        s = array([-vlimity, vlimitx])/math.sqrt(vlimitx*vlimitx+vlimity*vlimity)

        vlimitv = (dot(vlimitv, s)/dot(s, s)*s*tfactor+vlimitvpre*nfactor)*1
        print(vlimitv)

        w = invjacprod(x_end - x0, y_end - y0, l2, theta1, theta2, vlimitv)
        w1 = float(w[0])
        w2 = float(w[1])
        theta1_new = theta1 + w1
        theta2_new = theta2 + w2
        if theta1limitl <= theta1_new <= theta1limith and theta2limitl <= theta2_new <= theta2limith:
            theta1 = theta1_new
            theta2 = theta2_new


    return theta1, theta2




# Define the position of the base of the robot
x0 = screen_width / 2
y0 = screen_height / 2

# Define the position of the end-effector of the robot
x_end = x0 + l1 * cosd(theta1) + l2 * cosd(theta1 + theta2)
y_end = y0 + l1 * sind(theta1) + l2 * sind(theta1 + theta2)


# Define the font for displaying the angles
font = pygame.font.SysFont(None, 25)

ngrid = 5

# Define the main loop of the program
while True:
    # Clear the screen
    screen.fill(white)

    # Draw gridlines DELETE FOR PERFORMANCE
    for i in range(-ngrid,ngrid):
        glinebeginv = (i*simscale+screen_width/2,0)
        glineendv = (i*simscale+screen_width/2, screen_height)
        pygame.draw.line(screen, green, glinebeginv, glineendv)

    for j in range(-ngrid,ngrid):
        glinebeginh = (0,j*simscale+screen_height/2)
        glineendh = (screen_width, j*simscale+screen_height/2)
        pygame.draw.line(screen, green, glinebeginh, glineendh)

    limitborders()

    # Draw the base of the robot
    pygame.draw.circle(screen, black, (float(x0), float(y0)), 10)

    # Draw the first link of the robot
    pygame.draw.line(screen, black, (float(x0), float(y0)), (float(x0 + l1 * cosd(theta1)), float(y0 + l1 * sind(theta1))), 5)

    # Draw the second link of the robot
    pygame.draw.line(screen, black, (float(x0 + l1 * cosd(theta1)), float(y0 + l1 * sind(theta1))), (float(x_end), float(y_end)), 5)

    # Draw the end-effector of the robot
    pygame.draw.circle(screen, blue, (float(x_end), float(y_end)), 10)


    # Display the angles and cartesian coordinates of the two links DELETE FOR PERFORMANCE
    theta1_text = font.render("Theta1: {:.2f}".format(theta1), True, black)
    theta2_text = font.render("Theta2: {:.2f}".format(theta2), True, black)
    xpos_text = font.render("Xpos: {:.2f}".format(x_end-x0), True, black)
    ypos_text = font.render("Ypos: {:.2f}".format(y_end-y0), True, black)

    #defines the text position relative to top left corner of window
    screen.blit(theta1_text, (10, 10))
    screen.blit(theta2_text, (10, 40))
    screen.blit(xpos_text, (10, 70))
    screen.blit(ypos_text, (10, 100))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # Get the current joystick input
    try:
        target_xunit = xbox_360_controller.get_axis(0)
        target_yunit = xbox_360_controller.get_axis(1)
    except Exception:
        target_xunit = 0.0
        target_xunit = 0.0


    keys = pygame.key.get_pressed()

    #Executing toggle option on Spacebar input

    if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.JOYBUTTONDOWN and event.button == 4):
        toggle_controller_mode()

    # Keyboard Arrow key control section, checks toggle mode false for controller mode
    if is_controller_mode == False:
        if keys[pygame.K_LEFT]:
            vlimitv = array([-vlimit, 0], dtype=float)
            [theta1, theta2] = translation(theta1,theta2,vlimitv)
        if keys[pygame.K_RIGHT]:
            vlimitv = array([vlimit, 0], dtype=float)
            [theta1, theta2] = translation(theta1, theta2, vlimitv)
        if keys[pygame.K_UP]:
            vlimitv = array([0, -vlimit], dtype=float)
            [theta1, theta2] = translation(theta1, theta2, vlimitv)
        if keys[pygame.K_DOWN]:
            vlimitv = array([0, vlimit], dtype=float)
            [theta1, theta2] = translation(theta1, theta2, vlimitv)
        if keys[pygame.K_SPACE]:
            toggle_controller_mode()

    #Checks controller toggle condition
    elif is_controller_mode==True:
        deadzone = abs(target_yunit) < 0.05 and abs(target_xunit) < 0.05
        if not deadzone:
            vlimitv = array([vlimit*target_xunit, vlimit*target_yunit], dtype=float)
            [theta1, theta2] = translation(theta1, theta2, vlimitv)

    # Update the position of the end
    x_end = x0 + l1 * cosd(theta1) + l2 * cosd(theta1 + theta2)
    y_end = y0 + l1 * sind(theta1) + l2 * sind(theta1 + theta2)

    # Update the screen
    pygame.display.update()

    # Set the FPS
    clock.tick(fps)

pygame.quit()

