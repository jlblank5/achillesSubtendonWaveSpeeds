# read me file for "Shear wave propagation in the Achilles subtendons is modulated by helical twist and nonuniform loading"
Jonathon Blank, Lauren Welte, Jack Martin, Darryl Thelen
University of Wisconsin-Madison
Universtiy of Alberta

data.mat: final wave speed and prinical stress dataset used for all analyses in the study. 
Column 1 = gastrocnemius preferentially loaded
Column 2 = uniform loading
Column 3 = soleus preferentially loaded
* data showing a 0 in either wave speed or stress indicates a simulation that did not converge to a solution

radonFunction.m: matlab function for determining shear wave speeds using a Radon transform

baseModel.fs2: FEBioStudio base file
baseModel.feb: Febio base file (to be used in Python scripts)

*.feb: .feb files for each helical twist condition (0.feb, 10.feb, 20.feb, etc.)

edit_base_file.py: python script and associated functions for applying helical twist to the base .feb file
write_files.py: python script and associated functions for applying helical twist to the base .feb file
HTC_read.py: library of functions to read .feb files
HTC_write.py: library of functions to write .feb files
