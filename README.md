
 _______       ___   .___________.    ___   ____    ____  __       _______.
|       \     /   \  |           |   /   \  \   \  /   / |  |     /       |
|  .--.  |   /  ^  \ `---|  |----`  /  ^  \  \   \/   /  |  |    |   (----`
|  |  |  |  /  /_\  \    |  |      /  /_\  \  \      /   |  |     \   \    
|  '--'  | /  _____  \   |  |     /  _____  \  \    /    |  | .----)   |   
|_______/ /__/     \__\  |__|    /__/     \__\  \__/     |__| |_______/    
    ___              _                                  __     ___ 
   /   |  __________(_)___ _____  ____ ___  ___  ____  / /_   |__ \
  / /| | / ___/ ___/ / __ `/ __ \/ __ `__ \/ _ \/ __ \/ __/   __/ /
 / ___ |(__  |__  ) / /_/ / / / / / / / / /  __/ / / / /_    / __/ 
/_/  |_/____/____/_/\__, /_/ /_/_/ /_/ /_/\___/_/ /_/\__/   /____/ 
                   /____/                
                          
Student Name:Timucin Besken
Matriculation Number: 14-924-609

Usage:
conda create --name dvca2besken python=3 matplotlib numpy
activate dvca2besken
python Exercise2.py

IDE used: JetBrains PyCharm Community Edition 2017.2.1

Python Distro: Anaconda 5.0.1 Python 3.6 version
Libraries: 
1. matplotlib v2.1.0
2. numpy v1.13.3

Interpreter: Python 3.6.3

File needed:
HGTdata.bin
TCf01.bin
Uf01.bin
Vf01.bin
(Downloadable from: http://vis.computer.org/vis2004contest/data.html)

Implementation:
I decided this time to keep it simple without creating useless and complex classes.
First I'm declaring some costants which I will need later (such as XDIM, YDIM, NO_DATA_VAL) which are the
dimension of the data set and some special values.
After that I have the configuration variables, where the elevation and sample hour can be chosen.

I'm using 3 helper functions:
	1) get_val_from_set(x,y,z,data): this function takes as argument the desired index of the 3D matrix and the data array 
           and returns the value at the wanted position.
	   This is needed because when we open the file we have a 1D array.
	2) get_data(file_name): this function simply reads the data from the binary file and returns a numpy 1D array with the content.
	3) create_2D_matrix(data_set, elevation): this function creates a 2D matrix from the 1D array with the help of the first function
	   to get the right value. This can also be done with np.reshape but when I started I thought I would need to manipulate some values.

Task 1:
Here I simply get the data and build the 2D matrix with the functions above.
For plotting it I decided to use matplotlib.contour() instead of .contourf() since the contour is better visible when the rest is plotted above.

Task 2:
Same as task 1 with the difference that here the maximum value is the NO_DATA_VAL, and therefore this had to be ignored,
and of course here the plot is a full contour plot (matplotlib.contourf())

Task 3:
In the last task, to build the 20x20 grid I proceded in two steps:
1) Replace all NO_DATA_VAL with NaN
2) Downsample from 500x500 to 20x20 by taking the mean of the 25x25 submatrices as values for every 20x20 matrix cell

After that I just calculated the horizontal wind speed in order to color the arrows according to the wind speed.
The plotting was done with a quiver plot (matplotlib.quiver())
