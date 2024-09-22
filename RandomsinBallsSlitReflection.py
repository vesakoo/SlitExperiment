from vpython import sphere, vector, rate, sin, cos, box, label
import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Create the double-slit wall
wall_thickness = 0.2
wall_height = 10
wall_width = 0.5
amplitude = 2.0
freq = 2.5

# Position of the first wall (double-slit)
wall_pos1 = vector(0, 0, 0)

second_wall_x = 8

# Reduce the slit size by half (adjust the height of the top and bottom parts)
slit_size = 1  # Half of the original size
gap_size = 1  # Space between the top and bottom walls

# Create the top and bottom parts of the wall around the smaller slits
top_wall = box(pos=wall_pos1 + vector(0, wall_height / 4 + gap_size / 2, 0), 
               size=vector(wall_width, wall_height / 2 - slit_size, wall_thickness), color=vector(0.5, 0.5, 0.5))
bottom_wall = box(pos=wall_pos1 + vector(0, -wall_height / 4 - gap_size / 2, 0), 
                  size=vector(wall_width, wall_height / 2 - slit_size, wall_thickness), color=vector(0.5, 0.5, 0.5))

# Create the second solid wall (no gaps)
wall_pos2 = vector(second_wall_x , 0, 0)
second_wall = box(pos=wall_pos2, size=vector(wall_width, wall_height, wall_thickness), color=vector(0.7, 0.7, 0.7))

# Add x-axis scale labels with 10 steps from -5 to 10
for i in range(-7, 11):  # Steps from -5 to 10
    label(pos=vector(i, -2.5, 0), text=str(i), box=False, height=10,color=vector(128, 128, 128)) #color=vector(0, 0, 0))

# List to store the y-positions and angles when the balls pass through the slit and hit the second wall
hit_positions = []
tangent_values = []  # Store the tangent values
angles = []  # Store the angle values in degrees

# Function to simulate the motion of a single ball with a random phase shift
def simulate_ball():
    # Create a random phase shift between -π/2 and π/2
    label(pos=vector(-7,5,0),text='Ball hits: ' + str(len(hit_positions)) + '/300',box=False ,height=10,color=vector(0,255,0))
    phase_shift = random.uniform(0, 2*math.pi)
    amplitude_shift = random.uniform(0.7,amplitude)
    # Create a ball starting from the left
    ball = sphere(pos=vector(-7, 0, 0), radius=0.2, color=vector(1, 0, 0),make_trail=True, retain=100)

    # Time increment
    t = 0
    dt = 0.01
    dy=0 #slit reflection effect
    dangle =0 
    has_interacted = False
    diffr_point_x = 0
    diffr_point_y = 0
    first_diffraction =False
    deltax =0
    deltay =0
    # Loop to move the ball
    while t < 4*30:
        rate(600)  # Control the speed of the animation (100 frames per second)

        # Update the position of the ball
        x = t -2  # x increases over time
        y =  amplitude_shift* sin(t*freq + phase_shift) #-1*dy*(ball.pos.x -1.5)  # y follows a sine curve with the random phase shift 
        if has_interacted:
            tmpx = (x-diffr_point_x)* cos(dangle ) - (y-diffr_point_y)*sin(dangle )
            tmpy = (x-diffr_point_x)*sin(dangle ) +(y-diffr_point_y)*cos(dangle )
            if first_diffraction == False:
              first_diffraction = True
              deltax = x-tmpx
              deltay = y - tmpy
            x=tmpx + diffr_point_x + deltax #+2*1.5
            y=tmpy + diffr_point_y + deltay#- 4*dy*(1.5) 
            #y= y-1*dy*(ball.pos.x -1.5) 

        ball.pos = vector(x - 5, y, 0)  # Update ball position, offset x for centering
        
        # Ball interacts with the double-slit wall
        if (-0.15 < ball.pos.x < 0) and has_interacted == False:
           if -slit_size / 2 < ball.pos.y < slit_size / 2:
               pass
           else:
               ball.clear_trail()
               ball.visible = False
               del(ball)
               return False
        if (0 < ball.pos.x < 0.15) and has_interacted ==False:
            if (-slit_size / 2 < ball.pos.y < slit_size / 2) or has_interacted:  # Ball passes through the smaller slits
                pass  # Continue
            else:
                # Calculate the tangent (dy/dx) and the angle of the sine wave at this point
                tangent = cos(t + phase_shift)  # dy/dx for y = sin(t + phase_shift) is cos(t + phase_shift)
                angle = math.atan(tangent)  # Angle in radians
                dy = tangent#-1*tangent *(ball.pos.x -1.5)
                print("Angle: " + str(math.degrees(angle)) + " tangeng " + str(dy) ) 
                
                dangle = angle
                t -= dt
                diffr_point_x = ball.pos.x
                diffr_point_y = ball.pos.y
                
                # Adjust the phase shift so that the sine wave continues smoothly after diffraction
                # Calculate new phase to keep the sine wave continuous
                new_phase_shift = math.asin((ball.pos.y - diffr_point_y) / amplitude_shift)

                # Store the new phase shift and mark interaction as happened
                phase_shift = new_phase_shift
                has_interacted = True
                
                # Invert the sine wave direction by adding π (1second_wall_x 0 degrees)
                #phase_shift += math.pi  # Change the phase shift to invert the wave

        # Ball reaches the second wall
        if ball.pos.x >= second_wall_x :
            # Store the y position of the ball when it hits the second wall
            hit_positions.append(ball.pos.y)
            ball.clear_trail()
            return True # Stop the ball when it hits the second wall
        
        # Increment time
        t += dt

# Simulate the motion for [num_balls] balls, each with a random phase shift
num_balls = 300
for i in range(num_balls):
    while simulate_ball() ==False:
        pass 
    #simulate_ball()  # Start each ball's journey after the previous one hits the wall

# Plotting the y-positions where the balls hit the second wall using matplotlib
plt.figure(figsize=(second_wall_x , 20))
plt.hist(hit_positions, bins=200, color='blue', alpha=0.7, rwidth=0.85)
plt.title("Distribution of Y-Positions at the Second Wall (10 Balls with Smaller Slits)")
plt.xlabel("Y Position")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
