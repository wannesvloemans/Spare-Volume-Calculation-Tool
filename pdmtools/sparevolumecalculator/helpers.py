import os
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random


def intersect(x, y, R, placed_cables, min_distance_cables=0):

    """ Function to determine whether a circle with origin (x, y)
        and radius R is intersecting with another cable that was
        already placed into the grid. """

    for placed_cable in placed_cables:
        if math.sqrt((placed_cable["x-coordinate"]-x)**2 + (placed_cable["y-coordinate"]-y)**2) < placed_cable["radius"] + R + min_distance_cables:
            return True
    return False


def in_area(a, b, x, y, R, min_distance_border=0):

    """ Function to determine whether a circle with origin (x, y)
        and radius R is located entirely in the rectangular area
        defined by a and b.
    """

    if 0 <= x-R-min_distance_border and x+R+min_distance_border <= a and 0 <= y-R-min_distance_border and y+R+min_distance_border <= b:
        return True
    return False


def add_cable(a,b,cable,placed_cables):

    """ Function to add a cable to the grid if possible. """

    # Define the size of the grid
    coarseness = 0.125 # Defines the courseness of the grid as the distance between two adjacent grid points (in mm)
    c, d = round(a/coarseness), round(b/coarseness)

    # Generate the x and y coordinates of the grid points
    xlist = np.linspace(coarseness, a, c)
    ylist = np.linspace(coarseness, b, d)

    min_distance_border = 0 # Minimal distance between a cable and the border of the area.
    min_distance_cables = 0 # Minimal distance between two adjacent cables.

    for y in ylist:
        for x in xlist:
            if in_area(a, b, x, y, cable, min_distance_border) and not intersect(x, y, cable, placed_cables, min_distance_cables):
                placed_cables.append({"radius": cable, "x-coordinate": x, "y-coordinate": y})
                return
    print(f"Unable to place the cable with radius {cable}.")
    return False


def plot_circles_on_grid(circles, a, b):

    """ Function to plot the placed cables in the grid. """
    if len(circles) == 0:
        return False
    fig, ax = plt.subplots()
    colors = set()
    for circle in circles:
        x, y = circle['x-coordinate'], circle['y-coordinate']
        radius = circle['radius']
        while True:
            color = tuple(random.uniform(0, 1) for _ in range(3))  # Generate a random RGB color tuple
            if color not in colors:  # Make sure the color is unique
                colors.add(color)
                break
        ax.add_patch(Circle((x, y), radius, color=color))
    plt.xlim(0, a)  # Set the x-axis limits
    plt.ylim(0, b)  # Set the y-axis limits
    plt.gca().set_aspect('equal', adjustable='box')
    fig.savefig('sparevolumecalculator/static/images/result.png')
    return


def calculate_spare_volume2(a, b, circles):
    """ Function to calculate the spare volume inside the gutter. First, the border of the
        empty space on top of the placed cables is calculated. Next, this border is used
        to determine the spare volume inside the gutter. The value of "mesh" is a measure
        of the accuracy of the calculation. In general, a higher value for mesh increases
        the accuracy, but also the computational effort. """
    min_distance_border = 0 # Minimal distance between a cable and the border of the area.
    min_distance_cables = 0 # Minimal distance between two adjacent cables.
    mesh = a
    filled_area = 0
    border_heights = []
    for x in range(0, a, round(a/mesh)):
        for y in range(b, 0, -1):
            if in_area(a, b, x, y, 1, min_distance_border) and intersect(x, y, 0.001, circles, min_distance_cables):
                border_heights.append(y)
                filled_area += (a/mesh)*y
                break
    spare_volume = ((a*b -filled_area) / (filled_area))*100
    return round(spare_volume, 2)