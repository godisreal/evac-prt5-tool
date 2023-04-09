# -*- coding: utf-8 -*-
"""
Created on  Aug 2020
@author: WP and Topi
"""

import numpy as np
import sys
import os
import struct
import pygame
import re

########################
##### Color Info as below ###
########################

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
Cyan = 0, 255, 255
LightCyan = 224, 255, 255
lightgreen = 193, 255, 193


#######################
####### debug flag  #######
#######################
debugReadFDS=True
debugReadEVAC=True
debugPygame=True

# Normalize a vector
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm


# There are two types of entities in buidling construction: obstruction and passage
# Define obstruction class as below, and obstruction specifies the area that an agent cannot go through
class obst(object):
    
    """
    id:
        obstacle id 
    mode: 
        obstacle type (Line, Rect)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Line -> [x1,y1,x2,y2]
        Rect -> [x,y,w,h] 
    """
    
    def __init__(self, oid=0, mode='line', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.id = oid
        self.mode = mode
        
        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])
        
        #self.attachedDoors=[]
        #self.isSingleWall = False
        self.inComp = 1
        self.arrow = 0
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)


    def direction(self, arrow):
        if self.mode=='line':
            # Direction: (StartX, StartY) --> (EndX, EndY)
            direction = -np.array([self.params[0], self.params[1]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            if arrow>0:
                return direction
            elif arrow<0:
                return -direction
            elif arrow==0:
                return np.array([0.0, 0.0])
        
        elif self.mode=='rect':
            pass
            # What is a good representation of no direction?  
            direction = None  # np.array([0.0, 0.0])  #NaN

            ### +1: +x
            ###  -1: -x
            ### +2: +y
            ###  -2: -y 
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
            return direction
    
    
# There are two types of entities in buidling construction: obstruction and passage
# Define passage class as below, and passage specifies the area that an agent can go through, and it may include doorways, exits, etc.  We can also brief this entity as path in our code.  
class passage(object):
    
    """
    id:
        door id 
    mode: 
        door type (Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Rect -> [x,y,w,h] 
        Circle -> [x,y,r,None]
    """
    
    def __init__(self, oid=0, mode='rect', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.id = oid
        self.mode = 'rect' # All the door are in form of rect
        self.exitSign = 0

        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])

        self.attachedWalls=[]
        self.inComp = 1
        self.isSingleDoor = False
        self.arrow = 1
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5


    def direction(self, arrow):
        ### +1: +x
        ###  -1: -x
        ### +2: +y
        ###  -2: -y 
        if arrow == 1:
            direction = -np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            direction = np.array([1.0, 0.0])
        elif arrow == -1:
            direction = np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            direction = np.array([-1.0, 0.0])
        elif arrow == 2:
            direction = -np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            direction = normalize(direction)
            direction = np.array([0.0, 1.0])
        elif arrow == -2:
            direction = np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            direction = normalize(direction)
            direction = np.array([0.0, -1.0])
        elif arrow == 0:
            direction = np.array([0.0, 0.0])
        return direction
            
    def edge(self):
        p1 = np.array([self.params[0], self.params[1]])
        p2 = np.array([self.params[0], self.params[3]])
        p3 = np.array([self.params[2], self.params[3]])
        p4 = np.array([self.params[2], self.params[1]])
        return p1, p2, p3, p4


# Read in the job name CHID from a FDS input file
def readCHID(FileName):

    findHEAD=False
    for line in open(FileName):
        if re.match('&HEAD', line):
            findHEAD=True
        if  findHEAD:
            if re.search('CHID', line):
                temp1=line.split('CHID')
                line1=temp1[1]
                temp2 =  line1.split('\'')
                keyInfo = temp2[1]
                return keyInfo
          
          #      temp2 =  line1.split('=')
          #      keyInfo = temp2[1]
          #      result = keyInfo.split(',')
          #  return result[0].strip('\'')
 
            
# Read in obstruction from a FDS input file
def readOBST(FileName, Keyword='&OBST', Zmin=0.0, Zmax=3.0):
    #fo = open("OBSTout.txt", "w+")
    obstFeatures = []
    findOBST=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findOBST=True
        if  findOBST:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip('= ')
                #line1=temp1[1].strip('= ')
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()
                coords = re.split(r'[\s\,]+', dataXYZ)
                if debugReadFDS:
                    print(coords)
                if float(coords[4])<Zmin and float(coords[5])<Zmin:
                    continue
                if float(coords[4])>Zmax and float(coords[5])>Zmax:
                    continue
                obstFeature = []
                obstFeature.append(float(coords[0]))
                obstFeature.append(float(coords[2]))
                obstFeature.append(float(coords[1]))
                obstFeature.append(float(coords[3]))
                obstFeatures.append(obstFeature)
                findOBST=False

            if debugReadFDS:
                print (line, '\n', obstFeature)

    #print >>fo, 'test\n'
    #print >>fo, 'OBST Features\n'
    #print >>fo, obstFeatures
    
    walls = []
    index = 0
    for obstFeature in obstFeatures:
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.mode = 'rect'
        wall.id = index
        wall.inComp = 1
        wall.arrow = 0
        walls.append(wall)
        index = index+1
    return walls

# Read in passage from a FDS input file
def readPATH(FileName, Keyword='&HOLE', Zmin=0.0, Zmax=3.0):
    #fo = open("HOLEout.txt", "w+")
    holeFeatures = []
    
    findPATH=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findPATH=True
            
        if  findPATH:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip('= ')
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()    
                coords = re.split(r'[\s\,]+', dataXYZ)
                if debugReadFDS:
                    print(coords)
                if float(coords[4])<Zmin and float(coords[5])<Zmin:
                    continue
                if float(coords[4])>Zmax and float(coords[5])>Zmax:
                    continue
                holeFeature = []
                holeFeature.append(float(coords[0]))
                holeFeature.append(float(coords[2]))
                holeFeature.append(float(coords[1]))
                holeFeature.append(float(coords[3]))
                holeFeatures.append(holeFeature)
                findPATH=False

                if debugReadFDS:
                    print (line, '\n', holeFeature)
                    #print >>fo, line
                    #print >>fo, holeFeature

    #print ('test\n')
    #print ('HOLE Features\n')
    #print (holeFeatures)

    doors = []
    index = 0
    for holeFeature in holeFeatures:
        door = passage()
        door.params[0]= float(holeFeature[0])
        door.params[1]= float(holeFeature[1])
        door.params[2]= float(holeFeature[2])
        door.params[3]= float(holeFeature[3])
        door.arrow = 0
        door.id = index
        door.inComp = 1
        door.exitSign = 0
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        doors.append(door)
        index = index+1
    return doors


def readEXIT(FileName, Zmin=0.0, Zmax=3.0, outputFile=None, ShowData=False):
    #fo = open("EXITout.txt", "w+")
    exitFeatures = []
    findEXIT=False
    for line in open(FileName):
        if re.match('&EXIT', line):
            findEXIT=True
        if findEXIT:
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1]
                temp =  line1.split('=')
                dataXYZ = temp[1]
                coords = dataXYZ.split(',')
                #if float(coords[4])<Zmin and float(coords[5])<Zmin:
                #    continue
                #if float(coords[4])>Zmax and float(coords[5])>Zmax:
                #    continue
                exitFeature = []
                exitFeature.append(float(coords[0]))
                exitFeature.append(float(coords[2]))
                exitFeature.append(float(coords[1]))
                exitFeature.append(float(coords[3]))
                exitFeatures.append(exitFeature)
                findEXIT=False

                if ShowData:
                    print (line, '\n', exitFeature)
                    #print >>fo, line
                    #print >>fo, exitFeature

    #print >>fo, 'test\n'
    #print >>fo, 'EXIT Features\n'
    #print >>fo, exitFeatures

    if outputFile:
        with open(outputFile, mode='wb+') as exit_test_file:
            csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
            index_temp=0
            for exitFeature in exitFeatures:
                csv_writer.writerow(['--', str(exitFeature[0]), str(exitFeature[1]), str(exitFeature[2]), str(exitFeature[3]), '0', str(index_temp), '1', '0'])
                index_temp=index_temp+1

    exits = []
    index = 0
    for exitFeature in exitFeatures:
        exit = passage()
        exit.params[0]= float(exitFeature[0])
        exit.params[1]= float(exitFeature[1])
        exit.params[2]= float(exitFeature[2])
        exit.params[3]= float(exitFeature[3])
        exit.arrow = 0   #  This need to be improved
        exit.id = index
        exit.inComp = 1
        exit.exitSign = 0
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
        exits.append(exit)
        index = index+1
    return exits


