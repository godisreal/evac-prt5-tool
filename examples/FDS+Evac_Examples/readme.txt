There are many old examples for FDS+Evac

Step (1): Run fds command to get evac prt5 data
fds <inputfilename.fds>
Step (2): Visualize evac prt5 file.  Use the command as below. 
python ui.py -> select FDS input file -> select output prt5 data for 2D visualization

The program is compatible to both python 2 and python 3.  The GUI is built by tkinter.  The program is also dependent on numpy and pygame.  
