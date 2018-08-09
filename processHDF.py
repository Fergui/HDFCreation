#!/usr/bin/env python

from pyhdf.SD import SD, SDC
import sys
import os
import re
import glob
import numpy as np

# Function which giving a path, it search all the MOD03, MYD03, MOD14, and MYD14;
# and agrupate per pairs every geolocated product with the fire detection product
def agrupate_files(path):
	# Create a list of lists with all the geolocation files
	files=[[k] for k in glob.glob(path+'/M*D03*.hdf')]
	if len(files)==0:
		print 'Error: Any MODIS HDF file in the path'
		sys.exit()
	# Create a list of the fire detections files
	filesf=glob.glob(path+'/M*D14*.hdf')
	if len(files)!=len(filesf):
		print 'Error: Some files are missing'
		sys.exit()
	# Append each fire detection fire to the correspond list in files list
	for f in filesf:
		# Take the file name
		mf=re.split("/",f)
		if mf is not None:
			# Splitting the name by points
			m=mf[-1].split('.')
			if m is not None:
				# For each file in files
				for k,g in enumerate(files):
					# Take the file name
					mmf=re.split("/",g[0])
					# Splitting the name by points
					mm=mmf[-1].split('.')
					# Look if it is the geolocation file pair of the fire detection file
					if mm[0][1]==m[0][1] and mm[1]+'.'+mm[2]==m[1]+'.'+m[2]:
						# Append inside the corresponding list in files list
						files[k].append(f);		
	return files

# Function which creates the objects to read Latitude, Longitude and fire mask inside the pair files
def read_files(files):
	# Open the HDF files in read mode
	hdfg=SD(files[0],SDC.READ)
	hdff=SD(files[1],SDC.READ)
	# Select the desired objects
	lat_obj=hdfg.select('Latitude')
	lon_obj=hdfg.select('Longitude')	
	fire_mask_obj=hdff.select('fire mask')
	# Return an array with all the objects
	return [lat_obj,lon_obj,fire_mask_obj]

# Function which write the SDSname Scientific Dataset in the filehdf file
def write_file(filehdf,SDSname,data,dtype):
	# Creation of the SDS
	sds=filehdf.create(SDSname,dtype,data.shape)
	# Adding the data to the SDS
	sds[:]=data
	# Close the SDS
	sds.endaccess()

def main():
	# Agrupate all the files in the path
	list_files=agrupate_files(path)
	# For each file in the path, it is created a new HDF file
	for files in list_files:
		# Creation of the objects in order to get the data
		objs=read_files(files)
		# Getting the data: 3 rectangular numpy arrays lat, lon and fire_mask
		lat=np.array(objs[0].get())
		lon=np.array(objs[1].get())
		fire_mask=np.array(objs[2].get())
		# Creation of a data tuple
		data=(lat,lon,fire_mask)
		# New file name from the input files name
		m=files[0].split('/')
		mm=m[-1].split('.')
		nfile=mm[0][0:3]+'NN.'+'.'.join(mm[1:len(mm)])
		# Creation of the new HDF file
		nhdf=SD(nfile,SDC.WRITE|SDC.CREATE)
		print 'Creating:',nfile
		# Writting the data in the new HDF file
		write_file(nhdf,'Latitude',data[0],SDC.FLOAT32)
		write_file(nhdf,'Longitude',data[1],SDC.FLOAT32)
		write_file(nhdf,'FireMask',data[2],SDC.INT32)
		nhdf.end()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print 'Error: python',sys.argv[0],'path_to_hdf_files'
	else:
		path=sys.argv[1];
		if os.path.exists(path):
			sys.exit(main())
		else:
			print 'Error: Invalid path:',path

