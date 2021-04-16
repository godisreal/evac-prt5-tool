
#-----------------------------------------------------------------------
# Copyright (C) 2021, All rights reserved
#
# Peng Wang
#
#-----------------------------------------------------------------------
#=======================================================================
# 
# DESCRIPTION:
# This software is developed to analyze and visualize evacuation simulation results from Fire Dynamics Simulator with Evacuation (FDS+Evac).
# FDS+Evac is an open source software package developed by NIST. The source
# code is available at: https://github.com/firemodels/fds
#

import os
from sys import argv, exit
from read_evac import *

print("================================")
print ("Length of input parameters:", len(argv))
print("================================")

# The program will first read prt5 data and then visualize it.  
if len(argv)==2:
    file1 = argv[1]
    if file1:
        if os.path.exists(file1):
            print ('load .fds file and extract evac-related information', file1)
            CHID=readCHID(file1)
            print CHID

            # The following lines are effective only for the latest version of fds as well as fds6_dump205.exe
            # If you are using the old version of fds, please modify the code to read evac prt5 file.  
            readPRTfile(CHID+'_evac_0001.prt5')
            visualizeEvac(CHID+'_evac_0001.npz', file1)
        else:
            print ("Input file %s does not exist!" %file1)
            exit(-1)
    else
        print ('Show help info in readme.txt!')
        if os.path.exists("readme.txt"):
            for line in open("readme.txt"):
                print (line)
        else:
            print ("The file readme.txt is not in this folder.")
            print ("Please search readme.txt in other folders and read it.")
        exit(-1)


# flag is either /readonly or /showonly
# If no flag is given, the program will first read prt5 data and then visualize it.  
if len(argv)==3:
    file1 = argv[1]
    flag = argv[2]
    if file1:
        if os.path.exists(file1):
            print ('load .fds file and extract evac-related information', file1)
            CHID=readCHID(file1)
            print CHID

            # The following lines are effective only for the latest version of fds as well as fds6_dump205.exe
            # If you are using the old version of fds, please modify the code to read evac prt5 file.  
            if flag == '/readonly':
                readPRTfile(CHID+'_evac_0001.prt5')
            elif flag == '/showonly':
                visualizeEvac(CHID+'_evac_0001.npz', file1)
            else:
                print ("The parameter is not accepted.  Please browse readme.txt.")
        else:
            print ("Input file %s does not exist!" %file1)
            exit(-1)
    else:
        print ('Show help info in readme.txt!')
        if os.path.exists("readme.txt"):
            for line in open("readme.txt"):
                print (line)
        else:
            print ("The file readme.txt is not in this folder.")
            print ("Please search readme.txt in other folders and read it.")
        exit(-1)

if len(argv)>3:
    print("Too many input parameters!")
    print("Please browse readme.txt.")
    exit(-1)

    
