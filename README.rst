
evac-prt5-tool
--------------

|Python2| |Python3|

This program is developed based on numpy, pygame and tkinter (optional).  You will need these three modules installed before you can run the code.  The program is compatible to both Python 2 and Python 3.  There is a simple GUI developed with the source code and the program is started by running the python script as below. ::
python ui.py.  

If you find any problem when using this program, please use issue trackers to report errors.  Thanks.     

Quick Start
-----------
For our simulation platform of CrowdEgress, users need to first run a study case and generate an output binary data file (with suffix .bin).  The binary data will be extracted and visualized by this evac-prt5-tool.  
For fds+evac, users should first run a fds+evac case by using either fds5 or fds6, and ensure you get prt5 data file (with suffix .prt5).  The binary data will be extracted and visualized by this evac-prt5-tool.  

The binary data from our simulation platform CrowdEgress is compatible with the fds+evac prt5 data and thus they are extracted and visualized by the same button in GUI. 
<write binary data into txt file>: Write the data into a text file, and it is compliant for both bin or prt5 data file. 
<visualize binary data by pygame>: Visualize the data by using pygame, and it is compliant for both bin or prt5 data file. .   

Users need to select the fds+evac input file together with prt5 data file if the compartment layout is to be visualized together with the agent movement data for a fds+evac test case.  In the GUI window, uses could either read the bin/prt5 data into a text file or visualize the data by pygame (SDL for python).  In the pygame screen you can zoom in or zoom out the simulation.  This program deals with one-floor scenario because it displays agent trajactories in 2D space. 

Please try the following keys when the evac data is visualized by pygame.  Have fun!
<Space>: Pause simulation;
<PageUp> <PageDown>: Zoom in or zoom out entities;
<Home> <End>: Rewind or forward; 
<Up> <Down> <Left> <Right>: Move entities vertically or horizonally;
<T>: Draw Trajectory of agents

Credits
-------
This python script is extended based on Topi's contribution, please see FDS discussion forum for details.
https://groups.google.com/g/fds-smv/c/dFUWR00T6hw

Thank Topi for sharing his wonderful python script and thank Salah Benkorichi for sending this thread to me!
I mainly modified xyz.shape = (7,nplim) for evac prt5 data. In Topi's script it was initially given by xyz.shape = (3,nplim) for Lagrangian Particles. We use xyz.shape = (7,nplim) for evac prt5 data.  

We need your help to improve this small program! New contributors are welcome.  


Citation
--------
If you use this software in your research, please consider citing this project as:
P. Wang, X. Wang, P. B. Luh, N. Olderman, C. Wilkie, T. Korhonen, ¡°CrowdEgress: A Multi-Agent Simulation Platform for Pedestrian Crowd,¡± Technical Report (User Manual), arXiv:2406.08190 [physics.soc-ph], 2024.  
