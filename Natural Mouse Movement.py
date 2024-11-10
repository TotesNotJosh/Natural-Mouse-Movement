import pyautogui as p
import random
import numpy as np
import math
import time
from scipy import interpolate

RANDOM_OFFSET = 10

def find_distance(x1, y1 ,x2 , y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def move_mouse(first_position, second_position, draw):
    x1, y1 = first_position
    x2, y2 = second_position
    random_points = random.randint(3, 7) #Creates a random number of points on the line for the belzier curve to follow
    x = np.linspace(x1, x2, num=random_points, dtype='int')
    y = np.linspace(y1, y2, num=random_points, dtype='int')
    xr = [random.randint(-RANDOM_OFFSET, RANDOM_OFFSET) for point in range(random_points)] #Creates a random offset for each random point
    yr = [random.randint(-RANDOM_OFFSET, RANDOM_OFFSET) for point in range(random_points)] #This is what makes it curve randomly
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr
    degree = 3 if random_points > 3 else random_points - 1
    spline_curve, spline_points = interpolate.splprep([x,y], k=degree)
    spline_points = np.linspace(0, 1, num=2+int(find_distance(x1, y1, x2, y2) / 50.0))
    points = interpolate.splev(spline_points, spline_curve)
    duration = (random.randint(1, 250) * 0.0000002) #Adds randomness to the speed each line is drawn 0.1
    timeout = duration / len(points[0])
    point_list = zip(*(i.astype(int) for i in points))
    if draw == True:
        p.mouseDown()
    for point in point_list:
        p.moveTo(*point, duration= duration)
        time.sleep(timeout)
    p.mouseUp()

def main(coords):
    x1, y1 = next(iter(coords.items()))
    move_mouse((p.position()),(x1, y1), draw = False) #Moves the mouse from the wherever it might be when the script starts to the first positions in the dictionary
    x_coords = list(coords.keys())
    for i in range(len(x_coords) - 1): #Loops through the dict and adds a little more randomness to the starting and ending points to mimic the slight movement you have when you release and click your mouse
        first_position = (x_coords[i] + random.randint(-5, 5)), (coords[x_coords[i]] + random.randint(-5, 5))
        second_position = (x_coords[i + 1] + random.randint(-5, 5)), (coords[x_coords[i + 1]] + random.randint(-5, 5))
        move_mouse(first_position, second_position, draw = True)

if __name__ == "__main__":
    star = {600:900, 900:180, 1200:930, 450:400, 1290:420, 610:910} #Draws a five pointed star
    square = {600:900, 1100:900, 1110:400, 610:400, 605:900} #Draws a square
    triangle = {800:300, 600:750, 1000:750, 810:300} #Draws a triangle
    main(triangle)
    main(square)
    main(star)
    