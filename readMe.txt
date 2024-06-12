# read me file for "Shear wave propagation in the Achilles subtendons is modulated by helical twist and nonuniform loading"

data.mat: final wave speed and stress dataset used for all analyses in the study. 
Column 1 = gastrocnemius preferentially loaded
Column 2 = uniform loading
Column 3 = soleus preferentially loaded
* data showing a 0 in either wave speed or stress indicated a simulation that did not converge to a solution

radonFunction.m: matlab function for determining shear wave speeds using a Radon transform

*.fs2: FEBioStudio base file

*.feb: .feb files for each helical twist condition

*.py: python script and associated functions for applying helical twist to the base .feb file