#######################
# Drawing the obstructions
#######################
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

   

#############################
# Drawing the path like holes,  doors, etc.  
#############################
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


##############################
# The function readFRec is mainly written by Topi
# Read fortran record, return payload as bytestring
def readFRec(infile,fmt):
    len1   = infile.read(4)
    if not len1:
        return None
    len1   = struct.unpack('@I', len1)[0]

    if len1==0:
        len2=infile.read(4)
        return None
    num    = int(len1/struct.calcsize(fmt))
    fmt2   = str(num)+fmt
    if num>1:
        result = struct.unpack(fmt2,infile.read(len1))
    else:
        result = struct.unpack(fmt2,infile.read(len1))[0]  #?? why no list here??
    len2   = struct.unpack('@I', infile.read(4))[0]
    if fmt == 's':
        result=result[0] #.decode().rstrip()
    return result


#################################
# The function readPRTfile is mainly written by Topi
#Assumes single precision
def readPRTfile(fname, wrtxt = True, max_time=np.Inf, mode='evac'):

    fin = open(fname,'rb')
    temp = fname.split('.prt5')
    outfn = temp[0]
    outfile = open(outfn + ".txt", "w")
    
    one_integer=readFRec(fin,'I')  #! Integer 1 to check Endian-ness
    version=readFRec(fin,'I')       # FDS version number
    n_part=readFRec(fin,'I')        # Number of PARTicle classes
    #print(n_part)
    q_labels = []
    q_units  = []
    for npc in range(0,n_part):
        n_quant,zero_int=readFRec(fin,'I')  # EVAC_N_QUANTITIES, ZERO_INTEGER
        for nq in range(0,n_quant):
            smv_label=readFRec(fin,'s')
            units    =readFRec(fin,'s')
            q_units.append(units)  
            q_labels.append(smv_label)
    Q=[]
    T  = []
    #diam =[] ??? Not used in this program
    XYZ = []
    TAG = []
    while True:

        Time  = readFRec(fin,'f')  # Time index
        if Time == None or Time>max_time:
            break
        nplim = readFRec(fin,'I')  # Number of particles in the PART class
        if nplim>0:
            xyz  = np.array(readFRec(fin,'f'))
            tag  = np.array(readFRec(fin,'I'))
            q    = np.array(readFRec(fin,'f'))

            #print >> outfile, "g", q, "\n"
            if mode=='evac':
                xyz.shape = (7,nplim) # evac data: please check dump_evac() in evac.f90
            else: 
                xyz.shape = (3,nplim) # particle data: please check dump_part() in dump.f90
            
            q.shape   = (n_quant, nplim)
            
            if wrtxt:
                outfile.write("xyz:" + str(xyz) + "\n") 
                outfile.write("tag:" + str(tag) + "\n")           
                outfile.write( "q:" + str(q) + "\n")

            # process timestep data
            T.append(Time)
            XYZ.append(xyz)
            TAG.append(tag)
            Q.append(q)
        else:
            tmp = fin.read(24)
    
    fin.close()
    outfile.close()
    #np.savez( outfn + ".npz", T, XYZ, TAG, Q)
    #return (np.array(T),np.hstack(Q),q_labels,q_units)
    return T, XYZ, TAG, Q


