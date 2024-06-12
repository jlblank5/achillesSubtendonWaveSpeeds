# FEBIO HTC - Read Library
# Author: Jon Blank (2024)
# Paper: Shear wave propagation in the Achilles subtendons is modulated by helical twist and nonuniform loading
# ======================================================================================================================
# Library defines read functions febio file generation


# reads the base FEBio file and stores it as a string
# filename: name of the .feb file that needs read
def read_baseFile(filename):
    filestr = ""
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            filestr = filestr + line
    return(filestr)
