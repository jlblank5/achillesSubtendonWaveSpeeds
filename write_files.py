import os
import sys
import csv
import HTC_read
import HTC_write

def usage(argv):
    print('USAGE: ' + argv[0])

# FEBIO File Generation Code
# Author: Jon Blank (2024)
# Paper: Shear wave propagation in the Achilles subtendons is modulated by helical twist and nonuniform loading
# ======================================================================================================================
# This code writes out .feb files of different helical twist conditions to load levels corresponding to human gait

def main(argv):

    # Check for appropriate usage
    if len(argv) != 1:
        usage(argv)
        sys.exit(1)

    # change your directory to the location of the .feb files
    baseModelsDir = r"C:\.feb" # this is the directory where the 0,10,20.feb (and so on) .feb files are stored
    os.chdir(baseModelsDir)

    FEBfilename=[]

    # specify the FEBio file to write to
    FEBfilename.append("0.feb")
    FEBfilename.append("10.feb")
    FEBfilename.append("20.feb")
    FEBfilename.append("30.feb")
    FEBfilename.append("40.feb")
    FEBfilename.append("50.feb")
    FEBfilename.append("60.feb")
    FEBfilename.append("70.feb")
    FEBfilename.append("80.feb")
    FEBfilename.append("90.feb")
    FEBfilename.append("100.feb")
    FEBfilename.append("110.feb")
    FEBfilename.append("120.feb")
    FEBfilename.append("130.feb")
    FEBfilename.append("140.feb")
    FEBfilename.append("150.feb")
    FEBfilename.append("160.feb")
    FEBfilename.append("170.feb")
    FEBfilename.append("180.feb")

    # read the files and store them in filestr
    filestr=[]
    for i in range(0,len(FEBfilename)):
        filestr.append(HTC_read.read_baseFile(FEBfilename[i]))

    # # change your directory to where you want to store the output files
    dir = r"C:\simulations"
    os.chdir(dir)

    # name the output simulation to each input folder
    filename = 'model.feb'

    # read the gastroc prescribed load levels
    f=open("G_fp50.csv"); G_f = []
    for row in csv.reader(f):
        G_f=row
        
    # read the soleus prescribed load levels
    f=open("S_fp50.csv"); S_f = []
    for row in csv.reader(f):
        S_f=row

    # number of models to generate (right now it is 1900)
    nModels = len(S_f)

    # define base directory
    os.chdir(dir)

    # write parameter file
    gfwrite=[]; sfwrite=[]; filenamewrite=[]    
    for i in range(0,nModels):
        for j in range(0,len(filestr)):
            gfwrite.append(str(G_f[i]))
            sfwrite.append(str(S_f[i]))
            filenamewrite.append(FEBfilename[j])

    # write out the data used in each FEB file
    HTC_write.write_parametersSubtendonsGS(gfwrite,sfwrite,filenamewrite,'simulation_parameters.txt')

    counter=0
    for i in range(0,nModels):
        for j in range(0,len(filestr)):

            # filestrtemp = filestr[j]
            filestrtemp = filestr[j]

            # initialize by recording the base model and creating the run command
            FEBfilenameout = filename

            print(dir + "\\inputs\\" + str(counter))
            os.makedirs(dir + "\\inputs\\" + str(counter))
            os.makedirs(dir + "\\results\\" + str(counter))
            os.chdir(dir + "\\inputs\\" + str(counter))

            # change the load applied to subtendons
            filestrtemp = HTC_write.write_load(filestrtemp,"S_force","2",S_f[i])
            filestrtemp = HTC_write.write_load(filestrtemp,"G_force","3",G_f[i])

            # write the .feb file to the current directory
            FEBfilenameout = HTC_write.write_FEBfile(filestrtemp,FEBfilenameout)

            counter+=1       
        
# END OF main()

if __name__ == "__main__":
    main(sys.argv)