def visualizeAgents(fname, fdsfile=None, Zmin=0.0, Zmax=3.0, agents = None):
    
    # Because visualizeEvac is a 2D visualizer, we can only show agents in a single floors each time and if there are multiple floors in fds+evac simulation, users should specify which floor they want to visualize.  Otherwise there will be overlap of agents in different floors.  The default values are given by Zmin=0.0 and Zmax=3.0, which means the gound floor approximately.  
 
     # Therefore It is recommended for users to first open .fds input file to see if there are multiple floors.  User should specify Zmin and Zmax and agents are visualized in z axis between Zmin and Zmax.  
        
    #Zmin is the lower bound of z values in a floor (e.g., often z lower bound of an evacuation mesh)
    #Zmax is the upper bound of z values in a floor (e.g., often z upper bound of an evacuation mesh)
    
    # Agents define a list of agents to be visualized in pygame screen
    
    # If there are already .txt data extracted from .prt5 file, the visualizer will not repeat to write .txt file because it may be time-consuming.  
    temp = fname.split('.prt5')
    outtxt = temp[0]+".txt"
    if os.path.exists(outtxt):
        wrtxt=False
    else:
        wrtxt=True
     
    # Extract data from .prt5 data file
    Time, XYZ, TAG, INFO = readPRTfile(fname, wrtxt)
        
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

        # This is due to readFRec:.  Let x become [x] when x is a scalar 
        if np.size(TAG_t)==1:
            TAG_t = np.array([TAG_t])
        ################################
        # Next step is drawing agents by using evac data
        ################################  
        for idai, ai in enumerate(TAG_t):
            if ai not in agents: 
                continue
            if XYZ_t[2][idai]<Zmin or XYZ_t[2][idai]>Zmax:
                continue
            #scPos = np.array([0, 0])
            scPos = [0, 0]
            scPos[0] = int(XYZ_t[0][idai]*ZOOMFACTOR+xSpace)
            scPos[1] = int(XYZ_t[1][idai]*ZOOMFACTOR+ySpace)
            
            color_para = [255, 0, 0]
            #color_para[0] = int(255*min(1, agent.ratioV))
            pygame.draw.circle(screen, color_para, scPos, int(2.0), 2)
            #pygame.draw.circle(screen, color_para, scPos, int(0.2*ZOOMFACTOR), 2)
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)

        REWIND=False
        FORWARD=False
        pygame.display.flip()
        clock.tick(20)


