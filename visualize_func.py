
import math
import re
import csv
import numpy as np
#import matplotlib.pyplot as plt
import pygame
from read_evac import *
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")

red=255,0,0
green=0,255,0
blue=0,0,255
white=255,255,255
yellow=255,255,0
IndianRed=205,92,92
tan = 210,180,140
skyblue = 135,206,235
orange = 255,128,0
khaki = 240,230,140
black = 0,0,0
purple = 160, 32, 240
magenta = 255, 0, 255
lightpink =255, 174, 185
lightblue =178, 223, 238
cyan = 0, 255, 255
lightcyan = 224, 255, 255
lightgreen = 193, 255, 193

####################
# Drawing the walls
####################
def drawWalls(screen, walls, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for wall in walls:
        
        if wall.inComp == 0:
            continue
        
        if wall.mode=='line':
            startPos = np.array([wall.params[0],wall.params[1]]) #+xyShift
            endPos = np.array([wall.params[2],wall.params[3]]) #+xyShift
            startPx = startPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            endPx = endPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            pygame.draw.line(screen, red, startPx+xyShift, endPx+xyShift, 2)
            

            if SHOWDATA:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
                screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
                text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
                screen.blit(text_surface, endPos*ZOOMFACTOR +xyShift)

        elif wall.mode=='rect':
            x= ZOOMFACTOR*wall.params[0]
            y= ZOOMFACTOR*wall.params[1]
            w= ZOOMFACTOR*(wall.params[2] - wall.params[0])
            h= ZOOMFACTOR*(wall.params[3] - wall.params[1])
            
            pygame.draw.rect(screen, red, [x+xSpace, y+ySpace, w, h], 2)

            if SHOWDATA:
                pass
                startPos = np.array([wall.params[0],wall.params[1]])
                endPos = np.array([wall.params[2],wall.params[3]])

                myfont=pygame.font.SysFont("arial",10)

                #text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
                #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

                #text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
                #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)


def drawSingleWall(screen, wall, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0, lw=2.0):

    xyShift = np.array([xSpace, ySpace])
    if wall.inComp == 0:
        print('Error: Draw a wall that is not in Computation!\n')
        return
    
    if wall.mode=='line':
        startPos = np.array([wall.params[0],wall.params[1]]) #+xyShift
        endPos = np.array([wall.params[2],wall.params[3]]) #+xyShift
        startPx = startPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
        endPx = endPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
        pygame.draw.line(screen, red, startPx+xyShift, endPx+xyShift, lw)
        

        if SHOWDATA:
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
            text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
            screen.blit(text_surface, endPos*ZOOMFACTOR +xyShift)

    elif wall.mode=='rect':
        x= ZOOMFACTOR*wall.params[0]
        y= ZOOMFACTOR*wall.params[1]
        w= ZOOMFACTOR*(wall.params[2] - wall.params[0])
        h= ZOOMFACTOR*(wall.params[3] - wall.params[1])
        
        pygame.draw.rect(screen, red, [x+xSpace, y+ySpace, w, h], lw)

        if SHOWDATA:
            pass
            startPos = np.array([wall.params[0],wall.params[1]])
            endPos = np.array([wall.params[2],wall.params[3]])

            myfont=pygame.font.SysFont("arial",10)

            #text_surface=myfont.render(str(startPos), True, purple, (255,255,255))
            #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            #text_surface=myfont.render(str(endPos), True, purple, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)
    

    ####################
    # Drawing the doors
    ####################

def drawDoors(screen, doors, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for door in doors:

        if door.inComp == 0:
            continue
        
        #startPos = np.array([door[0], door[1]])
        #endPos = np.array([door[2], door[3]])

        startPos = np.array([door.params[0],door.params[1]]) #+xyShift
        endPos = np.array([door.params[2],door.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*door.params[0] 
        y= ZOOMFACTOR*door.params[1] 
        w= ZOOMFACTOR*(door.params[2] - door.params[0])
        h= ZOOMFACTOR*(door.params[3] - door.params[1])
            
        pygame.draw.rect(screen, green, [x+ xSpace, y+ ySpace, w, h], 2)

        if SHOWDATA:
            
            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render('Door:'+str(door.oid)+'/'+str(door.name)+'/'+str(door.arrow), True, green, black)
            screen.blit(text_surface, door.pos*ZOOMFACTOR+xyShift)


def drawSingleDoor(screen, door, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0, lw=2.0):

    xyShift = np.array([xSpace, ySpace])
    if door.inComp == 0:
        print('Error: Draw a door that is not in Computation!\n')
        return
    
    #startPos = np.array([door[0], door[1]])
    #endPos = np.array([door[2], door[3]])

    startPos = np.array([door.params[0],door.params[1]]) #+xyShift
    endPos = np.array([door.params[2],door.params[3]]) #+xyShift

    #Px = [0, 0]
    #Px[0] = int(Pos[0]*ZOOMFACTOR)
    #Px[1] = int(Pos[1]*ZOOMFACTOR)
    #pygame.draw.circle(screen, red, Px, LINESICKNESS)

    x= ZOOMFACTOR*door.params[0] 
    y= ZOOMFACTOR*door.params[1] 
    w= ZOOMFACTOR*(door.params[2] - door.params[0])
    h= ZOOMFACTOR*(door.params[3] - door.params[1])
        
    pygame.draw.rect(screen, green, [x+ xSpace, y+ ySpace, w, h], lw)

    if SHOWDATA:
        
        myfont=pygame.font.SysFont("arial",10)
        text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
        screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

        #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
        #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

        myfont=pygame.font.SysFont("arial",13)
        text_surface=myfont.render('Door:'+str(door.oid)+'/'+str(door.name)+'/'+str(door.arrow), True, green, black)
        screen.blit(text_surface, door.pos*ZOOMFACTOR+xyShift)


    ####################
    # Drawing the exits
    ####################

def drawExits(screen, exits, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for exit in exits:

        if exit.inComp == 0:
            continue

        startPos = np.array([exit.params[0],exit.params[1]]) #+xyShift
        endPos = np.array([exit.params[2],exit.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*exit.params[0]
        y= ZOOMFACTOR*exit.params[1]
        w= ZOOMFACTOR*(exit.params[2] - exit.params[0])
        h= ZOOMFACTOR*(exit.params[3] - exit.params[1])
            
        pygame.draw.rect(screen, orange, [x+ xSpace, y+ ySpace, w, h], 2)

        if SHOWDATA:

            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR + xyShift)

            #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR + xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render('Exit:'+str(exit.oid)+'/'+str(exit.name)+'/'+str(exit.arrow), True, red, white)
            screen.blit(text_surface, exit.pos*ZOOMFACTOR + xyShift)


def drawSingleExit(screen, exit, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0, lw=2.0):

    xyShift = np.array([xSpace, ySpace])
    if exit.inComp == 0:
        print('Error: Draw an exit that is not in Computation!\n')
        return

    startPos = np.array([exit.params[0],exit.params[1]]) #+xyShift
    endPos = np.array([exit.params[2],exit.params[3]]) #+xyShift

    #Px = [0, 0]
    #Px[0] = int(Pos[0]*ZOOMFACTOR)
    #Px[1] = int(Pos[1]*ZOOMFACTOR)
    #pygame.draw.circle(screen, red, Px, LINESICKNESS)

    x= ZOOMFACTOR*exit.params[0]
    y= ZOOMFACTOR*exit.params[1]
    w= ZOOMFACTOR*(exit.params[2] - exit.params[0])
    h= ZOOMFACTOR*(exit.params[3] - exit.params[1])
        
    pygame.draw.rect(screen, orange, [x+ xSpace, y+ ySpace, w, h], lw)

    if SHOWDATA:

        myfont=pygame.font.SysFont("arial",10)
        text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
        screen.blit(text_surface, startPos*ZOOMFACTOR + xyShift)

        #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
        #screen.blit(text_surface, endPos*ZOOMFACTOR + xyShift)

        myfont=pygame.font.SysFont("arial",13)
        text_surface=myfont.render('Exit:'+str(exit.oid)+'/'+str(exit.name)+'/'+str(exit.arrow), True, red, white)
        screen.blit(text_surface, exit.pos*ZOOMFACTOR + xyShift)


def drawDirection(screen, door, arrow, ZOOMFACTOR=10.0, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    
    if arrow == 1:
        direction = np.array([1.0, 0.0])
    elif arrow == -1:
        direction = np.array([-1.0, 0.0])
    elif arrow == 2:
        direction = np.array([0.0, 1.0])
    elif arrow == -2:
        direction = np.array([0.0, -1.0])
    elif arrow == 0:
        direction = np.array([0.0, 0.0])
    
    startPx=door.pos
    endPx=door.pos+direction
    pygame.draw.line(screen, green, startPx*ZOOMFACTOR+xyShift, endPx*ZOOMFACTOR+xyShift, 2)

    #dir = endPx - startPx
    #dir2 = np.array([-dir[0], dir[1]])
    #dir2 = normalize(dir2)
    #arrowPx = endPx - dir*0.2
    #arrowPx1 = arrowPx + 0.6*dir2
    #arrowPx2 = arrowPx - 0.6*dir2
    #pygame.draw.line(screen, green, endPx*ZOOMFACTOR+xyShift, arrowPx1*ZOOMFACTOR+xyShift, 2)
    #pygame.draw.line(screen, green, endPx*ZOOMFACTOR+xyShift, arrowPx2*ZOOMFACTOR+xyShift, 2)



##############################################
# Drawing the obstructions in FDS input data
##############################################
def drawOBST(screen, walls, color, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for wall in walls:
        
        if wall.inComp == 0:
            continue
        
        if wall.mode=='line':
            startPos = np.array([wall.params[0],wall.params[1]]) #+xyShift
            endPos = np.array([wall.params[2],wall.params[3]]) #+xyShift
            startPx = startPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            endPx = endPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            pygame.draw.line(screen, red, startPx+xyShift, endPx+xyShift, 2)
            

            if SHOWDATA:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(str(startPos), True, (255,0,0), (255,255,255))
                screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
                text_surface=myfont.render(str(endPos), True, (255,0,0), (255,255,255))
                screen.blit(text_surface, endPos*ZOOMFACTOR +xyShift)

        elif wall.mode=='rect':
            x= ZOOMFACTOR*wall.params[0]
            y= ZOOMFACTOR*wall.params[1]
            w= ZOOMFACTOR*(wall.params[2] - wall.params[0])
            h= ZOOMFACTOR*(wall.params[3] - wall.params[1])
            
            pygame.draw.rect(screen, color, [x+xSpace, y+ySpace, w, h], 2)

            if SHOWDATA:
                pass
                startPos = np.array([wall.params[0],wall.params[1]])
                endPos = np.array([wall.params[2],wall.params[3]])

                myfont=pygame.font.SysFont("arial",10)

                #text_surface=myfont.render(str(startPos), True, red, (255,255,255))
                #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

                #text_surface=myfont.render(str(endPos), True, red, (255,255,255))
                #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

   

#####################################################################
# Drawing the path like holes,  doors, etc. from FDS input data
#####################################################################
def drawPATH(screen, doors, color, ZOOMFACTOR=10.0, SHOWDATA=False, xSpace=0.0, ySpace=0.0):

    xyShift = np.array([xSpace, ySpace])
    for door in doors:

        if door.inComp == 0:
            continue
        
        #startPos = np.array([door[0], door[1]])
        #endPos = np.array([door[2], door[3]])

        startPos = np.array([door.params[0],door.params[1]]) #+xyShift
        endPos = np.array([door.params[2],door.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*door.params[0] 
        y= ZOOMFACTOR*door.params[1] 
        w= ZOOMFACTOR*(door.params[2] - door.params[0])
        h= ZOOMFACTOR*(door.params[3] - door.params[1])
            
        pygame.draw.rect(screen, color, [x+ xSpace, y+ ySpace, w, h], 2)

        if SHOWDATA:
            
            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render('ID'+str(door.id)+'/'+str(door.arrow), True, blue, (255,255,255))
            screen.blit(text_surface, door.pos*ZOOMFACTOR+xyShift)



def visualizeTpre(fname, evacfile=None, fdsfile=None, Zmin=0.0, Zmax=3.0, showdata=True):
    
    # Plot pre-movement time by using matplotlib
 

    # np.load has some unexpected problem for latest version of numpy in python3.  Thus I will not use this stuff.  
    # If anyone wants to help to debug the following lines, I will appreciate.  
    
    #prtdata = np.load(fname) #load .npz file
    #Time = prtdata["arr_0"]
    #XYZ = prtdata["arr_1"]
    #TAG = prtdata["arr_2"]
    #INFO = prtdata["arr_3"]
    #print("TAG:", TAG)
     
    # Extract data from binary data file
    Time, XYZ, TAG, INFO, n_part, n_agents, n_quant = readPRTfile(fname)
    T_END = len(Time)
    print('T_END:', T_END)

    T_INDEX=0
    arrayTpre = np.zeros((n_agents, T_END))  
             
    for T_INDEX in range(T_END):
        
        Time_t = Time[T_INDEX]
        XYZ_t = XYZ[T_INDEX]
        TAG_t = TAG[T_INDEX]
        INFO_t = INFO[T_INDEX]
        
        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        if np.size(TAG_t)==1:
            TAG_t = np.array([TAG_t])
        print(TAG_t)
        
        for idai in range(np.size(TAG_t)):
            #print(TAG_t[idai])
            arrayTpre[int(TAG_t[idai]), T_INDEX] = INFO_t[14][idai]
    
    print('Shape of arrayTpre:', np.shape(arrayTpre))
    print('arrayTpre:', arrayTpre)
    
    (NRow, NColomn) = np.shape(arrayTpre)  
    if showdata:
        for i in range(NRow):
            plt.plot(Time, arrayTpre[i,:], linewidth=2.0, label=str(i))
            #plt.plot(arrayTpre[i,:], linewidth=3.0, label=str(i))
            plt.text(0, arrayTpre[i,0], str(i), fontsize=18)
        plt.plot(Time, Time, linestyle='-.', linewidth=3.0)
        #plt.plot(arrayTpre)
        plt.title("Pre-movement Time")
        plt.grid()
        plt.legend(loc='best')
        plt.show()
        
    return arrayTpre


# Find the first &MESH line in FDS input file and return the value
def plotDoorProb(FileName, doorIndex=0):
    findMESH=False
    doorProb=[]
    for line in open(FileName):
        if re.match('&DoorProb', line):
            findMESH=True
            row=[]
        if  findMESH:
            if re.search('prob=', line):
                dataTemp=line.split('prob=')
                #print('dataTemp:', dataTemp[1:])

                #for index in range(len(dataTemp[1:])):
                #    probDist=dataTemp[index+1].lstrip('[').strip('=').rstrip(']')
                probDist=dataTemp[1].lstrip('[').strip('=').rstrip(']')
                temp2 =  re.split(r'[\s\,]+', probDist)
                print(temp2)
                prob = float(temp2[doorIndex].lstrip('[').strip('=').rstrip(']'))
                row.append(prob)
                #print(row)

                    #xpoints = temp2[0]
                    #ypoints = temp2[1]
            '''
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            '''
            if re.search('WellDone!', line):
                findMESH = False
                #doorProb.append(dataTemp[1:])
                doorProb.append(row)
                # return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored

    print('doorProb', doorProb)
    (NRow, NColomn) = np.shape(doorProb)  
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(doorProb[i][j])
    print('matrix', matrix)
    print(len(matrix))
    plt.figure()
    plt.plot(matrix)
    temp=FileName.split('.')
    fnamePNG = temp[0]+'_exitprob.png'
    plt.savefig(fnamePNG)
    plt.show()
    return matrix


def readDoorProb(FileName, doorIndex, showdata=True):
    findMESH=False
    doorProb=[]
    timeIndex= []
    for line in open(FileName):
        if re.match('&DoorProb', line):
            findMESH=True
            row=[]
        if  findMESH:
            if re.search('prob=', line):
                dataTemp=line.split('prob=')
                #print('dataTemp:', dataTemp[1:])

                #for index in range(len(dataTemp[1:])):
                #    probDist=dataTemp[index+1].lstrip('[').strip('=').rstrip(']')
                probDist=dataTemp[1].lstrip('[').strip('=').rstrip(']')
                temp2 =  re.split(r'[\s\,]+', probDist)
                print(temp2)
                prob = float(temp2[doorIndex+1].lstrip('[').strip('=').rstrip(']'))
                row.append(prob)
                #print(row)
            if re.search('SimulationTime=', line):
                dataTemp=line.split('=')
                timeIndex.append(float(dataTemp[1].lstrip().rstrip()))
                    #xpoints = temp2[0]
                    #ypoints = temp2[1]
            '''
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            '''
            if re.search('WellDone!', line):
                findMESH = False
                #doorProb.append(dataTemp[1:])
                doorProb.append(row)
                # return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored

    print('doorProb', doorProb)
    (NRow, NColomn) = np.shape(doorProb)  
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(doorProb[i][j])
    print('matrix', matrix)
    print('sizeOfMatrix:', np.shape(matrix))
    print('sizeOfTimeIndex:', np.shape(timeIndex))
    #print(timeIndex)
    if showdata:
        for j in range(NColomn):
            plt.plot(timeIndex, matrix[:,j], linewidth=3.0, label=str(j))
            plt.text(0,matrix[0,j], str(j), fontsize=18)
        plt.title("exit index:"+str(doorIndex))
        plt.grid()
        plt.legend(loc='best')
        temp=FileName.split('.')
        fnamePNG = temp[0]+'_exitprob.png'
        plt.savefig(fnamePNG)
        plt.show()
    return matrix

# This function is used for visualization of FDS+Evac prt5 data file
# Because FDS+Evac is not officially maintained by NIST and VTT, this function is not very useful now.  
def visualizeFdsEvac(fname, fdsfile=None, Zmin=0.0, Zmax=3.0):
    
    # Because visualizeEvac is a 2D visualizer, we can only show agents in a single floors each time and if there are multiple floors in fds+evac simulation, users should specify which floor they want to visualize.  Otherwise there will be overlap of agents in different floors.  The default values are given by Zmin=0.0 and Zmax=3.0, which means the gound floor approximately.  
 
     # Therefore It is recommended for users to first open .fds input file to see if there are multiple floors.  User should specify Zmin and Zmax and agents are visualized in z axis between Zmin and Zmax.  
        
    #Zmin is the lower bound of z values in a floor (e.g., often z lower bound of an evacuation mesh)
    #Zmax is the upper bound of z values in a floor (e.g., often z upper bound of an evacuation mesh)


    # np.load has some unexpected problem for latest version of numpy in python3.  Thus I will not use this stuff.  
    # If anyone wants to help to debug the following lines, I will appreciate.  
    
    #prtdata = np.load(fname) #load .npz file
    #Time = prtdata["arr_0"]
    #XYZ = prtdata["arr_1"]
    #TAG = prtdata["arr_2"]
    #INFO = prtdata["arr_3"]
    #print("TAG:", TAG)
    
    # If there are already .txt data extracted from .prt5 file, the visualizer will not repeat to write .txt file because it may be time-consuming.  
    temp = fname.split('.prt5')
    outtxt = temp[0]+".txt"
    if os.path.exists(outtxt):
        wrtxt=False
    else:
        wrtxt=True
     
    # Extract data from .prt5 data file
    Time, XYZ, TAG, INFO, n_part, version, n_quant = readPRTfile(fname, wrtxt)
        
    T_END = len(Time)
    if debugPygame:
        print ("Length of time axis in prt5 data file", T_END)
        print ("T_Initial=", Time[0])
        print ("T_Final=", Time[T_END-1])
    T_INDEX=0

    if fdsfile!=None:
        #meshes, evacZmin, evacZmax = readMESH(fdsfile, 'evac')
        #N_meshes = len(meshes)
        #evacZoffset=0.5*(evacZmin+evacZmax)
        
        walls=readOBST(fdsfile, '&OBST', Zmin, Zmax)
        holes=readPATH(fdsfile, '&HOLE', Zmin, Zmax)
        exits=readPATH(fdsfile, '&EXIT', Zmin, Zmax)
        doors=readPATH(fdsfile, '&DOOR', Zmin, Zmax)
        entries=readPATH(fdsfile, '&ENTRY', Zmin, Zmax)
        
    
    ZOOMFACTOR=10.0
    xSpace=20.0
    ySpace=20.0
    MODETRAJ=False
    SHOWTIME=True
    SHOWWALLDATA=True
    SHOWDOORDATA=True
    SHOWEXITDATA=True
    PAUSE=False
    REWIND=False
    FORWARD=False
    
    pygame.init()
    screen = pygame.display.set_mode([800, 350])
    pygame.display.set_caption('Visualize prt5 file for evac simulation')
    clock = pygame.time.Clock()
    #screen.fill(white)

    #myfont=pygame.font.SysFont("arial",16)
    #text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
    #screen.blit(text_surface, (16,20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                #button = pygame.mouse.get_pressed()            
            # elif event.type == pygame.MOUSEBUTTONUP:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    ZOOMFACTOR = ZOOMFACTOR +1
                elif event.key == pygame.K_PAGEDOWN:
                    ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
                elif event.key == pygame.K_t:
                    MODETRAJ = not MODETRAJ
                elif event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                elif event.key == pygame.K_HOME:
                    REWIND = True
                    PAUSE = True
                    #xSpace=xSpace-10
                elif event.key == pygame.K_END:
                    FORWARD = True
                    PAUSE = True
                    #xSpace=xSpace+10
                #elif event.key == pygame.K_v:
                 #   simu.SHOWVELOCITY = not simu.SHOWVELOCITY
                #elif event.key == pygame.K_i:
                 #   simu.SHOWINDEX = not simu.SHOWINDEX
                #elif event.key == pygame.K_d:
                 #   simu.DRAWDOORFORCE = not simu.DRAWDOORFORCE
                #elif event.key == pygame.K_r:
                #    simu.DRAWSELFREPULSION = not simu.DRAWSELFREPULSION
                elif event.key == pygame.K_KP1:
                    SHOWWALLDATA = not SHOWWALLDATA
                elif event.key == pygame.K_KP2:
                    SHOWDOORDATA = not SHOWDOORDATA
                elif event.key == pygame.K_KP3:
                    SHOWEXITDATA = not SHOWEXITDATA
                #elif event.key == pygame.K_s:
                #    simu.SHOWSTRESS = not simu.SHOWSTRESS
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10

        if MODETRAJ == False:
            screen.fill([0,0,0])

        #Time  = readFRec(fin,'f')  # Time index
        if T_INDEX == None or T_INDEX==T_END-1:
            print("Simulation End!")
            #running=False
            #pygame.display.quit()
            PAUSE=True
        else:
            if PAUSE==False:
                T_INDEX = T_INDEX+1
            else:
                if REWIND and T_INDEX>0:
                    T_INDEX = T_INDEX-1
                if FORWARD and T_INDEX<T_END-1:
                    T_INDEX = T_INDEX+1
        #nplim = readFRec(fin,'I')  # Number of particles in the PART class
        
        Time_t = Time[T_INDEX]
        XYZ_t = XYZ[T_INDEX]
        TAG_t = TAG[T_INDEX]
        INFO_t = INFO[T_INDEX]

        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        if np.size(TAG_t)==1:
            TAG_t = np.array([TAG_t])
            
        #############################
        ######### Drawing Process ######
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if SHOWTIME:
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Simulation Time:" + str(Time_t), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [620,300]) #[750,350]*ZOOMFACTOR)

        if fdsfile!=None:
            drawOBST(screen, walls, red, ZOOMFACTOR, SHOWWALLDATA, xSpace, ySpace)
            drawPATH(screen, holes, green, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
            drawPATH(screen, exits, lightpink, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)
            drawPATH(screen, doors, green, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)
            drawPATH(screen, entries, purple, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)

        if debugPygame:
            print ("Show TAG_t: ", TAG_t)
        
        ################################
        # Next step is drawing agents by using evac data
        ################################  
        for idai in range(np.size(TAG_t)):

            if XYZ_t[2][idai]<Zmin or XYZ_t[2][idai]>Zmax:
                continue
            #scPos = np.array([0, 0])
            scPos = [0, 0]
            scPos[0] = int(XYZ_t[0][idai]*ZOOMFACTOR+xSpace)
            scPos[1] = int(XYZ_t[1][idai]*ZOOMFACTOR+ySpace)
            
            '''
            if n_quant>1:
                desiredV = [0, 0]
                desiredV[0]=(XYZ_t[0][idai]+INFO_t[0][idai])*ZOOMFACTOR+xSpace
                desiredV[1]=(XYZ_t[1][idai]+INFO_t[1][idai])*ZOOMFACTOR+ySpace
                pygame.draw.line(screen, red, scPos, desiredV, 2)            
                        
            if n_quant>3:
                actualV = [0, 0]
                actualV[0]=(XYZ_t[0][idai]+INFO_t[2][idai])*ZOOMFACTOR+xSpace
                actualV[1]=(XYZ_t[1][idai]+INFO_t[3][idai])*ZOOMFACTOR+ySpace
                pygame.draw.line(screen, green, scPos, actualV, 2)
            '''
            
            color_para = [255, 0, 0]
            #color_para[0] = int(255*min(1, agent.ratioV))
            pygame.draw.circle(screen, color_para, scPos, int(2.0), 2)
            #pygame.draw.circle(screen, color_para, scPos, int(0.2*ZOOMFACTOR), 2)           
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)

        REWIND=False
        FORWARD=False
        pygame.display.flip()
        clock.tick(20)


# This function is mainly used for our simulation platform crowdEgress and socialArray
def visualizeAgent(fname, evacfile=None, fdsfile=None, ZOOMFACTOR=10.0, xSpace=20.0, ySpace=20.0, Zmin=0.0, Zmax=3.0, debug=False):
    
    # Because visualizeEvac is a 2D visualizer, we can only show agents in a single floors each time and if there are multiple floors in fds+evac simulation, users should specify which floor they want to visualize.  Otherwise there will be overlap of agents in different floors.  The default values are given by Zmin=0.0 and Zmax=3.0, which means the gound floor approximately.  
 
     # Therefore It is recommended for users to first open .fds input file to see if there are multiple floors.  User should specify Zmin and Zmax and agents are visualized in z axis between Zmin and Zmax.  
        
    #Zmin is the lower bound of z values in a floor (e.g., often z lower bound of an evacuation mesh)
    #Zmax is the upper bound of z values in a floor (e.g., often z upper bound of an evacuation mesh)


    # np.load has some unexpected problem for latest version of numpy in python3.  Thus I will not use this stuff.  
    # If anyone wants to help to debug the following lines, I will appreciate.  
    
    #prtdata = np.load(fname) #load .npz file
    #Time = prtdata["arr_0"]
    #XYZ = prtdata["arr_1"]
    #TAG = prtdata["arr_2"]
    #INFO = prtdata["arr_3"]
    #print("TAG:", TAG)
     
    # Extract data from binary data file
    Time, XYZ, TAG, INFO, n_part, n_agents, n_quant = readPRTfile(fname)
    agentsPos = np.zeros((n_agents, 2))

    temp=fname.split('.')
    fnameNPZ = temp[0]+'.npz'
    fnameCSV = temp[0]+'.csv'
    fnameTXT = temp[0]+'.txt' 
    
    
    #if simu.dumpBin:
    #    fbin.close()
    #    np.savez(simu.outDataName +'.npz', npzTime, npzSee, npzComm, npzTalk, npzP, npzD, npzC, npzB, npzA, npzRadius, npzMass)
       
    # Read in data from npz matrix data file
    if os.path.exists(fnameNPZ):
        try:
            agentdata=np.load(fnameNPZ)
            npzTime = agentdata["arr_0"]
            npzSee = agentdata["arr_1"]
            npzComm = agentdata["arr_2"]
            npzTalk = agentdata["arr_3"]
            npzP = agentdata["arr_4"]
            npzD = agentdata["arr_5"]
            npzC = agentdata["arr_6"]
            npzB = agentdata["arr_7"]
            npzA = agentdata["arr_8"]
            npzVD = agentdata["arr_9"]
            npzVE = agentdata["arr_10"]
            npzEP = agentdata["arr_11"]
            npzRadius = agentdata["arr_12"]
            npzMass = agentdata["arr_13"]
        except:
            agentdata=np.load(fnameNPZ)
            npzTime = agentdata["arr_0"]
            npzSee = agentdata["arr_1"]
            npzComm = agentdata["arr_2"]
            npzTalk = agentdata["arr_3"]
            npzP = agentdata["arr_4"]
            npzD = agentdata["arr_5"]
            npzC = agentdata["arr_6"]
            npzB = agentdata["arr_7"]
            npzA = agentdata["arr_8"]
            print("No npz data for visible door/exit and exit probabilit! \n ")
            print("No npz data for agent radius and mass! \n Please check! \n")
            
            
        T_END_Check = len(npzTime)
        npzflag=True
    else:
        T_END_Check = len(Time)
        npzflag=False
    
    T_END = len(Time)
    print('T_END_npz:', T_END_Check)
    print('T_END:', T_END)
    
    if T_END != T_END_Check and debug:
        if sys.version_info[0] == 2:
            raw_input('\nWarning: T_END_BIN != T_END_NPZ \n Please check!')
        if sys.version_info[0] == 3:
            input('\nWarning: T_END_BIN != T_END_NPZ \n Please check!')
    
    if debug:
        print ("Length of time axis in prt5 data file", T_END, T_END_Check)
        print ("T_Initial=", Time[0])
        print ("T_Final=", Time[T_END-1])
        
    T_INDEX=0
    
    walls=[]
    doors=[]
    exits=[]
    
    
    if evacfile!="" and evacfile!="None" and evacfile is not None:
        walls = readWalls(evacfile)  #readWalls(FN_Walls) #readWalls("obstData2018.csv")
        doors = readDoors(evacfile)
        exits = readExits(evacfile)
    
    if fdsfile!="" and fdsfile!="None" and fdsfile is not None and len(walls)+len(doors)+len(exits)==0:
        #meshes, evacZmin, evacZmax = readMESH(fdsfile, 'evac')
        #N_meshes = len(meshes)
        #evacZoffset=0.5*(evacZmin+evacZmax)
        
        walls=readOBST(fdsfile, '&OBST', Zmin, Zmax)
        doors=readPATH(fdsfile, '&HOLE', Zmin, Zmax) #+readPATH(fdsfile, '&DOOR', Zmin, Zmax)+readPATH(fdsfile, '&ENTRY', Zmin, Zmax)
        exits=readEXIT(fdsfile, '&EXIT', Zmin, Zmax)
        #doors=doors+readPATH(fdsfile, '&DOOR', Zmin, Zmax)
        #entries=readPATH(fdsfile, '&ENTRY', Zmin, Zmax)
    
    if os.path.exists(fnameCSV) and len(walls)+len(doors)+len(exits)==0:
        walls = readWalls(fnameCSV)
        doors = readDoors(fnameCSV)
        exits = readExits(fnameCSV)
        
    elif os.path.exists(fnameTXT) and len(walls)+len(doors)+len(exits)==0:
        walls = readWalls(fnameTXT)
        doors = readDoors(fnameTXT)
        exits = readExits(fnameTXT)
    
    MODETRAJ=False
    SHOWTIME=True

    SHOWVELOCITY=True
    SHOWINDEX=True
    SHOWFORCE=False
    SHOWTPRE=False
    SHOWRATIOV=False
    SHOWSTRESS=False
    
    SHOWWALLDATA=True
    SHOWDOORDATA=False
    SHOWEXITDATA=True
    
    PAUSE=True
    REWIND=False
    FORWARD=False
    TimeInterval=260
    
    agentIndex=-1
    agentIndex2=0
    drawLine = False
    
    pygame.init()
    screen = pygame.display.set_mode([900, 650])
    pygame.display.set_caption('Visualize data file for evac simulation')
    clock = pygame.time.Clock()
    #screen.fill(white)

    #myfont=pygame.font.SysFont("arial",16)
    #text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
    #screen.blit(text_surface, (16,20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                mouse_pos = np.array([mouseX, mouseY])
                px1 = (mouse_pos-xyShift)*(1/ZOOMFACTOR)
                drawLine = False

                #button = pygame.mouse.get_pressed()            
            elif event.type == pygame.MOUSEBUTTONUP:
                (mouseX2, mouseY2) = pygame.mouse.get_pos()
                mouse_pos2 = np.array([mouseX2, mouseY2])
                px2 = (mouse_pos2-xyShift)*(1/ZOOMFACTOR)
                drawLine = True
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    ZOOMFACTOR = ZOOMFACTOR +1
                elif event.key == pygame.K_PAGEDOWN:
                    ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
                    
                elif event.key == pygame.K_t:
                    MODETRAJ = not MODETRAJ
                elif event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                elif event.key == pygame.K_HOME:
                    REWIND = True
                    PAUSE = True
                    #xSpace=xSpace-10
                elif event.key == pygame.K_END:
                    FORWARD = True
                    PAUSE = True
                    #xSpace=xSpace+10
                    
                elif event.key == pygame.K_v:
                    SHOWVELOCITY = not SHOWVELOCITY
                elif event.key == pygame.K_i:
                    SHOWINDEX = not SHOWINDEX
                elif event.key == pygame.K_f:
                    SHOWFORCE = not SHOWFORCE
                elif event.key == pygame.K_r:
                    SHOWTPRE = not SHOWTPRE
                
                elif event.key == pygame.K_1:
                    SHOWWALLDATA = not SHOWWALLDATA
                elif event.key == pygame.K_2:
                    SHOWDOORDATA = not SHOWDOORDATA
                elif event.key == pygame.K_3:
                    SHOWEXITDATA = not SHOWEXITDATA
                #elif event.key == pygame.K_s:
                #    SHOWSTRESS = not SHOWSTRESS
                
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10

                elif event.key ==pygame.K_PERIOD:
                    TimeInterval = TimeInterval + 100
                elif event.key == pygame.K_COMMA:
                    TimeInterval = TimeInterval - 100
                    
                elif event.key == pygame.K_o:
                    agentIndex2=agentIndex2+1
                elif event.key == pygame.K_p:
                    agentIndex2=agentIndex2-1
                elif event.key == pygame.K_z:
                    agentIndex = -1
                    
        if MODETRAJ == False:
            screen.fill([0,0,0])

        #Time  = readFRec(fin,'f')  # Time index
        if T_INDEX == None or T_INDEX==T_END-1:
            #print("Simulation End!")
            #running=False
            #pygame.display.quit()
            #PAUSE=True
            T_INDEX=0
        else:
            if PAUSE==False:
                T_INDEX = T_INDEX+1
            else:
                if REWIND and T_INDEX>0:
                    T_INDEX = T_INDEX-1
                if FORWARD and T_INDEX<T_END-1:
                    T_INDEX = T_INDEX+1
        #nplim = readFRec(fin,'I')  # Number of particles in the PART class
        
        Time_t = Time[T_INDEX]
        XYZ_t = XYZ[T_INDEX]
        TAG_t = TAG[T_INDEX]
        INFO_t = INFO[T_INDEX]

        if npzflag:
            npzTime_t = npzTime[T_INDEX]
            npzSee_t = npzSee[T_INDEX,:,:]
            npzComm_t = npzComm[T_INDEX,:,:]
            npzTalk_t = npzTalk[T_INDEX,:,:]
            npzP_t = npzP[T_INDEX,:,:]
            npzC_t = npzC[T_INDEX,:,:]
            npzD_t = npzD[T_INDEX,:,:]
            npzB_t = npzB[T_INDEX,:,:]
            npzA_t = npzA[T_INDEX,:,:]
            try:
                npzVD_t = npzVD[T_INDEX,:,:]
                npzVE_t = npzVE[T_INDEX,:,:]
                npzEP_t = npzEP[T_INDEX,:,:]
            except:
                print("No npz data for visible door/exit and exit probability! Please check!")
            
        #############################
        ######### Drawing Process ######
        
        #print(npzTime_t, '\nnpzComm_t' ,npzComm_t, '\nnpzTalk_t' ,npzTalk_t)
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if SHOWTIME:
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("TimeInterval:" + format(TimeInterval, ".3f"), True, yellow, black)
            screen.blit(time_surface, [726,20]) #[750,350]*ZOOMFACTOR)
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Simulation Time:" + format(Time_t, ".3f"), True, yellow, black)
            screen.blit(time_surface, [726,40]) #[750,350]*ZOOMFACTOR)
            if npzflag:
                time_surface=myfont.render("Simulation Time (npz):" + str(npzTime_t), True, white, black)
                screen.blit(time_surface, [726,60]) #[750,350]*ZOOMFACTOR)
            
        drawWalls(screen, walls, ZOOMFACTOR, SHOWWALLDATA, xSpace, ySpace)
        #drawPATH(screen, holes, green, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, exits, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)
        drawDoors(screen, doors, ZOOMFACTOR, SHOWDOORDATA, xSpace, ySpace)
        #drawPATH(screen, entries, purple, ZOOMFACTOR, SHOWEXITDATA, xSpace, ySpace)

        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        if np.size(TAG_t)==1:
            TAG_t = np.array([TAG_t])
            
        #if debug:
            #print ("Show TAG_t: ", TAG_t)
        
        # Show Mouse Position
        (mouseX3, mouseY3) = pygame.mouse.get_pos()
        mouse_pos3 = np.array([mouseX3, mouseY3])
        #pygame.mouse.set_visible(False)
        #pygame.mouse.get_pressed() -> button1, button2, button3
        
        # Show Mouse Absolute and Relative Positions on the Screen
        myfont=pygame.font.SysFont("arial",17)
        text_surface=myfont.render(str((mouse_pos3-xyShift)*(1/ZOOMFACTOR)), True, black, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 18.0])
        text_surface=myfont.render(str(mouse_pos3), True, tan, white)
        screen.blit(text_surface, mouse_pos3+[0.0, 36.0])

        if drawLine:
            pygame.draw.line(screen, red, px1*ZOOMFACTOR+xyShift, px2*ZOOMFACTOR+xyShift, LINEWIDTH)
            measure_surface=myfont.render("length:" + str(np.round(np.linalg.norm(px1 - px2),2)), True, red, black)
            screen.blit(measure_surface, [726,80]) #[750,350]*ZOOMFACTOR)

        ################################
        # Next step is drawing agents by using evac data
        ################################  
        for idai in range(np.size(TAG_t)):

            if XYZ_t[2][idai]<Zmin or XYZ_t[2][idai]>Zmax:
                continue
            #scPos = np.array([0, 0])
            #scPosPhy = [XYZ_t[0][idai], XYZ_t[1][idai]]
            
            #scPos = [0, 0]
            agentsPos[int(TAG_t[idai]), 0] = int(XYZ_t[0][idai]*ZOOMFACTOR+xSpace)
            agentsPos[int(TAG_t[idai]), 1] = int(XYZ_t[1][idai]*ZOOMFACTOR+ySpace)

        ################################
        # Next step is drawing agents by using evac data
        ################################  
        for idai in range(np.size(TAG_t)):

            if XYZ_t[2][idai]<Zmin or XYZ_t[2][idai]>Zmax:
                continue
            #scPos = np.array([0, 0])
            scPosPhy = [XYZ_t[0][idai], XYZ_t[1][idai]]
            
            scPos = [0, 0]
            scPos[0] = int(XYZ_t[0][idai]*ZOOMFACTOR+xSpace)
            scPos[1] = int(XYZ_t[1][idai]*ZOOMFACTOR+ySpace)

            actualV = [INFO_t[0][idai], INFO_t[1][idai]]
            #actualVPos=(XYZ_t[:,idai]+actualV)*ZOOMFACTOR+xyShift
            actualVPos=[0, 0]
            actualVPos[0]=(XYZ_t[0][idai]+INFO_t[0][idai])*ZOOMFACTOR+xSpace
            actualVPos[1]=(XYZ_t[1][idai]+INFO_t[1][idai])*ZOOMFACTOR+ySpace
            
            desiredV = [INFO_t[2][idai], INFO_t[3][idai]]
            #desiredVPos=(XYZ_t[:,idai]+desiredV)*ZOOMFACTOR+xyShift
            desiredVPos = [0, 0]
            desiredVPos[0]=(XYZ_t[0][idai]+INFO_t[2][idai])*ZOOMFACTOR+xSpace
            desiredVPos[1]=(XYZ_t[1][idai]+INFO_t[3][idai])*ZOOMFACTOR+ySpace

            motiveF = [INFO_t[4][idai], INFO_t[5][idai]]
            motiveFPos = [0, 0]
            motiveFPos[0]=(XYZ_t[0][idai]+INFO_t[4][idai])*ZOOMFACTOR+xSpace
            motiveFPos[1]=(XYZ_t[1][idai]+INFO_t[5][idai])*ZOOMFACTOR+ySpace
    
            groupF = [INFO_t[6][idai], INFO_t[7][idai]]
            groupFPos = [0, 0]
            groupFPos[0]=(XYZ_t[0][idai]+INFO_t[6][idai])*ZOOMFACTOR+xSpace
            groupFPos[1]=(XYZ_t[1][idai]+INFO_t[7][idai])*ZOOMFACTOR+ySpace

            selfrepF = [INFO_t[8][idai], INFO_t[9][idai]]
            selfrepFPos = [0, 0]
            selfrepFPos[0]=(XYZ_t[0][idai]+INFO_t[8][idai])*ZOOMFACTOR+xSpace
            selfrepFPos[1]=(XYZ_t[1][idai]+INFO_t[9][idai])*ZOOMFACTOR+ySpace

            subF = [INFO_t[10][idai], INFO_t[11][idai]]
            subFPos = [0, 0]
            subFPos[0]=(XYZ_t[0][idai]+INFO_t[10][idai])*ZOOMFACTOR+xSpace
            subFPos[1]=(XYZ_t[1][idai]+INFO_t[11][idai])*ZOOMFACTOR+ySpace
            
            objF = [INFO_t[12][idai], INFO_t[13][idai]]
            objFPos = [0, 0]
            objFPos[0]=(XYZ_t[0][idai]+INFO_t[12][idai])*ZOOMFACTOR+xSpace
            objFPos[1]=(XYZ_t[1][idai]+INFO_t[13][idai])*ZOOMFACTOR+ySpace

            tpre = INFO_t[14][idai]
            exitSelected = INFO_t[15][idai]
            
            num_see_others = INFO_t[16][idai]
            num_others = INFO_t[17][idai]
            
            try:
                arousalLevel = INFO_t[18][idai]
                stressLevel = INFO_t[19][idai]
            except:
                print("No stressLevel data in the output binary file!")
                
            #temp = int(100*agent.ratioV)
            #AGENTCOLOR = [0,0,temp]
            #color_para = [0, 0, 0]
            #color_para[0] = int(255*min(1, agent.ratioV))
            
            if tpre > Time_t:
                try:
                    pygame.draw.circle(screen, black, scPos, int(npzRadius[TAG_t[idai]]*ZOOMFACTOR), LINEWIDTH+2)
                except:
                    pygame.draw.circle(screen, black, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)
            else:
                try:
                    pygame.draw.circle(screen, tan, scPos, int(npzRadius[TAG_t[idai]]*ZOOMFACTOR), LINEWIDTH)
                except:
                    pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)
                    
            if SHOWINDEX:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render(str(TAG_t[idai]), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, scPos)

            if SHOWTPRE:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",16)
                text_surface=myfont.render(str(tpre), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, scPos) #+[0.0, -100*ZOOMFACTOR])
            
            if SHOWVELOCITY:
                pygame.draw.line(screen, orange, scPos, actualVPos, 2)
                pygame.draw.line(screen, yellow, scPos, desiredVPos, 2)            
            

            if SHOWFORCE:
                pygame.draw.line(screen, red, scPos, motiveFPos, 2)
                pygame.draw.line(screen, lightpink, scPos, groupFPos, 2)    
                pygame.draw.line(screen, cyan, scPos, selfrepFPos, 2)  
            
            if np.linalg.norm(mouse_pos3-scPos)<10.0:
                
                #agentIndex2 = agentIndex
                agentIndex = TAG_t[idai]

                pygame.draw.line(screen, red, scPos, motiveFPos, 2)
                pygame.draw.line(screen, lightpink, scPos, groupFPos, 2)
                pygame.draw.line(screen, cyan, scPos, selfrepFPos, 2)  

                print(str(TAG_t[idai])+'num_see_others:'+str(INFO_t[16][idai]))
                print(str(TAG_t[idai])+'num_others:'+str(INFO_t[17][idai]))

                #myfont=pygame.font.SysFont("arial",16)
                #text_surface=myfont.render("@subF:"+format(np.linalg.norm(subF), ".3f")+str(subF), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 159.0])
                #text_surface=myfont.render("@objF:"+format(np.linalg.norm(objF), ".3f")+str(objF), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 179.0])

                if npzflag:
                    print('See List:\n'+str(TAG_t[idai])+str(npzSee_t[TAG_t[idai],:]))
                    print('Communication List:\n'+str(TAG_t[idai])+str(npzComm_t[TAG_t[idai],:])) #[TAG_t[idai],:]))
                    print('Talk List:\n'+str(TAG_t[idai])+str(npzTalk_t[TAG_t[idai],:]))

                    #text_surface=myfont.render("npzD:"+str(np.round(npzD_t[TAG_t[idai],:],2)), True, black, white)
                    #screen.blit(text_surface, mouse_pos3+[0.0, 97.0])
                    #text_surface=myfont.render("npzA:"+str(npzA_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, mouse_pos3+[0.0, 116.0])
                    #text_surface=myfont.render("npzB:"+str(npzB_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, mouse_pos3+[0.0, 136.0])

                    text_surface=myfont.render("See List:         "+str(npzSee_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, mouse_pos3+[0.0, 55.0])
                    text_surface=myfont.render("Attention List:"+str(npzComm_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, mouse_pos3+[0.0, 76.0])
                    #text_surface=myfont.render("Talk List :"+str(npzTalk_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, mouse_pos3+[0.0, 196.0])
                                    
                #text_surface=myfont.render("V:"+str(V[iii, jjj, T_INDEX]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 103.0])
                #text_surface=myfont.render("Ud:"+str(Ud0[iii, jjj]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 123.0])
                #text_surface=myfont.render("Vd:"+str(Vd0[iii, jjj]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 143.0])
                #text_surface=myfont.render("BLD:"+str(BLDinfo[iii, jjj]), True, black, white)
                #screen.blit(text_surface, mouse_pos3+[0.0, 169.0])

            #tempID = agentIndex%(np.size(TAG_t)+1)
            if agentIndex == TAG_t[idai]:
                #try:
                #    pygame.draw.circle(screen, tan, scPos, int(npzRadius[TAG_t[idai]]*ZOOMFACTOR), LINEWIDTH)
                #except:
                #    pygame.draw.circle(screen, tan, scPos, int(0.8*ZOOMFACTOR), LINEWIDTH)
                #pygame.draw.circle(screen, IndianRed, scPos, int(0.3*ZOOMFACTOR), 6)
                #pygame.draw.circle(screen, tan, scPos, int(0.3*ZOOMFACTOR), LINEWIDTH)
                myfont=pygame.font.SysFont("arial",20)
                text_surface=myfont.render(str(TAG_t[idai]), True, (0,0,0), orange)
                screen.blit(text_surface, scPos)
                
                pygame.draw.line(screen, red, scPos, motiveFPos, 2)
                pygame.draw.line(screen, lightpink, scPos, groupFPos, 2)
                pygame.draw.line(screen, cyan, scPos, selfrepFPos, 2)  
                
                myfont=pygame.font.SysFont("arial",17)
                text_surface=myfont.render('agentID:'+str(TAG_t[idai]), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [726.0, 118.0])
                text_surface=myfont.render("tpre:"+format(tpre, ".3f"), True, black, white)
                screen.blit(text_surface, [726.0, 138.0])
                text_surface=myfont.render("exit:"+str(exitSelected), True, black, white)
                screen.blit(text_surface, [726.0, 160.0])

                text_surface=myfont.render("@subF:"+format(np.linalg.norm(subF), ".3f"), True, black, white)
                screen.blit(text_surface, [726.0, 185.0])
                text_surface=myfont.render("@objF:"+format(np.linalg.norm(objF), ".3f"), True, black, white)
                screen.blit(text_surface, [726.0, 205.0])
                text_surface=myfont.render("@motiveF:"+format(np.linalg.norm(motiveF), ".3f"), True, black, white)
                screen.blit(text_surface, [726.0, 225.0])
                text_surface=myfont.render("@socialF:"+format(np.linalg.norm(groupF), ".3f"), True, black, white)
                screen.blit(text_surface, [726.0, 245.0])
                text_surface=myfont.render("@selfrepF:"+format(np.linalg.norm(selfrepF), ".3f"), True, black, white)
                screen.blit(text_surface, [726.0, 265.0])
                
                if npzflag:

                    text_surface=myfont.render("position:"+str(np.round(scPosPhy,2)), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 37.0])

                    text_surface=myfont.render("Attention List:"+str(npzComm_t[TAG_t[idai],:]), True, orange, white)
                    screen.blit(text_surface,  np.round(scPos, 2)+[0.0, 55.0])
                    text_surface=myfont.render("Talk List:         "+str(npzTalk_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface,  np.round(scPos, 2)+[0.0, 76.0])

                    text_surface=myfont.render("npzP:"+str(np.round(npzP_t[TAG_t[idai],:],2)), True, orange, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 97.0])
                    text_surface=myfont.render("npzC:"+str(np.round(npzC_t[TAG_t[idai],:],2)), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 116.0])

                    text_surface=myfont.render("npzD:"+str(np.round(npzD_t[TAG_t[idai],:],2)), True, orange, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 136.0])
                    text_surface=myfont.render("npzA:"+str(np.round(npzA_t[TAG_t[idai],:],2)), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 158.0])
                    text_surface=myfont.render("npzB:"+str(np.round(npzB_t[TAG_t[idai],:],2)), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 176.0])
                    text_surface=myfont.render("exitProb:"+str(np.round(npzEP_t[TAG_t[idai],:],2)), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 196.0])
                    text_surface=myfont.render("stressLevel:"+str(format(stressLevel, ".3f")), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 216.0])
                    text_surface=myfont.render("aroualLevel:"+str(format(arousalLevel, ".3f")), True, black, white)
                    screen.blit(text_surface, np.round(scPos, 2)+[0.0, 236.0])

                    #text_surface=myfont.render("See List:    "+str(npzSee_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, scPos+[0.0, 155.0])
                    #text_surface=myfont.render("Attention List:"+str(npzComm_t[TAG_t[idai],:]), True, black, white)
                    #screen.blit(text_surface, scPos+[0.0, 176.0])
                    for idaj in range(n_agents):  #np.size(npzComm_t[TAG_t[idai],:]):
                        if npzComm_t[TAG_t[idai],idaj]==1:
                            ajPos = agentsPos[idaj,:]
                            pygame.draw.line(screen, orange, scPos, ajPos, 2)
                    
                    for idaj in range(n_agents): #np.size(npzTalk_t[TAG_t[idai],:]):
                        if npzTalk_t[TAG_t[idai],idaj]==1:
                            ajPos = agentsPos[idaj,:]
                            pygame.draw.line(screen, purple, scPos, ajPos, 2)
                    

            #myfont=pygame.font.SysFont("arial",16)
            #text_surface=myfont.render('agentIndex2:'+str(agentIndex2), True, (0,0,0), (255,255,255))
            #screen.blit(text_surface, [726.0, 620.0])
            #tempID = agentIndex%(np.size(TAG_t)+1)
            if agentIndex2%n_agents == TAG_t[idai]:
                
                
                myfont=pygame.font.SysFont("arial",20)
                text_surface=myfont.render(str(TAG_t[idai]), True, (0,0,0), purple)
                screen.blit(text_surface, scPos)
                
                myfont=pygame.font.SysFont("arial",17)
                text_surface=myfont.render('agent position:' \
                 + format(XYZ_t[0,idai], ".3f") + "   " \
                 + format(XYZ_t[1,idai], ".3f"), True, (0,0,0), (255,255,255)) # + "   " \
                 #+ format(XYZ_t[2,idai], ".3f"), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [206.0, 538.0])
                
                text_surface=myfont.render('agentIndex2:'+str(agentIndex2), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [26.0, 538.0])
                
                text_surface=myfont.render('agentID:'+str(TAG_t[idai]), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, [26.0, 560.0])
                    
                text_surface=myfont.render("@motiveF:"+format(np.linalg.norm(motiveF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 580.0])
                text_surface=myfont.render("@socialF:"+format(np.linalg.norm(groupF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 600.0])
                text_surface=myfont.render("@selfrepF:"+format(np.linalg.norm(selfrepF), ".3f"), True, black, white)
                screen.blit(text_surface, [26.0, 620.0])
                #text_surface=myfont.render("objF:"+str(int(np.linalg.norm(objF))), True, black, white)
                #screen.blit(text_surface, [206.0, 560.0])

                if npzflag:
                    text_surface=myfont.render("See List:"+str(npzSee_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, [206.0, 560.0])
                    text_surface=myfont.render("Atttion List: "+str(npzComm_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, [206.0, 580.0])
                    text_surface=myfont.render("Talk List:      "+str(npzTalk_t[TAG_t[idai],:]), True, black, white)
                    screen.blit(text_surface, [206.0, 600.0])
                    
                    try: 
                        text_surface=myfont.render("exitProb:"+str(np.round(npzEP_t[TAG_t[idai],:],2)), True, black, white)
                        screen.blit(text_surface, [206.0, 619.0])
    
                        
                        text_surface=myfont.render("P Array:        "+str(np.round(npzP_t[TAG_t[idai],:], 2)), True, purple, white)
                        screen.blit(text_surface, [506.0, 538.0])
                        text_surface=myfont.render("C Array:        "+str(np.round(npzC_t[TAG_t[idai],:], 2)), True, black, white)
                        screen.blit(text_surface, [506.0, 560.0])
                        text_surface=myfont.render("D Array:        "+str(np.round(npzD_t[TAG_t[idai],:], 2)), True, purple, white)
                        screen.blit(text_surface, [506.0, 579.0])
                        text_surface=myfont.render("A Array:        "+str(np.round(npzA_t[TAG_t[idai],:], 2)), True, black, white)
                        screen.blit(text_surface, [506.0, 599.0])
                        text_surface=myfont.render("B Array:        "+str(np.round(npzB_t[TAG_t[idai],:], 2)), True, black, white)
                        screen.blit(text_surface, [506.0, 619.0])
                    except:
                        pass
        
        REWIND=False
        FORWARD=False
        pygame.display.flip()
        clock.tick(TimeInterval)


if __name__ == "__main__":

    #doorProb = readDoorProb('tpre2020-3_2022-12-12_18_29_33.txt')
    doorProb = plotDoorProb('..\..\examples\DoorAlgorithm\2door2022Dec_2022-12-14_16_46_53.txt')
    #doorProb = readDoorProb('2door2022Dec_2022-12-13_15_44_33.txt')
    #print(doorProb)
    print(len(doorProb))
    #(I,J) = np.shape(doorProb)
    #for i in range(I): #len(doorProb)):
    #    print(doorProb[i])
    #    print('\n')
    plt.plot(doorProb)
    #plt.subplot(121, vd0)
    #plt.subplot(121, vd1)
    #plt.subplot(121, vd2)

    #plt.subplot(122, v0)
    #plt.subplot(122, v1)
    #plt.subplot(122, v2)
    plt.grid()
    plt.show()
    #csv.write('test.csv', doorProb)
