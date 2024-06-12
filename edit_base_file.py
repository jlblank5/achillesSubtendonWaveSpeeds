import os
import sys
import numpy
import HTC_read
import HTC_write

def usage(argv):
    print('USAGE: ' + argv[0])

# FEBIO File Generation Code
# Author: Jon Blank (2024)
# Paper: Shear wave propagation in the Achilles subtendons is modulated by helical twist and nonuniform loading
# ======================================================================================================================
# This code changes the cross-sectional dimensions and helical twist of the base model

def main(argv):

    # Check for appropriate usage
    if len(argv) != 1:
        usage(argv)
        sys.exit(1)

    # change your directory to the location of the baseModel.feb file
    baseModelsDir = r"C:\.feb" 
    os.chdir(baseModelsDir)

    FEBfilename="baseModel.feb"
    
    # read the file and store it as a string
    filestr=HTC_read.read_baseFile(FEBfilename)

    # specify the directory to where you want to write the new .feb files
    dir = r"C:\.feb"

    # specify the helical twist angles of interest
    theta=[]
    for ii in range(0,190,10):
        theta.append(ii)
    print(theta)

    # number of models to generate
    nModels = len(theta)

    # specify the width and thickness at each end
    btopmin = 0.96; btopmax = 0.96
    bbottommin = 1.07; bbottommax = 1.07
    atopmin = 2.97; atopmax = 2.97
    abottommin = 3.67; abottommax = 3.67

    # define the bodies in the model to edit
    body1 = 'MedialGastroc'
    body2 = 'LateralGastroc'
    body3 = 'Soleus'
    body1grip = 'G_Grip'
    body2grip = 'S_Grip'

    # set min and max of width and thickness
    atop = numpy.random.uniform(atopmin,atopmax,nModels)
    abottom = numpy.random.uniform(abottommin,abottommax,nModels)
    btop = numpy.random.uniform(btopmin,btopmax,nModels)
    bbottom = numpy.random.uniform(bbottommin,bbottommax,nModels)

    # specify the model length (in meters)
    length = 0.06

    # define base directory
    os.chdir(dir)

    for i in range(0,nModels):

        # filestrtemp = filestr[j]
        filestrtemp = filestr

        # initialize by recording the base model and creating the run command
        FEBfilenameout = str(theta[i])+'.feb'
        print(FEBfilenameout)

        # change the helical twist in the model
        filestrtemp = HTC_write.write_subtendonTwist(filestrtemp,body1,theta[i],length)
        filestrtemp = HTC_write.write_subtendonTwist(filestrtemp,body2,theta[i],length)
        filestrtemp = HTC_write.write_subtendonTwist(filestrtemp,body3,theta[i],length)

        # change aspect ratio of each subtendon along its length
        filestrtemp = HTC_write.write_changeAspectRatioLength(filestrtemp,body1,atop[i],btop[i],abottom[i],bbottom[i],length)
        filestrtemp = HTC_write.write_changeAspectRatioLength(filestrtemp,body2,atop[i],btop[i],abottom[i],bbottom[i],length)
        filestrtemp = HTC_write.write_changeAspectRatioLength(filestrtemp,body3,atop[i],btop[i],abottom[i],bbottom[i],length)
            
        # change the aspect ratio of the two grips
        filestrtemp = HTC_write.write_changeAspectRatioLength(filestrtemp,body1grip,atop[i],btop[i],abottom[i],bbottom[i],length)
        filestrtemp = HTC_write.write_changeAspectRatioLength(filestrtemp,body2grip,atop[i],btop[i],abottom[i],bbottom[i],length)

        FEBfilenameout = HTC_write.write_FEBfile(filestrtemp,FEBfilenameout)

# END OF main()

if __name__ == "__main__":
    main(sys.argv)