import numpy as np
import matplotlib.pyplot as plt
import os

# Print head info
print("============================================================================")
print(" _______       ___   .___________.    ___   ____    ____  __       _______.")
print("|       \     /   \  |           |   /   \  \   \  /   / |  |     /       |")
print("|  .--.  |   /  ^  \ `---|  |----`  /  ^  \  \   \/   /  |  |    |   (----`")
print("|  |  |  |  /  /_\  \    |  |      /  /_\  \  \      /   |  |     \   \    ")
print("|  '--'  | /  _____  \   |  |     /  _____  \  \    /    |  | .----)   |   ")
print("|_______/ /__/     \__\  |__|    /__/     \__\  \__/     |__| |_______/    ")

print("    ___              _                                  __     ___ ")
print("   /   |  __________(_)___ _____  ____ ___  ___  ____  / /_   |__ \\")
print("  / /| | / ___/ ___/ / __ `/ __ \/ __ `__ \/ _ \/ __ \/ __/   __/ /")
print(" / ___ |(__  |__  ) / /_/ / / / / / / / / /  __/ / / / /_    / __/ ")
print("/_/  |_/____/____/_/\__, /_/ /_/_/ /_/ /_/\___/_/ /_/\__/   /____/ ")
print("                   /____/                                          ")

print("Timucin Besken - 14-924-609")
print("============================================================================")


# Constants (do not edit)
XDIM = 500
YDIM = 500
ZDIM = 100
NO_DATA_VAL = 1.0000000e+35
UMAXVAL = 85.17703
VMAXVAL = 82.95293

# Configs
ELEVATION = 5  # * 0.2 km
sample_hour = "01"
TERRAIN_LEVELS = 11
TEMPERATURE_LEVELS = 11
PDFNAME = "dvc_ex_2_14924609_output_figure.pdf"

# Data set files
Hg_file_path = "HGTdata.bin"  # Terrain
TCf_file_path = "TCf" + sample_hour + ".bin"  # Temperature
Uwind_file_path = "Uf" + sample_hour + ".bin"  # U wind
Vwind_file_path = "Vf" + sample_hour + ".bin"  # V wind


# Helper function to get value from 1D array of data
def get_val_from_set(x, y, z, data):
    return data[x + y*XDIM + z*XDIM*YDIM]


# Helper function to get data from binary file
def get_data(file_name):
    try:
        data = np.fromfile(file_name, dtype=">f4")  # >f = big-endian float
    except FileNotFoundError:
        file_found = False
        while(not file_found):
            print("File " + file_name + " was not found!")
            manual_file_name = input("Manually specify " + file_name + " path (e.g. C:\data\\fileName.bin): ")
            file_found = os.path.exists(manual_file_name)
        data = np.fromfile(manual_file_name, dtype=">f4")  # >f = big-endian float
    return data


# Helper function to create 2D (numpy) matrix from 3D data set
def create_2D_matrix(data_set, elevation):
    matrix = np.empty([XDIM, YDIM])
    for x in range(XDIM):
        for y in range(YDIM):
            matrix[x][y] = get_val_from_set(x, y, elevation, data_set)
    return matrix

########################
#       Task 1         #
########################
print("Preparing data for terrain...")
# Get Data
terrain_data_set = get_data(Hg_file_path)
# Transform into 2D matrix (500x500 with elevation 0)
terrain_matrix = create_2D_matrix(terrain_data_set, 0)
# Terrain levels, levels from minimum value to max ignoring no data
terrain_levels = np.linspace(terrain_matrix.min(), terrain_matrix.max(), TERRAIN_LEVELS)

########################
#       Task 2         #
########################
print("Preparing data for temperature...")
# Get Data
temp_data_set = get_data(TCf_file_path)
# Transform into 2D matrix (500x500 with elevation 4)
temp_matrix = create_2D_matrix(temp_data_set, ELEVATION)
# Temperature levels, levels from minimum value to max ignoring no data
temp_levels = np.linspace(temp_matrix.min(), temp_matrix[temp_matrix < NO_DATA_VAL].max(), TEMPERATURE_LEVELS)

########################
#       Task 3         #
########################
print("Preparing data for wind speed and direction...")
# Get Data
u_wind_data_set = get_data(Uwind_file_path)
v_wind_data_set = get_data(Vwind_file_path)
# Transform into 2D matrix (500x500)
u_wind_matrix = create_2D_matrix(u_wind_data_set, ELEVATION)
v_wind_matrix = create_2D_matrix(v_wind_data_set, ELEVATION)
# Replace no data with nan
u_wind_matrix[u_wind_matrix > UMAXVAL] = np.nan
v_wind_matrix[v_wind_matrix > VMAXVAL] = np.nan
# Reshape into 20x20 by taking mean of submatrices
# (based on https://stackoverflow.com/questions/4624112/grouping-2d-numpy-array-in-average/4624923#4624923)
u_wind_20x20 = u_wind_matrix.reshape([20, XDIM//20, 20, YDIM//20]).mean(3).mean(1)
v_wind_20x20 = v_wind_matrix.reshape([20, XDIM//20, 20, YDIM//20]).mean(3).mean(1)

# Horizontal wind speed (sqrt(u^2 + v^2)) in m/s
horizontal_wind_speed = np.sqrt(u_wind_20x20**2 + v_wind_20x20**2)

########################
#       Plots          #
########################

fig = plt.figure(figsize=(15, 8))

# Set axis
x_axis = np.arange(0, 500)
y_axis = np.arange(500, 0, -1)  # Flip y axis

# Title and labels
plt.title("Visualization of air temperature and wind speed of Hurrican Isabel in 2004 \n \
           sample hour 01, slice height 1 Km")
plt.xlabel("Latitude y - 23.7N to 41.7N")
plt.ylabel("Longitude x - 83W to 62W")
fig.suptitle("DVC Assignment 2 - Besken Timucin", fontweight="bold", fontsize=12)

# Plot terrain
print("Plotting terrain...")
plt.contour(x_axis, y_axis, terrain_matrix,
            cmap="terrain")
plt.colorbar(label="Terrain elevation [m]")  # colorbar for terrain

# Plot temp
print("Plotting temperature...")
plt.contourf(x_axis, y_axis, temp_matrix, temp_levels,
             cmap="coolwarm")
plt.colorbar(label="Temperature [°C]")  # Color bar for Temp

# Plot wind
print("Plotting wind...")
x_wind_axis = np.arange(0, 500, 25)  # Recalculate axis since grid is 20x20
y_wind_axis = np.arange(500, 0, -25)  # Flip y axis
quiver_plt = plt.quiver(x_wind_axis, y_wind_axis, u_wind_20x20, v_wind_20x20, horizontal_wind_speed,
                        scale=1.3,
                        scale_units="dots",
                        pivot="mid",
                        cmap="summer")
plt.colorbar(label="Horizontal wind speed [m/s]")

# Save to pdf
plt.savefig(PDFNAME,
            orientation="portrait",
            format="pdf")
print("Done")

# Show figure
plt.show()