def visualizeEvac(fname, fdsfile=None, Zmin=0.0, Zmax=3.0):
    
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
    Time, XYZ, TAG, INFO = readPRTfile(fname, wrtxt)
        
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
        #INFO_t = INFO[T_INDEX]

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
            
            color_para = [255, 0, 0]
            #color_para[0] = int(255*min(1, agent.ratioV))
            pygame.draw.circle(screen, color_para, scPos, int(2.0), 2)
            #pygame.draw.circle(screen, color_para, scPos, int(0.2*ZOOMFACTOR), 2)
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)

        REWIND=False
        FORWARD=False
        pygame.display.flip()
        clock.tick(20)

if __name__ == "__main__":
    #if len(sys.argv)<2:
    #    sys.exit("Give .prt5 file as argument")
    #T,Q,labels,units =  readPRTfile(sys.argv[1])
    #print(labels,units)
    #print(len(T),Q.shape)
    CHID=readCHID('./examples/'+'SMOKE_DET3.fds')
    print (CHID)
    #readPRTfile(CHID+'_evac_0001.prt5')
    #visualizeEvac(CHID+'_evac_0001.prt5', None) #"SMOKE_DET3.fds")
    visualizeAgents('./examples/'+CHID+'_evac_0001.prt5', './examples/'+'SMOKE_DET3.fds', 0.0, 3.0, [1,18, 42])
    #visualizeEvac('./examples/'+CHID+'_evac_0001.prt5', './examples/'+'SMOKE_DET3.fds', 0.0, 3.0)
