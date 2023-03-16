import time
import re
import numpy as np
import creopyson
import os


def naca4(code, n_points):
    """
    This function takes in parametric values for a NACA 4 series airfoil, and it generates the points for a sketch of
    the airfoil. It then formats these points into a way that PTC Creo design software can understand it and plot it.
    Ref: https://web.stanford.edu/~cantwell/AA200_Course_Material/The%20NACA%20airfoil%20series.pdf
    :param code: (str) The first digit specifies the maximum camber (m) in percentage of the chord (airfoil length),
                    the second indicates the position of the maximum camber (p) in tenths of chord, and the last two
                    numbers provide the maximum thickness (t) of the airfoil in percentage of chord.
    :param n_points: (int) Density of the points generated.
    :return: none
    """

    # Initialize values for airfoil
    m = float(code[0]) / 100
    p = float(code[1]) / 10
    t = float(code[2:]) / 100

    x = np.linspace(0, 1, n_points)

    def camberline(x, m, p):
        """
        Function to compute average camberline co-ordinates.
        :param x:
        :param m:
        :param p:
        :return: (array) Y-coordinates
        """
        yc = np.zeros(x.shape)
        yc[x < p] = ((m * x[x < p]) / p ** 2) * (2 * p - x[x < p])
        yc[x >= p] = ((m * (1 - x[x >= p])) / ((1 - p) ** 2)) * (1 + x[x >= p] - 2 * p)
        return yc

    yc = camberline(x, m, p)

    def theta_function(x, m, p):
        """
        Function to determine the angle for mean camberline.
        :param x:
        :param m:
        :param p:
        :return: (array)
        """
        if m > 0:
            dydx = np.zeros(x.shape)
            dydx[x < p] = (2 * m / p ** 2) * (p - x[x < p])
            dydx[x >= p] = ((2 * m) / ((1 - p) ** 2)) * (p - x[x >= p])
            theta = np.arctan(dydx)
        else:
            theta = 0
        return theta

    theta = theta_function(x, m, p)

    # Calculate thickness distribution above and below the mean camberline.
    yt = t * 5 * (0.2969 * (x ** 0.5) - 0.1260 * x - 0.3516 * (x ** 2) + 0.2843 * (x ** 3) - 0.1015 * (x ** 4))

    # Calculate the final co-ordinates for x and y, upper and lower
    xu = x - yt * np.sin(theta)
    xl = x + yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    yl = yc - yt * np.cos(theta)

    # Save top and bottom generated co-ordinates to respective files.
    static_value = np.full(x.shape, 0)
    top_camber_line = np.column_stack((xu, yu, static_value))
    np.savetxt("top_camber_line.pts", top_camber_line, fmt='%.5f')  # TODO remove this later
    bottom_camber_line = np.column_stack((xl, yl, static_value))
    np.savetxt("bottom_camber_line.pts", bottom_camber_line, fmt='%.5f')  # TODO remove this later
    return top_camber_line, bottom_camber_line


def parse_data(raw_data):
    # Split the raw data into lines
    lines = raw_data.split("\n")

    # Initialize an empty list to store the parsed data
    parsed_data = []

    # Loop through the lines and parse the data
    for line in lines:
        # Split the line into x, y, z coordinates
        coordinates = line.split(",")
        x = float(coordinates[0])
        y = float(coordinates[1])
        z = float(coordinates[2])

        # Append the parsed coordinates to the parsed_data list
        parsed_data.append([x, y, z])

    return parsed_data


# Create the points
# naca4(input("What four digits would you like for the profile?"), int(input("What density of points would you like?")))
top, bottom = naca4("2412", 11)

# Initialize creopyson Client and start PTC creo
c = creopyson.Client()
directory_path = os.path.join("C:" "\working", "nitro_proe_remote.bat")
c.start_creo(directory_path)

# Poll to check if PTC is now running with a timeout.
for i in range(3):
    time.sleep(10)
    if c.is_creo_running():
        print("running")
        break

# TODO debug Start CREOSON server
# exe_path = r"C:\working\CREOSON\CreosonServerWithSetup-2.8.1-win64\CreosonSetup.exe"
# subprocess.Popen(exe_path)

# Open Creofile
c.connect()
prt_file = "template_spline.prt"
c.file_open(file_=prt_file, dirname="working", display=True, activate=True)

# TODO this is where I am currently blocked. I am not able to get the spline dimensions or features
# TODO to be able to edit it.

# View functions
c.view_list(prt_file)  # ['BACK', 'BOTTOM', 'DEFAULT', 'FRONT', 'LEFT', 'RIGHT', 'TOP']
c.view_activate("FRONT")

# Parameter functions
parameter_list = c.parameter_list()

# Iterate to fill in top camber-line coordinates.
for i in range(9):
    # Set X coordinate of the point
    x_coordinate_value = top[i+1][0]
    spline_x_coordinate_value = "TP" + str(i+1) + "_X"
    c.parameter_set(spline_x_coordinate_value, value=x_coordinate_value, designate=True, type_="DOUBLE")

    # Set Y coordinate of the point
    y_coordinate_value = top[i+1][1]
    spline_y_coordinate_value = "TP" + str(i+1) + "_Y"
    c.parameter_set(spline_y_coordinate_value, value=y_coordinate_value, designate=True, type_="DOUBLE")

# Iterate to fill in bottom camber-line coordinates.
for i in range(9):
    # Set X coordinate of the point
    x_coordinate_value = bottom[i+1][0]
    spline_x_coordinate_value = "BP" + str(i+1) + "_X"
    c.parameter_set(spline_x_coordinate_value, value=x_coordinate_value, designate=True, type_="DOUBLE")

    # Set Y coordinate of the point
    y_coordinate_value = bottom[i+1][1]*-1
    spline_y_coordinate_value = "BP" + str(i+1) + "_Y"
    c.parameter_set(spline_y_coordinate_value, value=y_coordinate_value, designate=True, type_="DOUBLE")

# TODO remove once testing is done
parameter_list_after_change = c.parameter_list()

c.file_refresh()
c.file_regenerate()

# TODO add a call to save file with a new name.

# Debug point
print("test")

# Close PTC Creo
c.stop_creo()

# TODO
#   [DONE] Take naca input from the user and generate coordinates and save it to a file
#   Edit the existing PRT file with the naca functions output
#   Extrude the sketch and apply the desired dimension to the parameters of the file
#   Export it and save on local directory
# TODO
