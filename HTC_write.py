import re
import csv
import math

# FEBIO HTC - Write Library
# Author: Jon Blank (2024)
# Paper: Shear wave propagation in the Achilles subtendons is modulated by helical twist and nonuniform loading
# ======================================================================================================================
# Library defines several write functions for fEBio file generation

# changes the aspect ratio of the body in question (in x-y plane)
# filestr: .feb filestr
# body: body of interest in model (e.g., Soleus)
# a: major axis radius multiplication factor
# b: minor axis radius multiplication factor
def write_changeAspectRatio(filestr,body,a,b):
    filestrnew = filestr
    reading = 0
    for line in filestr.splitlines():
            if reading:
                if '</Nodes>' in line:
                    reading = 0
                else:
                    splitLine = re.split(",|<|>| ",line)
                    numb = splitLine[-4]; numb = float(numb)*b
                    numa = splitLine[-5]; numa = float(numa)*a
                    outputLine=''.join([splitLine[0],"<",splitLine[1]," ",splitLine[2],">",str(numa),",",str(numb),",",splitLine[5],
                        "<",splitLine[6],">",splitLine[7]])
                    filestrnew = filestrnew.replace(line, outputLine)
            else:
                if '<Nodes name="'+body+'">' in line:
                    reading = 1
    return(filestrnew)

# changes the aspect ratio of the body in question (in x-y plane) (along the length)
# filestr: .feb filestr
# body: body of interest in model (e.g., Soleus)
# atop: proximal major axis radius multiplication factor
# btop: proximal minor axis radius multiplication factor
# abottom: distal major axis radius multiplication factor
# bbottom: distal minor axis radius multiplication factor
# length: proximal-to-distal length of the tissue (in meters)
def write_changeAspectRatioLength(filestr,body,atop,btop,abottom,bbottom,length):
    filestrnew = filestr
    reading = 0
    for line in filestr.splitlines():
            if reading:
                if '</Nodes>' in line:
                    reading = 0
                else:
                    splitLine = re.split(",|<|>| ",line)

                    x = splitLine[-5]; 
                    y = splitLine[-4]; 
                    z = splitLine[-3]; 

                    newx = float(x)*((atop-abottom)*(float(z)/length)+abottom)
                    newy = float(y)*((btop-bbottom)*(float(z)/length)+bbottom)

                    outputLine=''.join([splitLine[0],"<",splitLine[1]," ",splitLine[2],">",str(newx),",",str(newy),",",splitLine[5],
                        "<",splitLine[6],">",splitLine[7]])
                    filestrnew = filestrnew.replace(line, outputLine)
            else:
                if '<Nodes name="'+body+'">' in line:
                    reading = 1
    return(filestrnew)

# changes the twist of subtendons along the tissue length
# filestr: .feb filestr
# body: body of interest in model (e.g., Soleus)
# theta: amount of helical twist (in degrees)
# length: proximal-to-distal length of the tissue (in meters)
def write_subtendonTwist(filestr,body,theta,length):
    filestrnew = filestr
    reading = 0
    for line in filestr.splitlines():
            if reading:
                if '</Nodes>' in line:
                    reading = 0
                else:
                    splitLine = re.split(",|<|>| ",line)
                    numy = splitLine[-4]; numx = splitLine[-5]; numz = splitLine[-3]
                    newtheta = math.pi*theta*(1-float(numz)/length)/180

                    if abs(float(numy))<0.0003 and abs(float(numx))<0.0003:
                        newx = float(numx)
                        newy = float(numy)
                    else:
                        newx = float(numx)*math.cos(newtheta)-float(numy)*math.sin(newtheta)
                        newy = float(numx)*math.sin(newtheta)+float(numy)*math.cos(newtheta)

                    outputLine=''.join([splitLine[0],"<",splitLine[1]," ",splitLine[2],">",str(newx),",",str(newy),",",splitLine[5],
                        "<",splitLine[6],">",splitLine[7]])
                    filestrnew = filestrnew.replace(line, outputLine)
            else:
                if '<Nodes name="'+body+'">' in line:
                    reading = 1
    return(filestrnew)


# specifies the load applied at the top grip
# filestr: .feb filestr
# name: body of interest in model (e.g., Soleus)
# lc: load curve of interest (hard-coded in .py file)
# F: force level to prescribe
def write_load(filestr,name,lc,F):
    filestrnew = filestr
    reading = 0
    for line in filestr.splitlines():
        if '</nodal_load>' in line:
            reading = 0
        if reading:
            if '<scale lc="'+lc+'"' in line:
                outputLine = '\t\t\t<scale lc="'+lc+'">' + str(F) + '</scale>'
                filestrnew = filestrnew.replace(line, outputLine)
                reading = 0
        if '<nodal_load name="'+name+'" type="nodal_load"' in line:
            reading = 1
    return(filestrnew)

# writes the .feb file
# filestr: .feb filestr
# filenameout: name of the .feb file
def write_FEBfile(filestr,filenameout):
    with open(filenameout, 'w') as f:
        f.write(filestr)
    return(filenameout)

# write parameters to a .txt file to keep track
# gfwrite: gastrocnemius force to write to file (array)
# swrite: soleus force to write to file (array)
# filenamewrite: name of the file corresponding to each load level
# filenameout: name of the fil to return
def write_parametersSubtendonsGS(gfwrite,sfwrite,filenamewrite,filenameout):

    with open(filenameout, 'w') as f:
        fieldnames = ['G_force','S_force','filename']
        header = csv.DictWriter(f,fieldnames)
        writer = csv.writer(f,delimiter='\t')
        header.writeheader()
        writer.writerows(zip(gfwrite,sfwrite,filenamewrite))
    return(filenameout)