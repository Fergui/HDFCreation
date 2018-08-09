# HDFCreation

From a desired path, it takes the geolocated data in MOD03/MYD03 and the Fire Mask data in MOD14/MYD14 and create a new HDF file called MODNN/MYDNN

# Required

Python 2.7+ with pyhdf

Recomended:
Download anaconda2 and use
conda install -c conda-forge pyhdf

# Execution

python processHDF path_desired

# Result

It is going to generate a MODNN/MYDNN file for each pair of MOD03/MYD03 and MOD14/MYD14 in the desired path
